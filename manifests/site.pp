Exec { path => '/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin' }

$inc_file_path = '/vagrant/manifests/files'
$domain_name = 'bakehouse.com'
$user = 'patrick'
$password = 'patrick'
$project = 'frollino'

include apt
include nginx
include uwsgi
include python
include postgresql::server

exec { "apt-update":
    command => "/usr/bin/apt-get update"
}

class user {
    exec { 'add user':
        command => "sudo useradd -m -G sudo -s /bin/bash ${user}",
        unless => "id -u ${user}"
    }

    exec { 'set password':
        command => "echo \"${user}:${password}\" | sudo chpasswd",
        require => Exec['add user']
    }

    # Prepare user's project directories
    file { ["/home/${user}/virtualenvs",
          "/home/${user}/public_html",
          "/home/${user}/public_html/${domain_name}",
          "/home/${user}/public_html/${domain_name}/static"
          ]:
        ensure => directory,
        owner => "${user}",
        group => "${user}",
        require => Exec['add user'],
        before => File['media dir']
    }

    file { 'media dir':
        path => "/home/${user}/public_html/${domain_name}/media",
        ensure => directory,
        owner => "${user}",
        group => 'www-data',
        mode => 0775,
        require => Exec['add user']
    }
}

class apt {
    exec { 'apt-get update':
        timeout => 0
    }

    package { 'python-software-properties':
        ensure => latest,
        require => Exec['apt-get update']
    }

    exec { 'add-apt-repository ppa:nginx/stable':
        require => Package['python-software-properties'],
        before => Exec['last ppa']
    }

    exec { 'last ppa':
        command => 'add-apt-repository ppa:git-core/ppa',
        require => Package['python-software-properties']
    }

    exec { 'apt-get update again':
        command => 'apt-get update',
        timeout => 0,
        require => Exec['last ppa']
    }
}

class nginx {
    package { 'nginx':
        ensure => latest,
        require => Class['apt']
    }

    service { 'nginx':
        ensure => running,
        enable => true,
        require => Package['nginx']
    }

    file { '/etc/nginx/sites-enabled/default':
        ensure => absent,
        require => Package['nginx']
    }

    file { 'sites-available config':
        path => "/etc/nginx/sites-available/${domain_name}",
        ensure => file,
        content => template("${inc_file_path}/nginx/nginx.conf.erb"),
        require => Package['nginx']
    }

    file { "/etc/nginx/sites-enabled/${domain_name}":
        ensure => link,
        target => "/etc/nginx/sites-available/${domain_name}",
        require => File['sites-available config'],
        notify => Service['nginx']
    }
}

class python {
    package { 'curl':
        ensure => latest,
        require => Class['apt']
    }

    package { 'python':
        ensure => '2.7.3*',
        require => Class['apt']
    }

    package { 'python-dev':
        ensure => '2.7.3*',
        require => Class['apt']
    }

    exec { 'install-distribute':
        command => 'curl http://python-distribute.org/distribute_setup.py | python',
        require => Package['python', 'curl']
    }

    exec { 'install-pip':
        command => 'curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python',
        require => Exec['install-distribute']
    }
}

class uwsgi {
    $sock_dir = '/tmp/uwsgi' # Without a trailing slash
    $uwsgi_user = 'www-data'
    $uwsgi_group = 'www-data'

    package { 'uwsgi':
        ensure => latest,
        provider => pip,
        require => Class['python']
    }

    service { 'uwsgi':
        ensure => running,
        enable => true,
        require => File['apps-enabled config']
    }

    # Prepare directories
    file { ['/var/log/uwsgi', '/etc/uwsgi', '/etc/uwsgi/apps-available', '/etc/uwsgi/apps-enabled']:
        ensure => directory,
        require => Package['uwsgi'],
        before => File['apps-available config']
    }

    # Prepare a directory for sock file
    file { [$sock_dir]:
        ensure => directory,
        owner => "${uwsgi_user}",
        require => Package['uwsgi']
    }

    file { '/etc/init/uwsgi.conf':
        ensure => file,
        source => "${inc_file_path}/uwsgi/uwsgi.conf",
        require => Package['uwsgi']
    }

    # Vassals ini file
    file { 'apps-available config':
    path => "/etc/uwsgi/apps-available/${project}.ini",
    ensure => file,
    content => template("${inc_file_path}/uwsgi/uwsgi.ini.erb")
    }

    file { 'apps-enabled config':
        path => "/etc/uwsgi/apps-enabled/${project}.ini",
        ensure => link,
        target => "/etc/uwsgi/apps-available/${project}.ini",
        require => File['apps-available config']
    }
}

class postgresql {
    postgresql::db { 'bakehouse':
        user     => $user,
        password => $password,
    }
}

class virtualenv {
    package { 'virtualenv':
        ensure => latest,
        provider => pip,
        require => Class['python', 'user']
    }

    exec { 'create virtualenv':
        command => "virtualenv ${domain_name}",
        cwd => "/home/${user}/virtualenvs",
        user => $user,
        unless => 'test -d /home/${user}/virtualenvs/${domain_name}',
        require => Package['virtualenv']
    }

    file { "/home/${user}/virtualenvs/${domain_name}/requirements/base.txt":
        ensure => file,
        owner => "${user}",
        group => "${user}",
        mode => 0644,
        source => "${inc_file_path}/virtualenv/requirements/base.txt",
        require => Exec['create virtualenv']
    }
}