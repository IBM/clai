#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

# Generic Makefile
#
# Author: Dan FitzGerald

repo=clai
version=TBD
makefile=$(shell utils/getMakeType.sh)

intro:
	@echo "$(repo) v$(version)"
	# TODO: Make this work with USS-style make
	
init-test:
	@make -f $(makefile) init-test
	
clean: intro
	@make -f $(makefile) clean
	
test: intro
	@make -f $(makefile) test
	
dev: intro
	@make -f $(makefile) dev
	
install: intro
	@make -f $(makefile) install

uninstall: intro
	@make -f $(makefile) uninstall

MAKE:
	intro
	install
	
.PHONY: intro init-test clean test dev install uninstall