#!/bin/bash

executable() {
    for x in /s6/*; do
        [[ -f $x/run ]] && chmod +x $x/run
        [[ -f $x/finish ]] && chmod $x/finish
    done
}

executable

exec "$@"
