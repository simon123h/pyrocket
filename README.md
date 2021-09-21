# pyrocket

A 2d self-landing rocket simulation written in Python.

## Requirements

You need `pygame` and `pymunk` installed, e.g. using
```bash
pip3 install --user pygame
pip3 install --user pymunk
```


## Launch

Run

```python3
python3 main.py
```

to start the simulation.

## Controls

| Key        |                                    |
| ---------- | :--------------------------------: |
| Up/Down    |          Throttle control          |
| Left/Right |       Thrust vector control        |
| Space      |         Start/Stop engine          |
| 0-9        | Switch stability assist mode (SAS) |
| Mouse      |          add an obstacle           |
| P          |               pause                |
| R          |         restart the rocket         |
