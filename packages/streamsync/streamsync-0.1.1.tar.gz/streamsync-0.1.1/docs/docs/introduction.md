# Introduction

## What is Streamsync?

Streamsync is an open-source framework that allows Python developers to create data apps using a drag-and-drop UI editor, while retaining the full power of Python in the backend. It's an alternative to Streamlit and Plotly Dash.

![alt text](sc1.png "Streamsync Builder screenshot")

It's fast.

- It uses streaming (WebSockets) to synchronise application state mutations between backend and frontend.
- The script is only loaded once, for all sessions.

It's neat.

- It provides strict separation between user interface and business logic.
- Event handlers are clearly defined and run in isolation.

It's all contained within a standard Python package. Deploy it in any cloud or even in a fifteen-dollar computer.

## How it works

### Overview

INSERT CHART HERE

Streamsync works by assigning each user session an application state and pushing it to the frontend. The frontend, in turn, produces events which trigger event handlers in the backend. Events trigger mutations to the application state, which are pushed to the frontend.

### In practice

**Step 1.** In `main.py`, the entry point for every app, the initial state is declared.

```py
import streamsync as ss

# The initial state is the same for every session
# Everyone starts from 0

ss.init_state({
    "counter": 0
})
```

**Step 2.** The user interface is created on Streamsync Builder, the framework's drag-and-drop UI builder. The UI gets hooked to the application state via state references, which have the syntax `@{my_variable}`. State mutations will be automatically synchronized via streaming, hence the framework's name. The user interface is saved in `ui.json`.

**Step 3.** Event handlers are defined in `main.py`. Event handlers receive the session state as an argument and mutate it.

```py
def click_increment(state):

    # The value of state will be different depending on which
    # session is triggering the event handler

    state["counter"] += 1
```

**Step 4.** The event handlers are hooked in the user interface. Events are sent from the frontend and processed in the backend by the relevant event handlers.

## Installation and Quickstart

Getting started with Streamsync is easy; it's all contained inside a standard Python package.

```sh
pip install streamsync
streamsync hello
```

- The first command will install Streamsync using pip.
- The second command will create a demo application in the subfolder "hello" and start Streamsync Builder. You will be able to access the server at http://localhost:3006.

## Commands

Streamsync is started from the command line. Once you've installed the package, the script "streamsync" should be available.

### Create

Creates a new application.

```sh
streamsync create [path]

# Creates a new application in subfolder "testapp"
streamsync create testapp
```

Applications are self-contained in their folders. To delete an application, simply delete the application folder.

### Run

Runs an existing application, starting a web server.

```sh
streamsync run [path]

# Run the application in subfolder "testapp"
streamsync run testapp
# Run the application using the specified port
streamsync run testapp --port=5001
```

### Edit

Starts Streamsync Builder for a given application, allowing you to modify it.

```sh
streamsync edit [path]

# Edit the application in subfolder "testapp"
streamsync edit testapp
# Edit the application, starting Builder in the specified port
streamsync edit testapp --port=5002
```

::: warning
Streamsync Builder is designed to be run locally or in protected development environments, as it gives full access to the underlying system.
:::

### Hello

Creates a demo app in the subfolder "hello" and starts Streamsync Builder.

```sh
streamsync hello
```

### Parameters Help

Shows a full overview of the valid parameters.

```sh
streamsync -h
```

# Guide: Create a data app

This short guide will take you through the creation of a basic data app using Streamsync.

The requirement is to create a data app

# Guide: Distributing a data app

# Components

```

```
