import streamsync as ss

print("Hello world! You'll see this message in the log")
print("If you edit the file somewhere else, for example, in VS Code, the code will reload automatically. Including dependencies!")

ss.init_state({
    "message": "Hello",
    "counter": 12,
    "_private": "I like white bread",
    "private": "I still like bologna on white bread now and then",
    "collapsible": "yes"
})

def toggle_collapsible(state):
    if state["collapsible"] == "yes":
        state["collapsible"] = "no"
    else:
        state["collapsible"] = "yes"

def increment(state):
    state["counter"] += 1
    print("you got to increment")


def slow_op():
    import time
    time.sleep(5)
    print("It's been five seconds")
