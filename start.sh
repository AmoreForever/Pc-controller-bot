#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

banner() {
	clear
	clear
	printf  "\n\n\033[0;35m█▀▀ █▀█ █▄ █ ▀█▀ █▀█ █▀█ █   █   █▀▀ █▀█\n"
    printf  "\033[0;35m█▄▄ █▄█ █ ▀█  █  █▀▄ █▄█ █▄▄ █▄▄ ██▄ █▀▄"
    printf  "\n\n\033[0;34mBot going to start\n\n"
}

banner


printf '\033[0;31m'
python3 main.py
