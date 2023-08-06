README
######

**NAME**

|
| ``opv`` - object programming version
|

**SYNOPSIS**


The ``opv`` package provides an Object class, that allows for save/load to/from
json files on disk. Objects can be searched with database functions and have a 
type in filename for reconstruction. Methods are factored out into functions to
have a clean namespace to read JSON data into.

This package should result in a Queue derived (or compatible) class that can
keep objects in sync on a multiprocessor environment.

|

**INSTALL**

|
| ``python3 -m pip install opv``
|

**PROGRAMMING**

basic usage is this::

 >>> import opv
 >>> o = opv.Object()
 >>> o.key = "value"
 >>> o.key
 >>> 'value'

Objects try to mimic a dictionary while trying to be an object with normal
attribute access as well. hidden methods are provided, the methods are
factored out into functions like get, items, keys, register, set, update
and values.

load/save from/to disk::

 >>> from opv import Object, load, save
 >>> o = Object()
 >>> o.key = "value"
 >>> p = save(o)
 >>> obj = Object()
 >>> load(obj, p)
 >>> obj.key
 >>> 'value'

great for giving objects peristence by having their state stored in files::

 >>> from opv import Object, save
 >>> o = Object()
 >>> save(o)
 'opv.objects.Object/2021-08-31/15:31:05.717063'

|

**AUTHOR**

|
| B.H.J. Thate <operbot100@gmail.com>
|

**COPYRIGHT**

|
| ``opv`` is placed in the Public Domain.
|
