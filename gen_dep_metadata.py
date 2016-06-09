"""
For the given bower libraries install it and makes a snapshot of all
installed dependencies with the exact versions in a format that Buck can understand
"""

from tempfile import mkdtemp
from subprocess import check_output
from json import loads

def run(folder,cmd):
    cmd = 'cd {0} && {1}'.format(folder,cmd)
    return check_output(cmd,shell=True)

def find_all_by_key(tree,name):
    return sum(map(lambda d: find_all_by_key(d,name),
                   filter(lambda d: isinstance(d,dict),tree.values())),
               [tree[name]] if name in tree.keys() else [])

def find_all_deps(dTree):
    return map(lambda d: (d['_originalSource'],d['version'],d.get('dependencies',{}).keys()),find_all_by_key(dTree['dependencies'],'pkgMeta'))

def gen_output(deps):
    dDeps = {name:' '.join([name,ver]) for (name,ver,_) in deps}
    return '\n'.join(list(set(map(lambda (name,ver,ddeps): "js_dep('{0} {1}',\n       [{2}])".format(name,
                                                                                                    ver,
                                                                                                    ',\n       '.join("'{0}'".format(d) for d in map(dDeps.get,ddeps))),
                                  deps))))

def gen_metadata(deps):
    folder = mkdtemp()
    # First install all the explicit dependencies with exact version, will throw in case of conflict
    run(folder,'bower install {0}'.format(" ".join(map(lambda d:d.replace(' ','#'),deps))))
    # Collect dependency tree
    return gen_output(find_all_deps(loads(run(folder,'bower list --json --loglevel error'))))
