#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

# Sample bashrc file for a z/OS USS ID that will run CLAI
#
# Instructions: set the following environment variables as is appropriate for
# your system configuration

# Respect file tags for ASCII/EBCDIC stuff.
export _BPXK_AUTOCVT=ON
export _CEE_RUNOPTS="FILETAG(AUTOCVT,AUTOTAG) POSIX(ON)"

# Specify the name of the TCP/IP stack to be used, as defined in the
# TCPIPJOBNAME statement in the related TCPIP.DATA.
export _BPXK_SETIBMOPT_TRANSPORT=TCP342

# Configure Python
export PYTHON_HOME=/path/to/python
export LIBPATH=$PYTHON_HOME/lib:$LIBPATH
export FFI_LIB=$PYTHON_HOME/lib/ffi
export MANPATH=$PYTHON_HOME/share/man:$MANPATH
export PKG_CONFIG_PATH=$PYTHON_HOME/lib/pkgconfig:$PYTHON_HOME/share/pkgconfig
export CURL_CA_BUNDLE=$PYTHON_HOME/etc/ssl/cacert.pem

# Configure PATH environment variable 
export PATH=$HOME/.local/bin:$PYTHON_HOME/bin:$PATH

# Uncomment the following line to set the TCP/IP port that CLAI uses to some
# value other than the default.  Replace "8xxx" with a unique port number.
#export CLAI_PORT=8xxx

# Uncomment the following line if you want to write CLAI logfile to
# /tmp/USERID instead of the default logfile path
#export CLAI_LOG_FILE="/tmp/$(whoami |  tr '[:upper:]' '[:lower:]').log"
