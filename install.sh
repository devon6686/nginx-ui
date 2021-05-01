#!/bin/bash

# Set Colors

bold=$(tput bold)
underline=$(tput sgr 0 1)
reset=$(tput sgr0)

red=$(tput setaf 1)
green=$(tput setaf 76)
white=$(tput setaf 7)
tan=$(tput setaf 202)
blue=$(tput setaf 25)

# Headers and Logging

underline() { printf "${underline}${bold}%s${reset}\n" "$@"
}
h1() { printf "\n${underline}${bold}${blue}%s${reset}\n" "$@"
}
h2() { printf "\n${underline}${bold}${white}%s${reset}\n" "$@"
}
debug() { printf "${white}%s${reset}\n" "$@"
}
info() { printf "${white}➜ %s${reset}\n" "$@"
}
success() { printf "${green}✔ %s${reset}\n" "$@"
}
error() { printf "${red}✖ %s${reset}\n" "$@"
}
warn() { printf "${tan}➜ %s${reset}\n" "$@"
}
bold() { printf "${bold}%s${reset}\n" "$@"
}
note() { printf "\n${underline}${bold}${blue}Note:${reset} ${blue}%s${reset}\n" "$@"
}

info "step1: install python3"
yum -y install python3 python3-pip python3-devel

if [ $? -eq 0 ];then
    success "succeed to install python3 and pip3"
else
    { error "failed to yum install python3 and pip3"; exit 1; }
fi

info "step2: install python3 module"
if which pip3 &> /dev/null;then
    info "command pip3 find"
else
    { error "failed to find command: pip3"; exit 1; }
fi


pip3 install -r requirements.txt
if [ $? -eq 0 ];then
   success "succeed to install python3 module"
else
   { error "failed to install python3 module"; exit 1; }
fi

h2 "Remember modify NGINX_PATH in config.py!"
