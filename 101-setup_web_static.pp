# Puppet manifest to set up web servers for web_static deployment

class setup_web_static {
  package { 'nginx':
    ensure => installed,
  }

  file { '/data':
    ensure => 'directory',
    owner  => 'ubuntu',
    group  => 'ubuntu',
  }

  file { '/data/web_static':
    ensure => 'directory',
    owner  => 'ubuntu',
    group  => 'ubuntu',
  }

  file { '/data/web_static/releases':
    ensure => 'directory',
    owner  => 'ubuntu',
    group  => 'ubuntu',
  }

  file { '/data/web_static/shared':
    ensure => 'directory',
    owner  => 'ubuntu',
    group  => 'ubuntu',
  }

  file { '/data/web_static/releases/test':
    ensure => 'directory',
    owner  => 'ubuntu',
    group  => 'ubuntu',
  }

  file { '/data/web_static/releases/test/index.html':
    ensure  => 'file',
    content => '<html><head></head><body>Holberton School</body></html>',
    owner   => 'ubuntu',
    group   => 'ubuntu',
  }

  file { '/data/web_static/current':
    ensure  => 'link',
    target  => '/data/web_static/releases/test',
    owner   => 'ubuntu',
    group   => 'ubuntu',
  }

  file { '/etc/nginx/sites-available/default':
    ensure  => 'file',
    content => "location /hbnb_static {\n\talias /data/web_static/current/;\n\tindex index.html;\n}",
    notify  => Service['nginx'],
  }

  service { 'nginx':
    ensure  => 'running',
    enable  => true,
    require => File['/etc/nginx/sites-available/default'],
  }
}

include setup_web_static
