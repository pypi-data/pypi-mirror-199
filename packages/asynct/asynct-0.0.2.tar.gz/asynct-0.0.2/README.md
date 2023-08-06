# Asynct

## Table of Contents

[Overview](#overview)

[Usage](#usage)

## Overview

This package uses threading to create a simple future-like async interface for functions.

## Usage

To make a function async you can use the `make_asynct` decorator:

```python
@make_asynct # Now this function won't block the main thread when ran.
def func(): ...
```

You can then use the result of the function (which is an asynct object) - either asynchronously or synchronously:

```python
func_asynct = func()

@func_asynct.then
def does_something_with_the_result(result): ...

@does_something_with_the_result.then
def does_another_thing_with_the_result(result): ...

# or

result = func_asynct.await_it()
# ...
```
