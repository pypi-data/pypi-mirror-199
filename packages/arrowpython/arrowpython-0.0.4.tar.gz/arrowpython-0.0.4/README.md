# ArrowPython

A programming language that transpiles to python. It has extremely similar syntax, but instead of colons (`:`),
you use arrows (`=>`). Along with this, you are also able to call functions with only one argument with the following syntax:
```python
function:argument
```
This allows for statements such as this in ArrowPython:
```python
print:"hello"
```
or:
```python
str:1234
```
It allows you to call single-argument functions whilst shortening the time it takes to write them.

To use arrow python, first install it using:
```shell
pip3 install arrowpython
```

Then, to use it in your program, create a new python file and before putting in any code write:
```python
import arrowpython
```

If you are using IDLE, IDLE can often be finicky over syntax errors, as it tries to find then *before* the code is run. This way you will often have a hard time executing ArrowPython in IDLE. I'd reccomend using something like Sublime Text or VSCode.

With that out of the way, this is an example of the popular FizzBuzz program in ArrowPython:
```python
import arrowpython

def fizbuzz:num =>
    for fizzbuzz in range:num =>
        if fizzbuzz % 3 == 0 and fizzbuzz % 5 == 0 =>
            print:"fizzbuzz"
            continue
        elif fizzbuzz % 3 == 0 =>
            print:"fizz"
            continue
        elif fizzbuzz % 5 == 0 =>
            print:"buzz"
            continue
        print:fizzbuzz

fizbuzz:51
```

Have fun coding!