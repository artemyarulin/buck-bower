# buck-bower

Set of helpers for Buck build system which allows to install bower dependencies and store it as long as metadata about it

## Why

I would like to use bower dependencies using Buck in my monorepo. I don't want to call `bower install` everytime I build, so I would like to store dependencies in my repo, which will make my builds consistent and fast. This project helps to track bower dependencies and generates `BUCK` file with metadata and fetches actual dependencies.

## Example

Running `gen_dep_metadata.py 'purescript-maybe#1.0.0` will generate following metadata file:

``` python
js_dep('purescript-maybe 1.0.0',
       ['purescript-monoid 1.0.0'])
js_dep('purescript-monoid 1.0.0',
       ['purescript-invariant 1.0.0',
       'purescript-control 1.0.0'])
js_dep('purescript-prelude 1.0.1',
       [])
js_dep('purescript-invariant 1.0.0',
       ['purescript-prelude 1.0.1'])
js_dep('purescript-control 1.0.0',
       ['purescript-prelude 1.0.1'])
```
