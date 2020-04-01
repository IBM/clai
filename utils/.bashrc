#!/bin/bash
#
# Licensed Materials - Property of IBM
# 5655-OD1
# COPYRIGHT IBM CORP. 2020
#
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with
# IBM Corp.
#
# .bashrc - Setup your environment for building and testing CLAI on z/OS.
#

# Set aliases
alias whereis="type"
alias tagascii="chtag -t -c iso8859-1"
alias tagebcdic="chtag -t -c IBM-1047"
alias tagascii-all="chtag -t -c iso8859-1 -R *"
alias tagebcdic-all="chtag -t -c IBM-1047 -R *"

# Initial PATH and SHELL
export PATH=/usr/bin:/bin:.:/usr/lpp/cbclib/xlc/bin:/u/sparkdev/dtools
export SHELL=/bin/bash

# Setup the prompt - [current_director]:
export PS1="[\W]: "
