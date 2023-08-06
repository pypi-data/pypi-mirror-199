import copy
import inspect
from typing import Any, Dict, List, Optional, Set, Union
import urllib.request
import base64
import io
import re
import json
from streamsync.types import Readable, InstancePath


class Config:

    is_mail_enabled_for_log = False


class StateProxy:

    """
    The root user state and its children (nested states) are instances of this class.
    Provides proxy functionality to detect state mutations via assignment.
    """

    def __init__(self, raw_state: Dict[str, Any] = {}):
        self.state: Dict[str, Any] = {}
        self.mutated: Set[str] = set()
        self.ingest(raw_state)

    def ingest(self, raw_state: Dict[str, Any]):
        for key, raw_value in raw_state.items():
            self.__setitem__(key, raw_value)

    def __getitem__(self, key):
        return self.state.get(key)

    def __setitem__(self, key, raw_value):

        # Items that are dictionaries are converted to StateProxy instances

        if isinstance(raw_value, dict):
            value = StateProxy(raw_value)
        else:
            value = raw_value

        self.state[key] = value
        self.apply(key)

    def apply(self, key):
        self.mutated.add(key)

    def get_mutations_as_dict(self):
        if len(self.mutated) == 0:
            return

        serialised_mutations = {}
        for key, value in self.state.items():
            if key.startswith("_"):
                continue
            serialised_value = None
            if isinstance(value, StateProxy):
                child_mutations = value.get_mutations_as_dict()
                if child_mutations is None:
                    continue
                for child_key, child_mutation in child_mutations.items():
                    nested_key = f"{key}.{child_key}"
                    serialised_mutations[nested_key] = child_mutation
            elif key in self.mutated:
                serialised_value = None
                try:
                    serialised_value = state_serialiser.serialise(value)
                except StateSerialiserException:
                    raise ValueError(
                        f"""Couldn't serialise value of type "{ type(value) }" for key "{ key }".""")
                serialised_mutations[key] = serialised_value

        self.mutated = set()
        return serialised_mutations

    def to_dict(self):
        serialised = {}
        for key, value in self.state.items():
            if key.startswith("_"):
                continue
            serialised_value = None
            try:
                serialised_value = state_serialiser.serialise(value)
            except StateSerialiserException:
                raise ValueError(
                    f"""Couldn't serialise value of type "{ type(value) }" for key "{ key }".""")
            serialised[key] = serialised_value
        return serialised


class StreamsyncState():

    """
    Root state. Comprises user configurable state and
    mail (notifications, log entries, etc).
    """

    LOG_ENTRY_MAX_LEN = 4096

    def __init__(self, raw_state: Dict[str, Any] = {}, mail=[]):
        self.user_state: StateProxy = StateProxy(raw_state)
        self.mail = mail

    @classmethod
    def get_new(cls):
        """ Returns a new StreamsyncState instance set to the initial state."""

        cloned_user_state = copy.deepcopy(initial_state.user_state.state)
        cloned_mail = copy.deepcopy(initial_state.mail)
        return StreamsyncState(cloned_user_state, cloned_mail)

    def reset_to_initial_state(self):
        self.user_state.mutated: Set[str] = set()
        self.user_state.state = copy.deepcopy(initial_state.user_state.state)
        self.mail = copy.deepcopy(initial_state.mail)

    def __getitem__(self, key: str):
        return self.user_state.__getitem__(key)

    def __setitem__(self, key: str, raw_value: Any):
        return self.user_state.__setitem__(key, raw_value)

    def add_mail(self, type: str, payload: Any):
        mail_item = {
            "type": type,
            "payload": payload
        }
        self.mail.insert(0, mail_item)

    def add_notification(self, type: str, title: str, message: str):
        self.add_mail("notification", {
            "type": type,
            "title": title,
            "message": message,
        })

    def add_log_entry(self, type: str, title: str, message: str, code: Optional[str] = None):
        if not Config.is_mail_enabled_for_log:
            return
        shortened_message = None
        if len(message) > StreamsyncState.LOG_ENTRY_MAX_LEN:
            shortened_message = message[0:StreamsyncState.LOG_ENTRY_MAX_LEN] + "..."
        else:
            shortened_message = message
        self.add_mail("logEntry", {
            "type": type,
            "title": title,
            "message": shortened_message,
            "code": code
        })

    def clear_mail(self):
        self.mail = []

    def set_page(self, active_page_key: str):
        self.add_mail("pageChange", active_page_key)

    def set_route_vars(self, route_vars: Dict[str, str]):
        self.add_mail("routeVarsChange", route_vars)


class Component:

    def __init__(self, id: str, type: str, content: Dict[str, str] = {}):
        self.id = id
        self.type = type
        self.content = content
        self.handlers: Dict[str, str] = {}
        self.parentId: Optional[str] = None
        self.position: int = 0
        self.visible: bool = True

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "content": self.content,
            "parentId": self.parentId,
            "handlers": self.handlers,
            "position": self.position,
            "visible": self.visible
        }


class ComponentManager:

    def __init__(self):
        self.counter: int = 0
        self.components: Dict[str, Component] = {}
        root_component = Component("root", "root", {})
        self.attach(root_component)

    def get_descendents(self, parent_id: str) -> List[Component]:
        children = list(filter(lambda c: c.parentId == parent_id,
                               self.components.values()))
        desc = children.copy()
        for child in children:
            desc += self.get_descendents(child.id)

        return desc

    def attach(self, component: Component):
        self.counter += 1
        self.components[component.id] = component

    def ingest(self, serialised_components: Dict[str, Any]):
        removed_ids = self.components.keys() - serialised_components.keys()

        for component_id in removed_ids:
            if component_id == "root":
                continue
            self.components.pop(component_id)
        for component_id, sc in serialised_components.items():
            component = Component(
                component_id, sc["type"], sc["content"])
            component.parentId = sc.get("parentId")
            component.handlers = sc.get("handlers")
            component.position = sc.get("position")
            component.visible = sc.get("visible")
            self.components[component_id] = component

    def to_dict(self):
        active_components = {}
        for id, component in self.components.items():
            active_components[id] = component.to_dict()
        return active_components


class EventDeserialiser:

    """Applies transformations to the payload of an incoming event, depending on its type.

    The transformation happens in place: the event passed to the transform method is mutated.

    Its main goal is to deserialise incoming content in a controlled and predictable way,
    applying sanitisation of inputs where relevant."""

    def __init__(self, session_state: StreamsyncState):
        self.evaluator = Evaluator(session_state)

    def transform(self, ev):
        
        # Events without payloads are safe
        # This includes non-custom events such as click

        if ev.get("payload") is None:
            return

        # Look for a method in this class that matches the event type
        # As a security measure, all custom event types must be linked to a transformer function.

        custom_event_name = ev["type"][3:]
        func_name = "transform_" + custom_event_name.replace("-", "_")
        if not hasattr(self, func_name):
            ev["payload"] = None
            raise ValueError(
                "No payload transformer available for custom event type.")
        tf_func = getattr(self, func_name)
        try:
            tf_payload = tf_func(ev)
        except BaseException:
            ev["payload"] = None
            raise RuntimeError("Payload transformation failed.")
        else:
            ev["payload"] = tf_payload

    def transform_option_change(self, ev):
        payload = ev.get("payload")
        if payload is None:
            return None
        options = self.evaluator.evaluate_field(
            ev["instancePath"], "options", True, """{ "a": "Option A", "b": "Option B" }""")
        if not isinstance(options, dict):
            raise ValueError("Invalid value for options")
        if payload not in options.keys():
            raise ValueError("Unauthorised option")
        return payload

    def transform_options_change(self, ev):
        payload = ev.get("payload")
        if payload is None:
            return None
        options = self.evaluator.evaluate_field(
            ev["instancePath"], "options", True, """{ "a": "Option A", "b": "Option B" }""")
        if not isinstance(options, dict):
            raise ValueError("Invalid value for options")
        if not isinstance(payload, list):
            raise ValueError(
                "Invalid multiple options payload. Expected a list.")
        if not all(item in options.keys() for item in payload):
            raise ValueError("Unauthorised option")
        return payload

    def transform_hashchange(self, ev):
        payload = ev.get("payload")
        page_key = payload.get("pageKey")
        route_vars = dict(payload.get("routeVars"))
        tf_payload = {
            "page_key": page_key,
            "route_vars": route_vars
        }
        return tf_payload

    def transform_change(self, ev):
        payload = ev["payload"]
        return payload

    def transform_webcam(self, ev):
        return urllib.request.urlopen(ev["payload"]).read()

    def transform_submit(self, ev):
        def file_item_transform(file_item: Dict):
            return {
                "name": file_item.get("name"),
                "type": file_item.get("type"),
                "data": urllib.request.urlopen(file_item.get("data")).read()
            }

        component_id = ev["instancePath"][-1]["componentId"]
        payload = ev["payload"]
        tf_payload = {}

        descendents = component_manager.get_descendents(component_id)

        for c in descendents:
            key = c.id
            if "key" in c.content:
                key = c.content["key"]
            if key not in payload:
                continue
            if c.type == "fileinput":
                tf_payload[key] = list(map(
                    file_item_transform, payload[key]))
                continue
            tf_payload[key] = payload[key]

        return tf_payload


class FileWrapper:

    """
    A wrapper for either a string pointing to a file or a file-like object with a read() method.
    Provides a method for retrieving the data as data URL.
    Allows for convenient serialisation of files.
    """

    def __init__(self, file: Union[Readable, str], mime_type: Optional[str]):
        if not file:
            raise ValueError("Must specify a file.")
        if not (
                callable(getattr(file, "read", None)) or
                isinstance(file, str)):
            raise ValueError(
                "File must provide a read() method or contain a string with a path to a local file.")
        self.file = file
        self.mime_type = mime_type

    def get_file_stream_as_dataurl(self, f_stream: Readable):
        base64_str = base64.b64encode(f_stream.read()).decode("latin-1")
        dataurl = f"data:{self.mime_type if self.mime_type is not None else '' };base64,{ base64_str }"
        return dataurl

    def get_as_dataurl(self):
        if isinstance(self.file, str):
            with open(self.file, "rb") as f_stream:
                return self.get_file_stream_as_dataurl(f_stream)
        elif callable(getattr(self.file, "read", None)):
            return self.get_file_stream_as_dataurl(self.file)
        else:
            raise ValueError("Invalid file.")


class BytesWrapper:

    """
    A wrapper for raw byte data.
    Provides a method for retrieving the data as data URL.
    Allows for convenient serialisation of byte data.
    """

    def __init__(self, raw_data: Any, mime_type: Optional[str]):
        self.raw_data = raw_data
        self.mime_type = mime_type

    def get_as_dataurl(self):
        b64_data = base64.b64encode(self.raw_data).decode("utf-8")
        durl = f"data:{ self.mime_type };base64,{ b64_data }"
        return durl


class StateSerialiserException(Exception):
    pass


class StateSerialiser:

    """
    Serialises user state values before sending them to the front end.
    Provides JSON-compatible values, including data URLs for binary data.
    """

    def serialise(self, v: Any):
        if isinstance(v, StateProxy):
            return self.serialise_dict_recursively(v.to_dict())
        if isinstance(v, (FileWrapper, BytesWrapper)):
            return self.serialise_ss_wrapper(v)
        if isinstance(v, dict):
            return self.serialise_dict_recursively(v)
        if isinstance(v, (list, str, int, float, bool)):
            return v
        if v is None:
            return v

        # Checking the MRO allows to determine object type without creating dependencies
        # to these packages

        v_mro = [
            f"{x.__module__}.{x.__name__}" for x in inspect.getmro(type(v))]

        if "matplotlib.figure.Figure" in v_mro:
            return self.serialise_matplotlib_fig(v)
        if "numpy.ndarray" in v_mro:
            return v.tolist()
        if "pandas.core.frame.DataFrame" in v_mro:
            return self.serialise_dict_recursively({
                "data": v.to_dict("list"),
                "metadata": {}
            })
        
        if hasattr(v, "to_dict") and callable(v.to_dict):
            # Covers Altair charts
            return self.serialise_dict_recursively(v.to_dict())

        raise StateSerialiserException(
            f"Object of type { type(v) } cannot be serialised.")

    def serialise_dict_recursively(self, d: Dict):
        return {k: self.serialise(v) for k, v in d.items()}

    def serialise_ss_wrapper(self, v: Union[FileWrapper, BytesWrapper]):
        return v.get_as_dataurl()

    def serialise_matplotlib_fig(self, fig):
        # It's safe to import matplotlib here without listing it as a dependency.
        # If this method is called, it's because a matplotlib figure existed.
        # If a matplotlib figure existed, the matplotlib module was imported
        import matplotlib.pyplot as plt

        iobytes = io.BytesIO()
        fig.savefig(iobytes, format="png")
        iobytes.seek(0)
        plt.close(fig)
        return FileWrapper(iobytes, "image/png").get_as_dataurl()


class Evaluator:

    """
    Evaluates templates and expressions in the backend.
    It allows for the sanitisation of frontend inputs.
    """

    template_regex = re.compile(r"[\\]?@{([\w\s.]*)}")

    def __init__(self, session_state: StreamsyncState):
        self.ss = session_state

    def evaluate_field(self, instance_path: InstancePath, field_key: str, as_json=False, default_field_value=""):
        context_data = self.get_context_data(instance_path)

        def replacer(matched):
            if matched.string[0] == "\\":  # Escaped @, don't evaluate
                return matched.string
            expr = matched.group(1).strip()
            expr_value = self.evaluate_expression(expr, context_data)

            serialised_value = None
            try:
                serialised_value = state_serialiser.serialise(expr_value)
            except StateSerialiserException:
                raise ValueError(
                    f"""Couldn't serialise value of type "{ type(expr_value) }" when evaluating field "{ field_key }".""")

            return json.dumps(serialised_value)

        component_id = instance_path[-1]["componentId"]
        component = component_manager.components[component_id]
        field_value = component.content.get(field_key) or default_field_value
        replaced = self.template_regex.sub(replacer, field_value)

        if as_json:
            return json.loads(replaced)
        else:
            return replaced

    def get_context_data(self, instance_path: InstancePath):
        context: Dict[str, Any] = {}

        for i in range(len(instance_path)):
            path_item = instance_path[i]
            component_id = path_item["componentId"]
            component = component_manager.components[component_id]
            if component.type != "repeater":
                continue
            if i + 1 >= len(instance_path):
                continue
            repeater_instance_path = instance_path[0:i+1]
            next_instance_path = instance_path[0:i+2]
            instance_number = next_instance_path[-1]["instanceNumber"]
            repeater_object = self.evaluate_field(
                repeater_instance_path, "repeaterObject", True)
            key_variable = self.evaluate_field(
                repeater_instance_path, "keyVariable", False, "itemId")
            value_variable = self.evaluate_field(
                repeater_instance_path, "valueVariable", False, "item")
            repeater_items = list(repeater_object.items())
            context[key_variable] = repeater_items[instance_number][0]
            context[value_variable] = repeater_items[instance_number][1]

        return context

    def evaluate_expression(self, expr: str, context_data: Dict[str, Any]):
        nested_key = expr.split(".")
        context_ref: Any = context_data
        state_ref: Any = self.ss.user_state.state
        for key in nested_key:
            if isinstance(state_ref, StateProxy):
                state_ref = state_ref[key]
            elif isinstance(state_ref, dict):
                state_ref = state_ref.get(key)

            if context_ref:
                context_ref = context_ref.get(key)

        result = None
        if context_ref:
            result = context_ref
        elif state_ref:
            result = state_ref

        if isinstance(result, StateProxy):
            return result.to_dict()
        return result


state_serialiser = StateSerialiser()
component_manager = ComponentManager()
initial_state = StreamsyncState()
