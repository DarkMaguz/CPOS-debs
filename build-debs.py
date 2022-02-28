#!/bin/python3

import os
import glob

debDirList = ['discord', 'firefox']
baseDir = os.getcwd()
repoBasePath = os.environ.get('REPOSITORY_BASE_PATH')
repoDebPath = os.path.join(repoBasePath, "repo/amd64")

if not repoBasePath:
  raise 'REPOSITORY_BASE_PATH environment variable is not defined'
if not os.path.exists(repoBasePath):
  raise 'REPOSITORY_BASE_PATH environment variable is not a valid path'

updatedDebFiles = []
for debDir in debDirList:
  print('building: ', debDir)
  os.chdir(os.path.join(baseDir, debDir))
  status = os.system('./build-deb.sh')
  debFiles = glob.glob('*.deb')
  for file in debFiles:
    if status == 0:
      os.system('mv %s %s' % (file, repoDebPath))
      updatedDebFiles.append(file)
    else:
      os.remove(file)

if updatedDebFiles:
  os.chdir(repoBasePath)
  status = os.system('./refresh-repo.sh')
