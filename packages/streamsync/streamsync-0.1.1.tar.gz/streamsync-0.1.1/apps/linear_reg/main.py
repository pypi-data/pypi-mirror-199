import altair as alt
import streamsync as ss
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("demoData/sample_data.csv")

ss.init_state({
    "data": data,
    "reg_alpha": 0.4,
    "reg_beta": 100,
    "reg_chart": None,
    "buttons":{
        "show_error":{
            "state":True,
            "text": "Show Error"
        },
        "show_formula":{
            "state":True,
            "text": "Show Reg Formula",
        }
    },
})

def make_chart(state):
    fig, ax = plt.subplots()
    ax.scatter(
        state["data"].square_meters,
        state["data"].price
    )
    ax.set(
        xlabel="square meters",
        ylabel="price",
        ylim=(0,400),
        xlim=(0,None),
    )
    predictions = state["reg_alpha"] * state["data"].square_meters + state["reg_beta"]
    ax.plot(
        state["data"].square_meters,
        predictions,
        c="tab:gray",
    )
    if state["buttons"]["show_error"]["state"]:
        ax.vlines(
            state["data"].square_meters, 
            state["data"].price, 
            predictions,
            color='red',
        )
        mse = round(
            np.mean(
                np.square(
                    state["data"].price - predictions
                )
            ), 1
        )
        ax.text(
            x = 300,
            y = 50,
            s = f"$MeanSquaredError = {mse}$"
        )
    if state["buttons"]["show_formula"]["state"]:
        alpha = state["reg_alpha"]
        beta = state["reg_beta"]
        ax.text(
            x = 300,
            y = 100,
            s = f"y = {alpha} * square_meter + {beta}"
        )

    state["reg_chart"] = fig
    plt.close()

def show_error(state):
    state["buttons"]["show_error"]["state"] = not state["buttons"]["show_error"]["state"]
    if state["buttons"]["show_error"]["state"]:
        button_text = "Hide Error"
    else:
        button_text = "Show Error"
    state["buttons"]["show_error"]["text"] = button_text
    make_chart(state)

def show_formula(state):
    state["buttons"]["show_formula"]["state"] = not state["buttons"]["show_formula"]["state"]
    if state["buttons"]["show_formula"]["state"]:
        button_text = "Hide Reg Formula"
    else:
        button_text = "Show Reg Formula"
    state["buttons"]["show_formula"]["text"] = button_text
    make_chart(state)

def reg_var_increment(var_name, value, state):
    state[var_name]=round(state[var_name]+value,2)
    make_chart(state)

def alpha_increment(state):
    reg_var_increment("reg_alpha",0.1,state)

def alpha_decrement(state):
    reg_var_increment("reg_alpha",-0.1,state)

def beta_increment(state):
    reg_var_increment("reg_beta",10,state)

def beta_decrement(state):
    reg_var_increment("reg_beta",-10,state)



