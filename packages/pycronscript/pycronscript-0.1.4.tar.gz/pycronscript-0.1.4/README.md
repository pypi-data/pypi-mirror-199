# pycronscript
Schedule your Python scripts.

## Getting started
**Install package**

`pip install pycronscript`

**Create config file**

This is created with the first run of `pycronscript` and you can see the path where it is has been created.

**Register your scripts for the scheduled run in config file**
```
[custom_name]
path=/home/my_user/foo/bar/my_script.py
each={'minutes': 5} # datetime.timedelta args, but in dict format. Default=1h.
...
```
**Start**

Run again `pycronscript`
