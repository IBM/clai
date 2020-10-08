#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

# Generic Makefile
#
# Author: Dan FitzGerald

repo=`echo "clai/__version__.py __title__" | utils/getVersionInfo.sh`
version=`echo "clai/__version__.py __version__" | utils/getVersionInfo.sh`
make_cmd=`ps -o comm | grep make`
makefile=`ps -o comm | grep make | utils/getMakeType.sh`

intro:
	@echo "$(repo) v$(version)"
	
init-test:
	@$(make_cmd) -f $(makefile) init-test
	
clean: intro
	@$(make_cmd) -f $(makefile) clean
	
test: intro
	@$(make_cmd) -f $(makefile) test
	
dev: intro
	@$(make_cmd) -f $(makefile) dev
	
install: intro
	@$(make_cmd) -f $(makefile) install

uninstall: intro
	@$(make_cmd) -f $(makefile) uninstall

MAKE:
	intro
	install
	
.PHONY: intro init-test clean test dev install uninstall