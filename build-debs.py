#!/bin/python3

import os

debsList = ['discord', 'firefox']
baseDir = os.getcwd()
deployPath = os.environ.get('DEB_DEPLOY_PATH')

if not deployPath:
  raise 'DEB_DEPLOY_PATH environment variable is not defined'
if not os.path.exists(deployPath):
  raise 'DEB_DEPLOY_PATH environment variable is not a valid path'

for deb in debsList:
  print('building:', deb)
  os.chdir(os.path.join(baseDir, deb))
  status = os.system('./build-deb.sh')
  if status == 0:
    os.system('mv *.deb %s' % deployPath)
