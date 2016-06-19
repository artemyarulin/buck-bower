# buck-bower

Set of helpers for Buck build system which allows to install bower dependencies and store it as long as metadata about it

## Why

I have a monorepo and I would like to use bower dependencies in a safe manner. Example could be that I have module `A` which depends on bower lib `B#1`, and I have another library `C` which depends on bower lib `Z#2` which in turn depends on `B#2`. In this case I want to force `B` library to use only one specific version of lib. Browser environment doesn't allow to use multiple versions of the same lib at the same time and I want to have safe environment where I can add `C` as a dependency of `A` without risk of changing behavior.

In short this project allows you to lock all version numbers of bower dependencies. Check Bower [issue #1120](https://github.com/bower/bower/issues/1120) which tracks development of lock file feature

## Example

Considering that I have BUCK file like that:
``` python
bower_dependencies(['purescript-eff#1.0.0',
	                'purescript-prelude#1.0.1'])
```
I can build it and following output will be generated:

``` bash
# ls buck-out/gen/generate_bower_deps/

BUCK
purescript-eff#1.0.0
purescript-prelude#1.0.1

# cat buck-out/gen/generate_bower_deps/BUCK
js_dep('purescript-eff 1.0.0',
       ['purescript-prelude 1.0.1'])
js_dep('purescript-prelude 1.0.1',
       [])
```
Just copy output from this task to your repo and commit. After that you can start referencing those dependencies, here example with [buck-purescript](https://github.com/artemyarulin/buck-purescript/):

``` python
ps_module('hello',
          deps = ['purescript-prelude'])
```

## Installation

Copy RULES folder to the root of your Buck repo. Then in your BUCK files reference it as `include_defs('//RULES/buck-purescript/lib)`. Alternatively use Alternatively use [.buckconfig includes](https://buckbuild.com/concept/buckconfig.html#buildfile.includes)
