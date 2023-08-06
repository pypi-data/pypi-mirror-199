from typing import Union, Optional, Dict, Any
from streamsync.core import Readable, FileWrapper, BytesWrapper, Config
from streamsync.core import initial_state, component_manager

component_manager
Config

VERSION = "0.1.1"


def pack_file(file: Union[Readable, str], mime_type: Optional[str]):
    
    """ Returns a FileWrapper for the file provided."""
    
    return FileWrapper(file, mime_type)


def pack_bytes(raw_data, mime_type: Optional[str]):

    """ Returns a BytesWrapper for the bytes raw data provided."""

    return BytesWrapper(raw_data, mime_type)


def init_state(state_dict: Dict[str, Any]):

    """
    Sets the initial state, which will be used as the starting point for
    every session.
    """
    
    initial_state.user_state.state = {}
    initial_state.user_state.ingest(state_dict)
    return initial_state
