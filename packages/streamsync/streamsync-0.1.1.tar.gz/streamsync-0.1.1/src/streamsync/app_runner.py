import multiprocessing
import multiprocessing.connection
import threading
import asyncio
import concurrent.futures
import importlib
import inspect
import os
import sys
from types import FunctionType, ModuleType
import json
from typing import Dict
import watchdog.observers
import watchdog.events
from streamsync import VERSION

class SessionPruner(threading.Thread):

    """
    Prunes sessions in intervals, without interfering with the AppProcess server thread.  
    """

    PRUNE_SESSIONS_INTERVAL_SECONDS=60
    
    def __init__(self,
                 is_session_pruner_terminated: threading.Event):
        super().__init__()
        self.is_session_pruner_terminated = is_session_pruner_terminated

    def run(self):
        import streamsync.sessions

        while True:
            self.is_session_pruner_terminated.wait(timeout=SessionPruner.PRUNE_SESSIONS_INTERVAL_SECONDS)
            if self.is_session_pruner_terminated.is_set():
                return
            streamsync.sessions.session_manager.prune_sessions()

class AppProcess(multiprocessing.Process):

    """
    Streamsync runs the user's app code using an isolated process, based on this class.
    The main process is able to communicate with the user app process via app messages (e.g. event, componentUpdate).
    """

    def __init__(self, 
                 client_conn: multiprocessing.connection.Connection,
                 server_conn: multiprocessing.connection.Connection,
                 app_path: str,
                 mode: str,
                 run_code: str,
                 components: Dict,
                 is_app_process_server_ready: multiprocessing.Event):
        super().__init__()
        self.client_conn = client_conn
        self.server_conn = server_conn
        self.app_path = app_path
        self.mode = mode
        self.run_code = run_code
        self.components = components
        self.is_app_process_server_ready = is_app_process_server_ready
        self.packet_outbox = []

    def load_module(self):
        """
        Loads the entry point for the user code in module streamsyncuserapp.
        """

        module_name = "streamsyncuserapp"
        spec = importlib.util.spec_from_loader(module_name, loader=None)
        module: ModuleType = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        globals()[module_name] = module
        return module

    def get_user_functions(self):
        """
        Returns functions exposed in the user code module, which are potential event handlers.
        """

        import streamsyncuserapp
        all_user_functions = map(lambda x: x[0], inspect.getmembers(
                streamsyncuserapp, inspect.isfunction))
        exposed_user_functions = list(filter(lambda x: not x.startswith("_"), all_user_functions))
        return exposed_user_functions

    def handle_session_init(self):
        """
        Handles session initialisation and provides a starter pack.
        """

        import streamsync
        from streamsync.sessions import session_manager
        import traceback as tb

        session = session_manager.get_new_session()
        payload = {"userState": {}}
        payload["sessionId"] = session.session_id

        try:
            payload["userState"] = session.session_state.user_state.to_dict()
        except BaseException:
            session.session_state.add_log_entry(
                "error", "Serialisation error", tb.format_exc())

        payload["mail"] = session.session_state.mail
        session.session_state.clear_mail()
        payload["components"] = streamsync.component_manager.to_dict()
        payload["userFunctions"] = self.get_user_functions()
        return payload

    def handle_message(self, session_id: str, message: Dict):
        """
        Handles messages from the main process to the app's isolated process.
        """

        import streamsync
        from streamsync.sessions import session_manager

        session = None
        type = message.get("type")
        payload = message.get("payload")
        response = {
            "status": "error"
        }

        if type == "sessionInit":
            response["payload"] = self.handle_session_init()
            response["status"] = "ok"
            return response
        elif type == "checkSession":
            session = session_manager.get_session(session_id)
            if session:
                response["status"] = "ok"
            return response

        session = session_manager.get_session(session_id)
        if not session:
            return response
        session.update_last_active_timestamp()

        if type == "event":
            response["payload"] = session.event_handler.handle(payload)
            response["status"] = "ok"
            response["mutations"] = session.session_state.user_state.get_mutations_as_dict()
            response["mail"] = session.session_state.mail
            session.session_state.clear_mail()
            return response

        if self.mode == "edit" and type == "componentUpdate":
            streamsync.component_manager.ingest(payload)
            response["status"] = "ok"
            return response

    def execute_user_code(self):
        """
        Executes the user code and captures standard output.
        """

        import streamsync
        from contextlib import redirect_stdout
        import io
        import streamsyncuserapp

        with redirect_stdout(io.StringIO()) as f:
            exec(self.run_code, streamsyncuserapp.__dict__)
        captured_stdout = f.getvalue()

        if captured_stdout:
            streamsync.initial_state.add_log_entry(
                "info", "Stdout message during initialisation", captured_stdout)

    def apply_configuration(self):
        import streamsync

        if self.mode == "edit":
            streamsync.Config.is_mail_enabled_for_log = True
        elif self.mode == "run":
            streamsync.Config.is_mail_enabled_for_log = False

    def main(self):
        self.apply_configuration()
        import os
        os.chdir(self.app_path)
        self.load_module()
        # Allows for relative imports from the app's path
        sys.path.append(self.app_path)
        import streamsync
        import traceback as tb
        import signal

        try:
            self.execute_user_code()
        except BaseException:
            # Initialisation errors will be sent to all sessions via mail during session initialisation

            streamsync.initial_state.add_log_entry(
                "error", "Code Error", "Couldn't execute code. An exception was raised.", tb.format_exc())

        try:
            streamsync.component_manager.ingest(self.components)
        except BaseException:
            streamsync.initial_state.add_log_entry(
                "error", "UI Components Error", "Couldn't load components. An exception was raised.", tb.format_exc())

        def signal_handler(sig, frame):
            self.server_conn.close()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        self._run_app_process_server()

    def _handle_message_and_get_packet(self, message_id: int, session_id: str, message: Dict):
        response = self.handle_message(session_id, message)
        return (message_id, session_id, response)

    def _send_packet(self, packet_future: concurrent.futures.Future):
        result = packet_future.result()
        self.server_conn.send(result)

    def _run_app_process_server(self):
        is_app_process_server_terminated = threading.Event()
        session_pruner = SessionPruner(is_app_process_server_terminated)
        session_pruner.start()

        with concurrent.futures.ThreadPoolExecutor(100) as thread_pool:
            self.is_app_process_server_ready.set()
            while True:  # Starts app message server
                if self.server_conn.poll(1):
                    packet = self.server_conn.recv()
                    if packet is None:  # An empty packet terminates the process
                        self.server_conn.send(None) # Send empty packet to client for it to close
                        is_app_process_server_terminated.set()
                        session_pruner.join()
                        return
                    (message_id, session_id, message) = packet
                    thread_pool_future = thread_pool.submit(self._handle_message_and_get_packet,
                                                message_id, session_id, message)
                    thread_pool_future.add_done_callback(self._send_packet)

    def run(self):
        self.client_conn.close()
        self.main()


class FileEventHandler(watchdog.events.PatternMatchingEventHandler):

    """
    Watches for changes in files and triggers code reloads.
    """

    def __init__(self, update_callback: FunctionType):
        self.update_callback = update_callback
        super().__init__(patterns=["*.py"], ignore_patterns=[
            ".*"], ignore_directories=False, case_sensitive=False)

    def on_any_event(self, event):
        if event.event_type not in ("modified", "deleted", "created"):
            return
        self.update_callback()


class ThreadSafeAsyncEvent(asyncio.Event):

    """ Asyncio event adapted to be thread-safe."""

    def __init__(self):
        super().__init__()
        if self._loop is None:
            self._loop = asyncio.get_event_loop()

    def set(self):
        self._loop.call_soon_threadsafe(super().set)


class AppProcessListener(threading.Thread):

    """
    Listens to messages from the AppProcess server.
    Notifies receipt via events in response_events and makes the responses available in response_packets.  
    """

    def __init__(self,
                 client_conn: multiprocessing.connection.Connection,
                 is_app_process_server_ready: multiprocessing.Event,
                 response_packets: Dict,
                 response_events: Dict):
        super().__init__()
        self.client_conn = client_conn
        self.is_app_process_server_ready = is_app_process_server_ready
        self.response_packets = response_packets
        self.response_events = response_events

    def run(self):
        self.is_app_process_server_ready.wait()
        while True:
            if self.client_conn.poll(1):
                packet = self.client_conn.recv()
                if packet is None:
                    return
                message_id = packet[0]
                self.response_packets[message_id] = packet
                response_event = self.response_events.get(message_id)
                if response_event:
                    response_event.set()
                else:
                    raise ValueError("No response event found for message {message_id}.")

class AppRunner:

    """
    Starts a given user app in a separate process.
    Manages changes to the app.
    Allows for communication with the app via messages.
    """

    def __init__(self, app_path: str, mode: str):
        self.server_conn: multiprocessing.connection.Connection = None
        self.client_conn: multiprocessing.connection.Connection = None
        self.app_process: multiprocessing.Process = None
        self.saved_code: str = None
        self.run_code: str = None
        self.components:Dict = None
        self.is_app_process_server_ready = multiprocessing.Event()
        self.run_code_version:int = 0
        self.observer = None
        self.app_path:str = app_path
        self.response_events = {}
        self.response_packets = {}
        self.message_counter = 0

        if mode not in ("edit", "run"):
            raise ValueError("Invalid mode.")

        self.mode = mode

    def load(self):
        self.saved_code = self._load_persisted_script()
        self.run_code = self.saved_code
        self.components = self._load_persisted_components()

        if self.mode == "edit":
            self.observer = watchdog.observers.Observer()
            self.observer.schedule(
                FileEventHandler(self.reload_code_from_saved), path=self.app_path, recursive=True)
            self.observer.start()

        self._start_app_process()

    def get_run_code_version(self):
        return self.run_code_version

    async def dispatch_message(self, session_id, message):

        """
        Sends a message to the AppProcess server, waits for the listener to obtain a response and returns it.
        """

        message_id = self.message_counter
        self.message_counter += 1
        is_response_ready = ThreadSafeAsyncEvent()
        self.response_events[message_id] = is_response_ready
        packet = (message_id, session_id, message)        
        self.client_conn.send(packet)

        await is_response_ready.wait() # Set by the listener thread

        response_packet = self.response_packets.get(message_id)
        if response_packet is None:
            raise ValueError(f"Empty packet received in response to message { message_id }.")
        response_message_id, response_session_id, response = response_packet
        del self.response_packets[message_id]
        del self.response_events[message_id]
        if (session_id != response_session_id):
            raise PermissionError("Session mismatch.")
        if (message_id != response_message_id):
            raise PermissionError("Message mismatch.")

        return response

    def _load_persisted_script(self):
        with open(os.path.join(self.app_path, "main.py"), "r") as f:
            return f.read()

    def _load_persisted_components(self):
        file_payload: Dict = None
        with open(os.path.join(self.app_path, "ui.json"), "r") as f:
            file_payload = json.load(f)
        return file_payload.get("components")

    async def check_session(self, session_id: str):
        response = await self.dispatch_message(session_id, {
            "type": "checkSession"
        })
        is_ok: bool = response["status"] == "ok"
        return is_ok

    async def update_components(self, session_id: str, components: Dict):
        if self.mode != "edit":
            return

        self.components = components

        file_payload = {
            "metadata": {
                "streamsync_version": VERSION
            },
            "components": components
        }

        with open(os.path.join(self.app_path, "ui.json"), "w") as f:
            json.dump(file_payload, f, indent=4)

        return await self.dispatch_message(session_id, {
            "type": "componentUpdate",
            "payload": components
        })

    def save_code(self, session_id: str, saved_code: str):
        if self.mode != "edit":
            return

        with open(os.path.join(self.app_path, "main.py"), "w") as f:
            f.write(saved_code)
        self.saved_code = saved_code

    def _clean_process(self):
        # Terminate the AppProcess server by sending empty message
        # The empty message will bounce an empty message and terminate the client too
        self.client_conn.send(None)
        self.app_process.join()
        self.app_process.close()
        self.client_conn.close()
        self.server_conn.close()
        self.response_events = {}
        self.response_packets = {}

    def shut_down(self):
        if self.observer is not None:
            self.observer.stop()
            self.observer.join()
        if self.app_process is not None:
            self._clean_process()

    def _start_app_process(self):
        self.is_app_process_server_ready.clear()
        self.client_conn, self.server_conn = multiprocessing.Pipe(duplex=True)
        self.app_process = AppProcess(
            client_conn=self.client_conn,
            server_conn=self.server_conn,
            app_path=self.app_path,
            mode=self.mode,
            run_code=self.run_code,
            components=self.components,
            is_app_process_server_ready=self.is_app_process_server_ready)
        self.app_process.start()
        self.app_process_listener = AppProcessListener(self.client_conn, self.is_app_process_server_ready, self.response_packets, self.response_events)
        self.app_process_listener.start()

    def reload_code_from_saved(self):
        if not self.is_app_process_server_ready.is_set():
            return
        self.saved_code = self._load_persisted_script()
        self.update_code(None, self.saved_code)

    def update_code(self, session_id: str, run_code: str):
        if self.mode != "edit":
            return
        if not self.is_app_process_server_ready.is_set():
            return
        self.run_code = run_code
        self._clean_process()
        self._start_app_process()
        self.is_app_process_server_ready.wait()
        self.run_code_version += 1
