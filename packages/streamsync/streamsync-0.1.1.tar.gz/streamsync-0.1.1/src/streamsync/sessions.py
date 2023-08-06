import secrets
from typing import Dict
from streamsync.core import StreamsyncState
import time

from streamsync.events import EventHandler

IDLE_SESSION_MAX_SECONDS = 3600


class StreamsyncSession:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.last_active_timestamp: int = int(time.time())
        new_state = StreamsyncState.get_new()
        self.session_state = new_state
        self.event_handler = EventHandler(new_state)

    def update_last_active_timestamp(self):
        self.last_active_timestamp = int(time.time())


class SessionManager:

    def __init__(self):
        self.sessions: Dict[str, StreamsyncSession] = {}

    def get_new_session(self):
        new_id = self.generate_session_id()
        new_session = StreamsyncSession(new_id)
        self.sessions[new_id] = new_session
        return new_session

    def get_session(self, session_id: str):

        # Id was specified but such session doesn't exist

        if session_id not in self.sessions:
            return None

        return self.sessions[session_id]

    def generate_session_id(self):
        return secrets.token_urlsafe(16)

    def clear_all(self):
        self.sessions = {}

    def reset_state_for_all(self):
        for session in self.sessions.values():
            session.session_state.reset_to_initial_state()

    def close_session(self, session_id: str):
        del self.sessions[session_id]

    def prune_sessions(self):
        cutoff_timestamp = int(time.time()) - IDLE_SESSION_MAX_SECONDS
        prune_sessions = []
        for session_id, session in self.sessions.items():
            if session.last_active_timestamp < cutoff_timestamp:
                prune_sessions.append(session_id)
        for session_id in prune_sessions:
            self.close_session(session_id)


session_manager = SessionManager()
