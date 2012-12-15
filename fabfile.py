import re
import os
from fabric.api import *
from string import Template
import sys
sys.path.append(os.path.dirname(__file__))
from fabric_html_template import *

TARGET_DIR='pkg'
SITES_DIR='sites'
PUPPET_PACKAGE_NAME='puppetlabs-release-precise.deb'
PUPPET_PACKAGE_URL='http://apt.puppetlabs.com/puppetlabs-release-precise.deb'
RUBYGEM_PKG='rubygems'
RUBY_VERSION='1.9.3-p286'

# eliminate some of the errors that happen with sudo
env.shell = '/bin/sh -c'

def _lines2list(puppet):
  return re.sub(re.compile('^(info|notice|err): (.*)$', re.MULTILINE), r'</pre><li class="\1">\2<pre>', puppet)
  
def _puppet2html(puppet):
  t = Template(html_doc())
  li = _lines2list(puppet)
  # TODO: push host string
  return t.substitute(dict(host=env.host_string, content=li))

def _write_capture(html_capture):
  f = open('{0}.html'.format(env.host_string), 'w')
  f.write(html_capture)
  f.close

def _revision(segment=''):
  revision = os.environ.get('GO_PIPELINE_LABEL', 'dev')
  if ('' != segment):
    exp = r'(?:{0})([\d+\.]+)'.format(segment)
    m = re.search(exp, revision)
    if (m): 
      return m.group(1)
  return revision

def _query_vm(vm_hostname, fact_name):
  result = local('vagrant ssh-config ' + vm_hostname + ' | grep ' + fact_name, capture=True)
  return result.split()[1]

def _query_vm_ssh_key_filename(vm_hostname):
  return _query_vm(vm_hostname, 'IdentityFile')

def _query_vm_ssh_port(vm_hostname):
  return _query_vm(vm_hostname, 'Port')

def _query_vm_host_as_list(vm_hostname):
  return ['{0}:{1}'.format(VAGRANT_HOST, _query_vm_ssh_port(vm_hostname))]

def _configure_fabric_ssh_options_for_vm(vm_hostname):
  env.user = 'vagrant'
  env.hosts = _query_vm_host_as_list(vm_hostname)
  env.key_filename = _query_vm_ssh_key_filename(vm_hostname)
  env.disable_known_hosts = True
  env.reject_unknown_hosts = False

def vmp2pool():
  """
  Host: Vagrant VM Frontend
  """
  global _do_security_update
  _do_security_update = False
  _configure_fabric_ssh_options_for_vm('p2pool')
#
# Methods
#

def install_puppet():
  """
  Install Puppet and Puppet release repo"
  # """
  run('wget -q {0}'.format(PUPPET_PACKAGE_URL))
  sudo('dpkg -i {0}'.format(PUPPET_PACKAGE_NAME))
  sudo('apt-get update -qq')
  sudo('apt-get install -y -q puppet')

def bootstrap():
  """
  Install puppet release repo and puppet.
  """
  install_puppet()

def security_update():
  """
  Apply OS security updates
  """
  print "Applying security updates..."
  sudo('aptitude update')
  sudo('aptitude safe-upgrade -o Aptitude::Delete-Unused=false --assume-yes --target-release `lsb_release -cs`-security')
  print "Security updates installed (if any)"

_do_security_update = True

def upload():
  """
  Upload the assets, unpack puppet to /etc, unpack sites to /tmp/deployment/p2pool/
  """
  # Cleanup the tmp folder
  sudo('rm -f /tmp/puppet-*.tgz')
  # Upload puppet, sites packages
  put('pkg/puppet-{0}.tgz'.format(_revision('cm')), '/tmp')
  sudo('mkdir -p /root/deployments/')

  # Move the files into the deployments folder
  sudo('mv /tmp/puppet-*.tgz /root/deployments')

  # unpack the files
  sudo('rm -rf /etc/puppet_releases/puppet-dev')
  sudo('mkdir -p /etc/puppet_releases')
  sudo('tar xzf /root/deployments/puppet-{0}.tgz -C /etc/puppet_releases'.format(_revision('cm')))
  sudo('rm -rf /etc/puppet')
  sudo('ln -sf /etc/puppet_releases/puppet-{0}/puppet /etc/puppet'.format(_revision('cm')))

def dryrun():
  """
  Upload and dry run the puppet manifests.
  """
  apply(True)

_debug = False

def debug():
  """
  Show debug information
  """
  global _debug
  _debug = True

PUPPET_OK = 0
PUPPET_OK_WITH_CHANGES = 2

def _puppet_sudo(puppet_command_line):
  with settings(warn_only=True):
    result = sudo(puppet_command_line)
  
  if result.return_code == PUPPET_OK or result.return_code == PUPPET_OK_WITH_CHANGES:
    return result

  _write_capture(_puppet2html(result))
  abort('Puppet signified failure exit code: {0}'.format(result.return_code))

def apply(dry_run=''):
  """
  Upload and apply the puppet manifests.
  """
  upload()
  if(dry_run != ''): 
    dry_run = '--noop'
  debug_flags = '--debug --verbose' if _debug else ''
  
  capture = _puppet_sudo("umask 022; puppet apply --detailed-exitcodes {0} --summarize {1} --color=false --show_diff /etc/puppet/manifests/site.pp".format(dry_run, debug_flags))
  
  _write_capture(_puppet2html(capture))
 # if(dry_run != '--noop'): 
 #   if(env.host != "10.9.1.57"):
 #     verify()

