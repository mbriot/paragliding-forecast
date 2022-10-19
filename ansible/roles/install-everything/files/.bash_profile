# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
	. ~/.bashrc
fi

alias ll="ls -larth"
alias ap="ansible-playbook"

# cutomize bash prompt
PS1='\[\033[02;32m\]\u:\[\033[02;32m\]\w\$\[\033[00m\] '

# User specific environment and startup programs

PATH=$PATH:$HOME/.local/bin:$HOME/bin

export PATH