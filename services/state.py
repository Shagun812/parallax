"""Persist runtime state"""
from pathlib import Path
from utils.loader import load_config
import json



STATE_FILE= Path(".parallax/state.json")


def default_state():
    cfg= load_config()
    state={"active_model": cfg.inference.default_model}

    return state


def write_state(state):

    if not STATE_FILE.parent.exists():
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(STATE_FILE,"w") as f:
        json.dump(state,f)


def read_state():

    if not STATE_FILE.exists():
        state=default_state()
        write_state(state)
        return state
        
    else:
        with open(STATE_FILE) as f:
            try:
                state = json.load(f)
                return state
            except json.JSONDecodeError:
                state=default_state()
                write_state(state)
                return state

                
def validate_state():
    cfg= load_config()
    state= read_state()

    if "active_model" not in state:
        state=default_state()
        write_state(state)
        return state
    
    else:

        active_model=state["active_model"]
        if active_model not in cfg.models:
            state=default_state()
            write_state(state)
            return state
        else:
            return state



def get_active_model():
    state=validate_state()
    return state["active_model"]

def set_active_model(model_name):
    state=validate_state()
    state["active_model"]= model_name
    write_state(state)

