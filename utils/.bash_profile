export PS1='\e[33;1m\u@\h: \e[31m\W\e[0m\$ '
#export PS1='$PWD> '
export TERM=xterm
#export HOME=/Kepler/achicks
alias psx="env COLUMNS=2048 ps -o jobname,xasid,vsz,stime,atime,ppid,pid,pgid,si
d,args=CMD -U $USER | sed 's/ *$//' "
export STEPLIB=ZSPARK.MDS.AZKS.SAZKLOAD
#export _BPXK_AUTOCVT=ON
#export _CEE_RUNOPTS="FILETAG(AUTOCVT,AUTOTAG) POSIX(ON)"
source /Voyager/profiles/.voyager_conf_ah_ptf
#source /Voyager/profiles/.voyager_conf
# ROCKET VIM
export VIM=/var/tools/rocket/bin/vim/share/vim/
export _CEE_RUNOPTS="FILETAG(AUTOCVT,AUTOTAG) POSIX(ON)"
export _BPXK_AUTOCVT=ON
export _TAG_REDIR_ERR=txt
export _TAG_REDIR_IN=txt
export _TAG_REDIR_OUT=txt
export PATH="/Voyager/git/bin/:$PATH"
