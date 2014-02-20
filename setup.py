#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import subprocess
from lib.epistle import Epistle 

def get_pyscript_path():
  this_dir = os.path.dirname(os.path.realpath(__file__))
  return os.path.join(this_dir,"lib","epistle.py")

def get_vim_path():
  v = subprocess.check_output(['which vim'], shell=True)
  return v.strip()

def parse_gist_url(gist):
  # https://gist.github.com/2fcae0fc9df815f82567.git
  # git@github.com:2fcae0fc9df815f82567.git
  url = re.sub('https://gist\.github\.com/','git@github.com:', gist)
  return url

# the module
e = Epistle()

# create dir: ~/.epistle
print "Creating directory %s" % e.epistle_dir
os.system("mkdir %s" % e.epistle_dir)

# create file: ~/.epistle/epistle.cfg
print "Creating config file %s" % e.epistle_cfg
os.system("touch %s" % e.epistle_cfg)
e.read_config() # load the config file

# get input => git repo (gist)
git_repo = parse_gist_url(raw_input("Enter your git (or gist) clone URL: "))

# checkout the repo to: ~/.epistle/epistles
if len(git_repo) > 0:
  print "Cloning %s into %s" % (git_repo, e.epistles_dir)
  os.system("cd %s && git clone %s %s" % (e.epistle_dir, git_repo, e.epistles_dir))
  e.config.add_section("Git")
  e.config.set("Git", "Remote", git_repo)
else:
  print "Creating empty git repo"
  os.system("mkdir %s && cd %s && git init" % (e.epistles_dir,e.epistles_dir))

# symlink the script
print "Creating symbolic link"
os.system("ln -s %s /usr/local/bin/epistle" % get_pyscript_path())

# chmod the script
os.system("chmod +x %s" % get_pyscript_path())

vim_path = get_vim_path()
print "Using vim path %s" % vim_path
e.config.add_section("Epistle")
e.config.set("Epistle", "Vim", vim_path)
print "To change your vim path, edit %s" % e.epistle_cfg

# write the config file
with open(e.epistle_cfg, 'w') as configfile:
  e.config.write(configfile)


