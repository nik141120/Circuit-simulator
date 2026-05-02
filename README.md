# Circuit-Simulator

A basic RIC (Resistor-Inductor-Capacitor) circuit simulator built in Python.
Inspired by the [Falstad Circuit Simulator](https://www.falstad.com/circuit/),
this project lets the user build simple DC circuits on a grid and solves them
using Kirchhoff's Current and Voltage laws.

## Features

- Drag-and-zoom grid (left click to drag, scroll wheel to zoom)
- Five placeable component types, colour-coded:
  - **Black** — wire
  - **Green** — DC voltage source
  - **Red** — resistor
  - **Yellow** — capacitor
  - **Blue** — inductor
- Live simulation button (top-right)
- Automatic node detection and connection mapping
- Loop-finding algorithm to derive Kirchhoff Voltage Law equations
- Linear-algebra solver for circuit currents and voltages

## How it works

1. The user places components on the grid. Each component is created as an
   instance of a `Component` subclass and stored in `components[]`.
2. Node coordinates and the components attached to each node are recorded in
   `storePointCoordinates` and `storeConnectionsAtPoints`. This data
   directly encodes Kirchhoff's Current Law.
3. `storeConnectionsAtPoints` is simplified into `storeConnectionReference`,
   an adjacency list used by a recursive pathfinding algorithm to discover
   independent voltage loops.
4. Each component contributes a constitutive equation
   (V = 0 for a wire, V = a for a source, V − IR = 0 for a resistor, etc.).
   These are combined with the KCL and KVL equations to form a square linear
   system that is solved each timestep.

## Running the simulator

```bash
python main.py
```

Requires Python 3 with `numpy` and `pygame` (or whichever GUI library
`main.py` imports).

## Current status

This is a working proof-of-concept. The solver runs and returns currents and
voltages to the terminal.

### Known limitations

- Component values (V, R, L, C) are not yet user-editable
- The KVL search can return redundant loops, which can break the linear solve
  on more complex circuits
- Disconnected sub-circuits, or two loops connected through a single node,
  are not currently supported
- Component sprites are orientation-sensitive
- Output is terminal-only — no on-screen voltage/current visualisation yet

## Roadmap

- Filter redundant KVL loops before solving
- User-editable component values
- AC voltage sources
- Diodes, transistors, op-amps
- Voltmeters and ammeters
- On-canvas voltage/current visual aids (in the style of Falstad)
- UI polish