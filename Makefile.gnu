#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

# Makefile for GNU-style make
#
# Author: Daniel Nicolas Gisolfi

repo=clai
version=TBD

about:
	@echo "Processing a GNU-style Makefile"
	
init-test:
	@python3 -m pip install -r requirements_test.txt 
	
clean: about
	-rm -f *.pyc *.pyo *.pyd *\$$py.class
	# These two files will be updated by CLAI, we dont want to commit the testing data
	-git checkout anonymize.json
	-git checkout configPlugins.json
	
test: about
ifeq (, $(shell type docker-compose 2> /dev/null))
	$(warning docker-compose not in $(PATH), running tests locally)
	$(MAKE) init-test
	@python3 -m pytest $(PWD)/test
else
	@echo "running tests in a docker container"
	@docker-compose run clai bash -c "cd /clai && make init-test && python3 -m pytest ./test"
endif

dev: about
ifeq (, $(shell type docker-compose 2> /dev/null))
	$(warning docker-compose not in $(PATH), running development script locally)
	@python3 develop.py install --path $(PWD)
else
	@echo "running development script in a docker container"
	@docker-compose run clai bash -c "cd /clai && python3 develop.py install --path /clai && bash"
endif
	
install: about
ifeq ($(shell whoami), root)
	@echo "Installing CLAI as root"
	./install.sh
else
	@echo "You are not running as the superuser, will preform an install local to your user"
	./install.sh --user
endif

uninstall: about
ifeq ($(shell whoami), root)
	@echo "Uninstalling CLAI as root"
	./uninstall.sh
else
	@echo "You are not running as the superuser, will preform an uninstall local to your user"
	./uninstall.sh --user
endif

MAKE:
	intro
	install
	
.PHONY: intro init-test clean test dev install uninstall