cygwin prompt coloring
```console
export PS1="\[\033[36m\]\u\[\033[m\]@\[\033[32m\]\h:\[\033[33;1m\]\W\[\033[m\]\$ "
export CLICOLOR=1

alias ls="ls --color=auto"
LS_COLORS=$LS_COLORS':no=00'
LS_COLORS=$LS_COLORS':di=36;01'
LS_COLORS=$LS_COLORS':tw=33;01'
LS_COLORS=$LS_COLORS':ow=33;01'
LS_COLORS=$LS_COLORS':fi=93'
LS_COLORS=$LS_COLORS':ln=00'
LS_COLORS=$LS_COLORS':pi=00'
LS_COLORS=$LS_COLORS':so=00'
LS_COLORS=$LS_COLORS':ex=00'
LS_COLORS=$LS_COLORS':bd=00'
LS_COLORS=$LS_COLORS':cd=00'
LS_COLORS=$LS_COLORS':or=00'
LS_COLORS=$LS_COLORS':mi=00'
LS_COLORS=$LS_COLORS':*.sh=31'
LS_COLORS=$LS_COLORS':*.sh=31'
LS_COLORS=$LS_COLORS':*.exe=31'
LS_COLORS=$LS_COLORS':*.bat=31'
LS_COLORS=$LS_COLORS':*.com=31'
export LS_COLORS

```