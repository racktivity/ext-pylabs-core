#!/usr/local/bin/expect --
set timeout -1
spawn passwd
expect "password: "
send "$passwd$\r"
expect "password: "
send "$passwd$\r"