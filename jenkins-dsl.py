#!/usr/bin/python
import yaml

def getDownstream(name, clist):
  ret = []
  for n in clist:
    if name['name'] in n['deps']:
      ret.append(n['name'])
  return ret 

yf = open('ci.yaml', 'r')

xx = yaml.load(yf)

f = open('jobs.dsl', 'w')

for x in xx:
  print >> f, 'job(\'{0}\') {'.format(x['name'])
  print >> f, '  using \'package_template\''
  print >> f, '  disabled(false)'
  print >> f, '  scm {'
  print >> f, '    git {'
  print >> f, '      remote {'
  print >> f, '        github(\'{0}\')'.format(x['url'])
  print >> f, '      }' # remote
  print >> f, '      branch(\'{0}\')'.format(x['branch'])
  print >> f, '      relativeTargetDir(\'src\')'
  print >> f, '      wipeOutWorkspace(true)'
  print >> f, '    }' # git
  print >> f, '  }' # scm
  print >> f, '  environmentVariables {'
  print >> f, '    env(\'DEPS\', \'{0}\')'.format(' '.join(x['deps']))
  print >> f, '  }' # environmentVariables
  print >> f, '  triggers {'
  if (x['external']):
    print >> f, '    scm(\'H */4 * * *\')'
  else:
    print >> f, '    githubPush()'
  print >> f, '  }' # triggers
  print >> f, '  publishers {'
  for n in getDownstream(x, xx):
    print >> f, '  downstream(\'{0}\', \'UNSTABLE\')'.format(n)
  print >> f, '  }' # publishers
  print >> f, '}' # job
  
  if (not x['external']):
    print >> f, 'job {'
    print >> f, '  using \'package_pull_template\''
    print >> f, '  name \'{0}_pullrequest\''.format(x['name'])
    print >> f, '  disabled(false)'
    print >> f, '  scm {'
    print >> f, '    git {'
    print >> f, '      remote {'
    print >> f, '        github(\'{0}\')'.format(x['url'])
    print >> f, '        refspec(\'+refs/pull/*:refs/remotes/origin/pr/*\')'
    print >> f, '      }' # remote
    print >> f, '      branch(\'${sha1}\')'
    print >> f, '      relativeTargetDir(\'src\')'
    print >> f, '      wipeOutWorkspace(true)'
    print >> f, '    }' # git
    print >> f, '  }' # scm
    print >> f, '  environmentVariables {'
    print >> f, '    env(\'DEPS\', \'{0}\')'.format(' '.join(x['deps']))
    print >> f, '  }' # environmentVariables
    print >> f, '}' # job
  
