# Dictionary Restructure Tool

## Project

This project implements in Python a function called `restructure()`:

```python
def restructure(data: dict, specification: dict):
	...
```

It is useful to restructure where keys are in a dictionary, for example to
upgrade a configuration file to a new schema.

## Usage

```python
from restructure import restructure
```

For example, to move a nested dictionary to the top-level:

```python
input_data = {
	'key1': {
		'key2': {
			'key3': 'value'
		}
	}
}
specification = {
	'key1.key2.key3': 'key1',
}

output = restructure(data, specification)

assert output == {
	'key1': 'value'
}
```

or the opposite:

```python
input_data = {
	'key1': 'value'
}
specification = {
	'key1': 'key1.key2.key3',
}

output = restructure(input_data, specification)

assert output == {
	'key1': {
		'key2': {
			'key3': 'value'
		}
	}
}
```

Or to swap keys:

```python
input_data = {
	'key1': {
		'key2': 'value1',
	},
	'key3': {
		'key4': 'value2',
	},
}
specification = {
	'key1.key2': 'key3.key4',
	'key3.key4': 'key1.key2',
}

output = restructure(input_data, specification)

assert output == {
	'key1': {
		'key2': 'value2',
	},
	'key3': {
		'key4': 'value1',
	},
}
```

etc.

## For Developers

- Follows [Semantic Versioning 2.0.0](https://semver.org/)
- Follows [this package structure](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

### Testing

To run unit tests, run the following command from the root directory of the project:

```bash
python -m unittest
```
