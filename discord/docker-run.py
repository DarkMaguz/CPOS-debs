#!/bin/python3

import os
import pycurl
import certifi
from io import BytesIO
import apt


userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'


def getHeader(url):
  header = BytesIO()
  try:
    curl = pycurl.Curl()
    curl.setopt(curl.USERAGENT, userAgent)
    curl.setopt(curl.URL, url)
    curl.setopt(curl.CAINFO, certifi.where())
    curl.setopt(curl.CONNECTTIMEOUT, 30)
    curl.setopt(curl.NOBODY, True)
    curl.setopt(curl.HEADERFUNCTION, header.write)
    curl.perform()
  except Exception as e:
    print('getHeader() error: %s' % (url, e))
  else:
    return header.getvalue().decode('iso-8859-1')
  finally:
    curl.close()


def getFile(url, fileName):
  responseCode = 0
  try:
    with open(os.path.join(os.getcwd(), fileName), 'wb') as newFile:
      curl = pycurl.Curl()
      curl.setopt(curl.URL, url)
      curl.setopt(curl.USERAGENT, userAgent)
      curl.setopt(curl.WRITEDATA, newFile)
      curl.setopt(curl.CAINFO, certifi.where())
      #curl.setopt(curl.FOLLOWLOCATION, True)
      curl.setopt(curl.TIMEOUT, 300)
      curl.setopt(curl.LOW_SPEED_LIMIT, 5)
      curl.setopt(curl.CONNECTTIMEOUT, 30)
      curl.perform()
      responseCode = curl.getinfo(curl.RESPONSE_CODE)
      curl.close()
  except Exception as e:
    print('getFile() error: %s' % (url, e))
  finally:
    return responseCode


location = getHeader('https://discord.com/api/download?platform=linux&format=deb')
#location = 'location: https://dl.discordapp.net/apps/linux/0.0.17/discord-0.0.17.deb'
discordDebUrl = location.split()[-1]
versionAvailable = discordDebUrl.split('/')[-2]
debFile = discordDebUrl.split('/')[-1]

print('versionAvailable:', versionAvailable)
#print('debFile:', debFile)

# First of all, open the cache
cache = apt.Cache()
# Now, lets update the package list
cache.update()
# We need to re-open the cache because it needs to read the package list
cache.open(None)

currentVersion = ''
try:
  pkg = cache['discord']
  currentVersion = pkg.versions[0].version
except Exception as e:
  pass


print('currentVersion:', currentVersion)
if currentVersion != versionAvailable:
  getFile(discordDebUrl, debFile)
  os.chown(debFile, int(os.environ.get('USERID')), int(os.environ.get('GROUPID')))
