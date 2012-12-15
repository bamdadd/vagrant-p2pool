import re
import os
import urllib
from time import sleep
from fabric.api import *
from string import Template

EVENTS_DEST='/usr/share/nginx/events'
EVENTS_BAK='/usr/share/nginx/events_bak'
ASSET_NAME='events'


# eliminate some of the errors that happen with sudo
env.shell = '/bin/sh -c'

#
# Helpers
#
def _revision(segment=''):
  return os.environ.get('GO_PIPELINE_LABEL', 'unversioned')

#
# Environments
#

def vmp2pool():
  """
  Host: Vagrant VM p2pool
  """
  env.hosts = ['127.0.0.1:2022']
  env.disable_known_hosts = True
#
# Methods
#
def clean():
  """
  Clean the output folder.
  """
  local('rm -rf target')

def upload():
  """
  Upload the events and store in /root/deployments folder.
  """
  # Cleanup the tmp folder
  sudo('rm -f /tmp/{0}_*.tar.gz'.format(ASSET_NAME))
  # Upload events using scp
  put('target/{0}_{1}.tar.gz'.format(ASSET_NAME, _revision('fe')), '/tmp')
  # Create deployments folder
  sudo('mkdir -p /root/deployments/')
  sudo('mv /tmp/{0}_{1}.tar.gz /root/deployments'.format(ASSET_NAME, _revision('fe')))

def unpack():
  """
  Unpack the events on the remote server.
  """
  stop()
  sudo('rm -rf {0}'.format(EVENTS_BAK))
  sudo('mv -f {0} {1} || true'.format(EVENTS_DEST, EVENTS_BAK))
  sudo('mkdir --mode=0755 {0}'.format(EVENTS_DEST))
  sudo('tar xzpf /root/deployments/{0}_{1}.tar.gz --owner=events -C {2}'.format(ASSET_NAME, _revision('fe'), EVENTS_DEST))

def stop():
  # sudo('service events stop')
  pass

def run():
  #sudo('service events start')
  pass

def verify():
  # Implement a verification check that the deployment of the events service has been successful
  pass
  

def deploy():
  """
  Deploy the application to the server.
  """
  # Upload from local machine to server
  upload()
  # Unpack on the server
  unpack()
  # Run the app on the server
  run()
  verify()
