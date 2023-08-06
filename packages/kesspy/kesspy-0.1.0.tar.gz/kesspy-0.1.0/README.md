# KessPy

- [KessPy](#kesspy)
  - [Installation](#installation)
  - [Getting Started](#getting-started)
  - [Result Data Format](#result-data-format)
  - [Documentation](#documentation)
  - [Testing](#testing)

kesspy is a Python library for simulating explosion and collision events in orbit using the NASA Standard Breakup Model. The breakup model was implemented based on the following works: NASA’s new breakup model of evolve 4.0 (Johnson et al.), and Proper Implementation of the 1998 NASA Breakup Model (Krisko et al.).

## Installation

kesspy runs on Python 3.6 or higher (Python 3.8 is recommended):
Currently the package is available using pip:

```shell
pip install nasa_sbm
```

> _A conda distribution will be made available when the project is stable_

## Getting Started

To use kesspy, you must first create a .yaml file to configure the simulation.
This file has three required fields, the minimum characteristic length, the [simulation type](https://nasa-breakup-model-python.readthedocs.io/en/latest/_autosummary/nasa_sbm.configuration.SimulationType.html),
and the [satellite type](https://nasa-breakup-model-python.readthedocs.io/en/latest/_autosummary/nasa_sbm.configuration.SatType.html)
involved in the fragmentation event.

Secondly, you must provide an implementation of [Satellite](https://nasa-breakup-model-python.readthedocs.io/en/latest/_autosummary/nasa_sbm.satellite.Satellite.html).

Once, you have those two criterion met you can perform the simulation as follows:

```python
from nasa_sbm.configuration import SimulationConfiguration
from nasa_sbm.model import BreakupModel

config = SimulationConfiguration('data/simulation_config.yaml')
event  = BreakupModel(config, np.array([sat]))
debris = event.run()
```

> An example configuration.yaml and Satellite implementation has been provided in `examples`

## Result Data Format

| index | data                       | type                              |
| ----- | -------------------------- | --------------------------------- |
| 0     | SatType (for internal use) | enum                              |
| 1     | position                   | np.array (, 3), containing floats |
| 2     | characteristic length      | float                             |
| 3     | area to mass ratio         | float                             |
| 4     | area                       | float                             |
| 5     | mass                       | float                             |
| 6     | velocity                   | np.array (, 3), containing floats |

> _The returned debris is an (n, 7, 3) numpy array. However, only the position and velocity use the third axis as those quanities are vectors._ >_All other fields have 3 copies of their respective data. This was done as a performance optimization for numpy_

## Documentation

- [Read the Docs](https://kesspy.rtfd.io)

## Testing

```shell
pytest --cov=nasa_sbm tests/
```

```shell
coverage report -m
```
