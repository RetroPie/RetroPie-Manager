.PHONY: help install install-dev assets clean delpyc syncf5

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo
	@echo "  clean  -- to clean your local repository from all builded stuff and caches"
	@echo "  delpyc  -- to remove all *.pyc files, this is recursive from the current directory"
	@echo
	@echo "  install -- to build the project"
	@echo "  install-dev -- to build the project for development"
	@echo
	@echo "  assets  -- to build assets for production environment"
	@echo
	@echo "  syncf5 -- to synchronize Foundation5 sources dir to assets (used only when you upgrade Foundation5)"

delpyc:
	find . -name "*\.pyc"|xargs rm -f

clean: delpyc
	rm -Rf bin include lib local node_modules compass/.sass-cache

install:
	virtualenv --no-site-packages --python=/usr/bin/python2.7 .
	bin/python -m pip install -r pip-requirements/basic.txt
	bin/python -m pip install psutil
	bin/python manage.py migrate

install-dev: install
	bundle install --gemfile=compass/Gemfile
	npm install
	foundation new foundation5 --version=5.5.2

assets: 
	grunt uglify
	grunt cssmin

syncf5:
	rm -f foundation5/bower_components/foundation/js/vendor/jquery.js
	cp foundation5/bower_components/jquery/dist/jquery.js foundation5/bower_components/foundation/js/vendor/jquery.js
	rm -Rf project/webapp_statics/js/foundation5
	cp -r foundation5/bower_components/foundation/js project/webapp_statics/js/foundation5
	# Cleaning vendor libs
	rm -Rf project/webapp_statics/js/foundation5/vendor
	mkdir -p project/webapp_statics/js/foundation5/vendor
	# Getting the real sources for updated vendor libs
	cp foundation5/bower_components/fastclick/lib/fastclick.js project/webapp_statics/js/foundation5/vendor/
	cp foundation5/bower_components/foundation/js/vendor/jquery.js project/webapp_statics/js/foundation5/vendor/
	cp foundation5/bower_components/jquery-placeholder/jquery.placeholder.js project/webapp_statics/js/foundation5/vendor/
	cp foundation5/bower_components/jquery.cookie/jquery.cookie.js project/webapp_statics/js/foundation5/vendor/
	cp foundation5/bower_components/modernizr/modernizr.js project/webapp_statics/js/foundation5/vendor/
