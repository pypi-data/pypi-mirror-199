# jobject

[![pypi version](https://img.shields.io/pypi/v/jobject.svg)](https://pypi.org/project/jobject) ![MIT License](https://img.shields.io/pypi/l/jobject.svg)

JObject: A dictionary replacement that gives additional access to data using C struct notation, just like JavaScript Objects

## Installation
```bash
pip install jobject
```

## Import
```python
from jobject import JObject

my_dict = JObject({'one': 1, 'two': 2, 'three': 3})

print(my_dict.three) # prints '3'
```

## Inheritance
Because JObject extends dict it can be dropped into any code that requires
dict notation or iteration. Because of this, JObject makes sure any dictionary
instances that are passed to it are also converted into JObjects

```python
from jobject import JObject

my_dict = JObject({
	'one': {
		'two': {
			'three': 123
		}
	}
})

print(my_dict.one.two.three) # prints '123'
```

It will even follow lists to make sure everything under it is converted to a
JObject

```python
from jobject import JObject

my_dict = JObject({
	'array': [
		{'one': 1},
		{'two': 2},
		{'three': 3}
	]
})

print(my_dict[2].three) # prints '3'
```

This even includes data set after the fact

```python
from jobject import JObject

my_dict = JObject()

my_dict.test = {
	'one': [
		{'two': 2}
	]
}

print(my_dict.test.one[0].two) # prints '2'
print(my_dict['test']['one'][0]['two']) # prints '2'
```