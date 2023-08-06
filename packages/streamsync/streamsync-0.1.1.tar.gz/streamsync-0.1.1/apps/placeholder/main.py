import streamsync as ss

# This is a placeholder to get you started or refresh your memory.
# Delete it or adapt it as necessary.

# Shows in the log when the app starts
print("Hello world!")

# Its name starts with _, so this function won't be exposed
def _update_message(state):
    is_even = state["counter"] % 2 == 0
    message = "The number is " + ("even" if is_even else "odd")
    state["message"] = message

def decrement(state):
    state["counter"] -= 1
    _update_message(state)

def increment(state):
    state["counter"] += 1
    print(f"The counter has been incremented.")
    _update_message(state)
    
# Initialise the state

initial_state = ss.init_state({
    "my_app": {
        "title": "My App"
    },
    "message": None,
    "counter": 26,
})

_update_message(initial_state)