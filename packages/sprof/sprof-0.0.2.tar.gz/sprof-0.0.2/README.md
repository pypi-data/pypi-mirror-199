#sprof

A simple project framework to keep you from getting burned.

sprof is intended to facilitate rapid, reproducible development for small-scale
research projects. It is a work in progress and not yet ready for non-development use.

How it works
------------
sprof requires a fairly specific structure organization in order to eliminate further  boilerplate but, when properly applied, it can save you lots of pain.

An example project directory looks like this:

my_project
-> inputs
--> some_file.csv
-> outputs
-> local.py
-> environment.yml
-> 010_clean_data.py
-> 020_calculate.py
-> 030_visualize.py


Quickstart
---------

Generally sprof is used from the command line.

```bash
sprof create new_project --
```
