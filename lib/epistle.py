#!/bin/python

import os, sys
import subprocess
import ConfigParser

TEMP_FILE = 'tmp'

class Epistle():

  def __init__(self):
    self.epistle_dir = os.path.join(os.path.expanduser('~'), ".epistle")
    self.epistle_cfg = os.path.join(self.epistle_dir, "epistle.ini")
    self.epistles_dir = os.path.join(self.epistle_dir, "epistles")
    # read the config
    self.config = ConfigParser.ConfigParser()
    self.config.read(self.epistle_cfg)

  def get_vim(self):
    # get vim 
    try:
      return self.config.get("Epistle","Vim")
    except:
      return os.environ.get('EDITOR','vim') # http://stackoverflow.com/questions/6309587/call-up-an-editor-vim-from-a-python-script

  def get_epistle(self,name):
    epistle_path = os.path.join(self.epistles_dir,name)
    if not os.path.isfile(epistle_path):
      # make the file
      os.system("touch %s" % epistle_path)
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
    os.system("cd %s && git add %s && git commit -m 'date:%s'" % (self.epistles_dir,epistle,"TODO:add-datestamp"))

  def git_push(self):
    os.system("cd %s && git push" % (self.epistles_dir))

  def main(self, argv):
    # update git repo (pull)
    if self.has_git_remote():
      self.git_pull()

    vim = self.get_vim()
    print "Using vim from: %s" % vim

    epistle = self.get_epistle(argv[1])
    print "Got epistle file: %s" % epistle

    subprocess.check_call([vim, epistle])
    print "exited with success"
    # add and commit the changes. 
    self.git_commit(epistle)
    if self.has_git_remote():
      self.git_push()


if __name__ == "__main__":
  e = Epistle()
  e.main(sys.argv)

