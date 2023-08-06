import altair as alt
import streamsync as ss
import pandas as pd

# INIT

data = pd.DataFrame({'a': list('CCCDDDEEE'),
                     'b': [10, 7, 4, 1, 2, 6, 8, 4, 1]})
chart = alt.Chart(data).mark_bar().encode(
    x='a',
    y='average(b)'
).configure_mark(color='#EF9906')

data_cereal = pd.read_csv("demoData/cereal.csv")

print("Hello world! You'll see this message in the log")

# STATE INIT

ss.init_state({
    "counter": 10,
    "chart": chart,
    "data_cereal": data_cereal
})

# EVENT HANDLERS

def increment(state):

    """
    Increments counter by one.
    """

    state["counter"] += 1


def slow_handler():

    """
    Example of a non-blocking, slow operation.
    """

    print("Slow handler triggered. You'll see this message in the log.")
    import time
    time.sleep(2)