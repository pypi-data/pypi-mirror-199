# DictShaper

**The module for convenient viewing of dictionary 
with the all necessary indents.**

This module extends the standard `dict` class, so you can
use all its properties and methods. Over all of this `DictShaper`
adds the new method `shape()`. You can also give a name for your
dictionary by the `name=` param.

`your_dictionary.shape(name='any_name')`

You can also add a path to a file for writing the dictionary there,
using the `write_to=` param. It will be writing in a convenient view,
like in an example below.

`your_dictionary.shape(name='any_name', write_to='any_path')`

If you set as a value `1` or `True` in `write_to=` param then the
dictionary will be writing to the end of a current file.

## EXAMPLES

We will work with the dictionary below called **'some dictionary'**.

`some_dictionary = {'Level-1 el-1': [0, 1, 2, 3, 4], 'Level-1 el-2': {'Level-2 el-1': 1, 'Level-2 el-2': 2}, 'Level-1 el-3': 'Some string', 'Level-1 el-4': ('Tuple', 1, ['a', 'b']), 'Level-1 el-5': {'Level-2 el-3': {'Level-3 el-1': 'https://some-site.com/page1?par=120&another=500', 'Level-3 el-2': (9, 125, 87), 'Level-3 el-3': 'Very very very very very very very very very very long string.'}, 'Level-2 el-4': 2}, 'Level-1 el-6': {}, 'Level-1 el-7': 'The end of the dictionary!'}`

> ### First you need to import this module with the following command
> 
> `from dictshaper.shaper import DictShaper`

## For outputting the dict without a name to a console

### Enter following commands

> 1. `some_dictionary = DictShaper(some_dictionary)`
> 2. 
> 3. `print(some_dictionary.shape())`

* You also can add the *'name='* param

### Output

<p><code>{<br>
&nbsp;&nbsp;&nbsp;&nbsp;'Level-1 el-1': [0, 1, 2, 3, 4],<br>
&nbsp;&nbsp;&nbsp;&nbsp;'Level-1 el-2': {<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'Level-2 el-1': 1,<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'Level-2 el-2': 2,<br>
&nbsp;&nbsp;&nbsp;&nbsp;},<br>
&nbsp;&nbsp;&nbsp;&nbsp;'Level-1 el-3': 'Some string',<br>
&nbsp;&nbsp;&nbsp;&nbsp;'Level-1 el-4': ('Tuple', 1, ['a', 'b']),<br>
&nbsp;&nbsp;&nbsp;&nbsp;'Level-1 el-5': {<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'Level-2 el-3': {<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'Level-3 el-1': 'https://some-site.com/page1?par=120&another=500',<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'Level-3 el-2': (9, 125, 87),<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'Level-3 el-3': 'Very very very very very very very very very very long string.',<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;},<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'Level-2 el-4': 2,<br>
&nbsp;&nbsp;&nbsp;&nbsp;},<br>
&nbsp;&nbsp;&nbsp;&nbsp;'Level-1 el-6': {},<br>
&nbsp;&nbsp;&nbsp;&nbsp;'Level-1 el-7': 'The end of the dictionary!',<br>
}</code></p>

## For writing the dict with a name to a file 

> 1. `some_dictionary = DictShaper(some_dictionary)`
> 2.
> 3. `some_dictionary.shape(name='shaped_dict', write_to=True)`
> 4.
> 5.
> 6.  `shaped_dict = {`
> 7.  &nbsp;&nbsp;&nbsp;&nbsp;`'Level-1 el-1': [0, 1, 2, 3, 4],`
> 8.  &nbsp;&nbsp;&nbsp;&nbsp;`'Level-1 el-2': {`
> 9.  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`'Level-2 el-1': 1,`
> 10. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`'Level-2 el-2': 2,`
> 11. &nbsp;&nbsp;&nbsp;&nbsp;`},`
> 12. &nbsp;&nbsp;&nbsp;&nbsp;`'Level-1 el-3': 'Some string',`
> 13. &nbsp;&nbsp;&nbsp;&nbsp;`'Level-1 el-4': ('Tuple', 1, ['a', 'b']),`
> 14. &nbsp;&nbsp;&nbsp;&nbsp;`'Level-1 el-5': {`
> 15. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`'Level-2 el-3': {`
> 16. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`'Level-3 el-1': 'https://some-site.com/page1?par=120&another=500',`
> 17. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`'Level-3 el-2': (9, 125, 87),`
> 18. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`'Level-3 el-3': 'Very very very very very very very very very very long string.',`
> 19. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`},`
> 20. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`'Level-2 el-4': 2,`
> 21. &nbsp;&nbsp;&nbsp;&nbsp;`},`
> 22. &nbsp;&nbsp;&nbsp;&nbsp;`'Level-1 el-6': {},`
> 23. &nbsp;&nbsp;&nbsp;&nbsp;`'Level-1 el-7': 'The end of the dictionary!',`
> 24. `}`
> 25.