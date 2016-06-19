#!/usr/bin/env python

# For the given bower libraries install it and makes a snapshot of all
# installed dependencies with the exact versions in a format that Buck can understand

# If package was renamed then pkgMeta.name would have a new name,
# while pkgMeta._originalSource would have a previous name. Folder in bower_components
# would be named using original name

from tempfile import mkdtemp
from subprocess import check_output
from json import loads
from sys import argv

def run(cmd,ignoreErrors=False):
    try:
        return check_output(cmd,shell=True)
    except:
        if not ignoreErrors:
            raise

def find_all_by_key(tree,name):
    return sum(map(lambda d: find_all_by_key(d,name),
                   filter(lambda d: isinstance(d,dict),tree.values())),
               [tree[name]] if name in tree.keys() else [])


def find_all_deps(dTree):
    def process_dep(acc,cur):
        source,name,ver,deps = cur['_originalSource'],cur['name'],cur['version'],cur.get('dependencies',{}).keys()
        if (source != name):
            acc[source] = (ver,[name])
        acc[name] = (ver,deps)
        return acc
    return reduce(process_dep,
                  find_all_by_key(dTree['dependencies'],'pkgMeta'),
                  {})

def sort_folders(deps):
    map(lambda (name,(ver,deps)): run("mv 'bower_components/{0}' '{1}'".format(name,'#'.join([name,ver])),True),
        deps.iteritems())
    run('rm -rf bower_components')

def gen_output(deps):
    dDeps = {name:' '.join([name,ver]) for (name,(ver,_)) in deps.iteritems()}
    return '\n'.join(map(lambda (name,(ver,ddeps)): "js_dep('{0} {1}',\n       [{2}])".format(name,
                                                                                                ver,
                                                                                                ',\n       '.join("'{0}'".format(d) for d in map(dDeps.get,ddeps))),
                         sorted(deps.iteritems())))



def gen_metadata(deps):
    run('bower install --force-latest {0}'.format(" ".join(map(lambda d: d.replace(' ','#'),deps))))
    dTree = find_all_deps(loads(run('bower list --json --loglevel error')))
    sort_folders(dTree)
    return gen_output(dTree)

if (__name__ == "__main__"):
    print(gen_metadata(argv[1:]))
