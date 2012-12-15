class python {
  package { "python-zope.interface":
     ensure => "installed"
     }

  package { "python-twisted":
     ensure => "installed"
  }  
  package { "python-twisted-web":
     ensure => "installed"
  }
}
