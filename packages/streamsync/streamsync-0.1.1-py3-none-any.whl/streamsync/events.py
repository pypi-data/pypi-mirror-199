import io
import traceback
from contextlib import redirect_stdout
from streamsync.types import StreamsyncEvent
from streamsync.core import Evaluator, EventDeserialiser, StreamsyncState
import streamsync
import streamsyncuserapp
import logging

class EventHandler:
    def __init__(self, session_state: StreamsyncState):
        self.session_state = session_state
        self.deser = EventDeserialiser(session_state)
        self.evaluator = Evaluator(session_state)

    def call_handler_callable(self, ev: StreamsyncEvent):
        event_type = ev["type"]
        instance_path = ev["instancePath"]
        target_id = instance_path[-1]["componentId"]

        logging.debug(
            f"Handling event with type {event_type} and id {target_id}.")

        target_component = streamsync.component_manager.components[target_id]

        handler = target_component.handlers.get(event_type)
        if not handler:
            raise ValueError(
                f"The handler for '{ event_type }' couldn't be found. It may have not been synchronised yet."
            )

        if not hasattr(streamsyncuserapp, handler):
            raise ValueError(
                f"""Invalid handler. Couldn't find the handler "{ handler }".""")
        callable_handler = getattr(streamsyncuserapp, handler)

        if not callable(callable_handler):
            raise ValueError(
                "Invalid handler. The handler isn't a callable object.")

        arg_names = callable_handler.__code__.co_varnames
        args = []
        for arg_name in arg_names:
            if arg_name == "state":
                args.append(self.session_state)
            elif arg_name == "payload":
                payload = ev["payload"]
                args.append(payload)
            elif arg_name == "context":
                context = self.evaluator.get_context_data(ev["instancePath"])
                args.append(context)

        result = None
        with redirect_stdout(io.StringIO()) as f:
            result = callable_handler(*args)
        captured_stdout = f.getvalue()
        if captured_stdout:
            self.session_state.add_log_entry(
                "info",
                "Stdout message",
                captured_stdout
            )
        return result

    def handle(self, ev: StreamsyncEvent):
        event_type = ev["type"]
        ok = True

        try:
            self.deser.transform(ev)
        except BaseException:
            ok = False
            self.session_state.add_notification(
                "error", "Error", f"A deserialisation error occurred when handling event '{ event_type }'.")
            self.session_state.add_log_entry("error", "Deserialisation Failed",
                                             f"The data sent might be corrupt. A runtime exception was raised when deserialising event '{ event_type }'.", traceback.format_exc())

        result = None
        try:
            result = self.call_handler_callable(ev)
        except BaseException:
            ok = False
            self.session_state.add_notification("error", "Runtime Error", f"An error occurred when processing event '{ event_type }'.",
                                                )
            self.session_state.add_log_entry("error", "Runtime Exception",
                                             f"A runtime exception was raised when processing event '{ event_type }'.", traceback.format_exc())

        return {"ok": ok, "result": result}
