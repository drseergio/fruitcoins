# -*- coding: utf-8 -*-
from fabric.api import *

PRODUCTION = 'asparagus.thecurious.me'
STAGING = 'washington-wlan.bethania'
DOGFOOD = 'carolina-wlan.bethania'
SENCHA = '/opt/SenchaSDKTools-1.2.3'

def production():
  env.hosts = [ PRODUCTION ]
  env.repo = 'moneypit'
  env.settings = 'production_settings.py'
  env.parent = 'origin'
  env.branch = 'master'
  env.home = '/home/drseergio'
  env.www = '/var/www/moneypit'


def staging():
  env.hosts = [ STAGING ]
  env.repo = 'moneypit'
  env.settings = 'staging_settings.py'
  env.parent = 'origin'
  env.branch = 'master'
  env.home = '/home/drseergio'
  env.www = '/var/www/moneypit'


def dogfood():
  env.hosts = [ DOGFOOD ]
  env.repo = 'moneypit'
  env.settings = 'dogfood_settings.py'
  env.parent = 'origin'
  env.branch = 'master'
  env.home = '/home/drseergio'
  env.www = '/var/www/moneypit'


def makecss():
  local('git rm -f core/static/resources/images/icons-*png;'
        'cd core/static/resources/sass;'
        'compass compile moneypit.scss;'
        'cd -;'
        'sed -i -e \'s:/\.\.:..:g\' -e \'s/background-position:0 -[0-9]*px/& !important/ig\' core/static/resources/css/moneypit.css;'
        'git add core/static/resources/images/icons-*png;')

def makejs():
  local('cd core/static;'
        'PATH="${PATH}:%(SENCHA)s/appbuilder/:%(SENCHA)s/command:%(SENCHA)s" sencha create jsb -a build.html -p app.jsb3;'
        'PATH="${PATH}:%(SENCHA)s/appbuilder/:%(SENCHA)s/jsbuilder:%(SENCHA)s/command:%(SENCHA)s" sencha build -p app.jsb3 -d .' % {'SENCHA': SENCHA})


def publishcode():
  local('mkdir -p fruitcoins-code/desktop;mkdir -p fruitcoins-code/mobile;'
        'cp -R core/static/app-js/ fruitcoins-code/dekstop;'
        'cp -R core/static/js-extra/ fruitcoins-code/dekstop;'
        'cp -R core/static/app.js fruitcoins-code/desktop;'
        'cp -R mobile/static/mobile-js/ fruitcoins-code/mobile/;'
        'zip -r fruitcoins-code fruitcoins-code;'
        'rm -rf fruitcoins-code/;')
  local('scp fruitcoins-code.zip blog.fruitcoins.com:/var/www/localhost/htdocs/')
  local('rm -f fruitcoins-code.zip')


def pushpull():
  local('git push production') 
  local('cd core/static;'
        'PATH="${PATH}:%(SENCHA)s/appbuilder/:%(SENCHA)s/command:%(SENCHA)s" sencha create jsb -a build.html -p app.jsb3;'
        'PATH="${PATH}:%(SENCHA)s/appbuilder/:%(SENCHA)s/jsbuilder:%(SENCHA)s/command:%(SENCHA)s" sencha build -p app.jsb3 -d .' % {'SENCHA': SENCHA})
  put('./core/static/app-all.js', '%(home)s/git/%(repo)s/www/core/static/app-all.js' % env)
  local('cd mobile/static;cat build|xargs cat>app-all.js;java -jar %(SENCHA)s/jsbuilder/ycompressor/ycompressor.jar app-all.js -o app-all-compressed.js' % {'SENCHA': SENCHA})
  put('./mobile/static/app-all-compressed.js', '%(home)s/git/%(repo)s/www/mobile/static/mobile-js/app-all.js' % env)
  local('#Running API tests')
  local('python manage.py test api')
  run('cd %(home)s/git/%(repo)s/; git pull %(parent)s %(branch)s;'
      'sudo rm -rf %(www)s;'
      'sudo cp -R %(home)s/git/%(repo)s/www %(www)s;'
      'sudo cp www/%(settings)s %(www)s/local_settings.py;'
      'cd %(www)s;'
      'sudo rm -rf .git;'
      'sudo cp -R mobile/static/mobile-js core/static;'
      'sudo cp -R mobile/static/touch core/static;'
      'sudo chown -R nginx:nginx %(www)s;'
      'python manage.py syncdb;'
      'sudo /etc/init.d/uwsgi.moneypit reload' % env)
  local('cd core/static;rm app-all.js all-classes.js app.jsb3')
  local('cd mobile/static;rm app-all.js app-all-compressed.js')


def reload():
  run('/etc/init.d/nginx reload;'
      '/etc/init.d/uwsgi.moneypit reload')
