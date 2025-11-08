#!/bin/bash

executable() {
    for x in /s6/*; do
        [[ -f $x/run ]] && chmod +x $x/run
        [[ -f $x/finish ]] && chmod $x/finish
    done
}

sys_user() {
    #create system user if not exists
    cat /etc/passwd | egrep -w "${username}" >&/dev/null
    if [ $? -ne 0 ]; then
        useradd -MN "${username}"
        usermod -aG sambashare "${username}"
    fi
}
smb_user() {
    #create samba user if not exists
    pdbedit -L | egrep -w "${username}" >&/dev/null
    if [ $? -ne 0 ]; then
        echo -e "${password}\n${password}" | smbpasswd -s -a "${username}"
    fi
}

sys_user
smb_user

executable

exec "$@"
