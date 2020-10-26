#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

# Sample bash profile for a z/OS USS ID that will run CLAI
#
# Instructions: Uncomment the `export SHELL` statement that is appropriate for
# your system configuration

export SHELL=/bin/bash
#export SHELL=/local/bash
#export SHELL=/Voyager/anaconda/bin/bash
#export SHELL=/usr/lpp/IBM/izoda/anaconda/bin/bash
exec $SHELL --login