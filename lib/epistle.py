#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import subprocess
from datetime import datetime
import ConfigParser

class Epistle():

  def __init__(self):
    # file system stuff
    self.epistle_dir = os.path.join(os.path.expanduser('~'), ".epistle")
    self.epistle_cfg = os.path.join(self.epistle_dir, "epistle.ini")
    self.epistles_dir = os.path.join(self.epistle_dir, "epistles")
    # read the config
    self.config = ConfigParser.ConfigParser()
    self.config.read(self.epistle_cfg)

  def get_vim(self):
    try:
      return self.config.get("Epistle","Vim")
    except:
      return os.environ.get('EDITOR','vim') # http://stackoverflow.com/questions/6309587/call-up-an-editor-vim-from-a-python-script

  def list_epistles(self):
    epistles = [ f for f in os.listdir(self.epistles_dir) if os.path.isfile(os.path.join(self.epistles_dir,f))]
    for e in epistles:
      print e

  def get_epistle(self,name):
    epistle_path = os.path.join(self.epistles_dir,name)
    if not os.path.isfile(epistle_path):
      os.system("touch %s" % epistle_path)  # make the file
    return epistle_path

  def has_git_remote(self):
    try:
      remote = self.config.get("Git","Remote")
      return (len(remote) > 0)
    except:
      return False

  def git_pull(self):
    os.system("cd %s && git pull" % self.epistles_dir)

  def git_commit(self, epistle):
    deets = (self.epistles_dir, epistle, datetime.now().strftime("%Y%m%d%H%m"))
    os.system("cd %s && git add %s && git commit -m 'date:%s'" % deets)

  def git_push(self):
    os.system("cd %s && git push" % (self.epistles_dir))

  def git_rm(self, epistle):
    deets = (self.epistles_dir, epistle, os.path.basename(epistle))
    os.system("cd %s && git rm %s && git commit -m 'deleted %s'" % deets)
    self.git_push()

  def compose_epistle(self, name):
    
    if self.has_git_remote():
      self.git_pull()

    vim = self.get_vim()
    print "Using vim from: %s" % vim

    epistle = self.get_epistle(name)
    print "Got epistle file: %s" % epistle

    # launch vim and wait for exit code
    subprocess.check_call([vim, epistle])

    # add and commit the changes. 
    self.git_commit(epistle)
    if self.has_git_remote():
      self.git_push()


  def main(self, argv):
    if len(argv) < 2:
      self.print_help()
      return
    arg = argv[1]
    if arg == "-h":
      self.print_help()
    elif arg == "-l":
      self.list_epistles()
    elif arg == "-d":
      self.git_rm(argv[2])
    else:
      self.compose_epistle(arg)

  def print_help(self):
    print """
    Epistle is a tool for taking notes in Vim and saving them using Git.

    Usage:

        $ epistle <something>     -> create or edit a note with this name

        $ epistle -l              -> list available epistles

        $ epistle -d <something>  -> delete an epistle

        $ epistle -h              -> print this help

    See more at http://github.com/msharp/epistle
    """

if __name__ == "__main__":
  e = Epistle()
  e.main(sys.argv)

