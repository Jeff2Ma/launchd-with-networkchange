#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author: JeffMa

import sys
import os
import time
import subprocess
import getpass


reload(sys)
sys.setdefaultencoding('utf-8')

# current dir
dir_path = os.path.dirname(os.path.abspath(__file__))

def add_to_keychain(username, password):
    p = subprocess.Popen([
        "/usr/bin/security",
        "add-generic-password",
        "-a", username,
        "-s", "launchd with networkchange",
        "-w", password,
        "-T", ""],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.communicate()
    if p.returncode != 0:
        return False
    return True

def delete_from_keychain(username):
    p = subprocess.Popen([
        "/usr/bin/security",
        "delete-generic-password",
        "-a", username,
        "-s", "launchd with networkchange"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.communicate()
    if p.returncode != 0:
        return False
    return True

def script_header():
    print """----------------
launchd with networkchange

see: https://github.com/Jeff2Ma/launchd-with-networkchange for more help.

by JeffMa v1.2
----------------"""

def script_footer():
    print "All done! Please edit the codes in `example.sh` as what you want."

def create_plist_file():
    appscript_file_path = dir_path + '/run.applescript'
    stdout_log = dir_path + '/onnetworkchange.log'
    stderr_log = dir_path + '/onnetworkchange.err.log'
    file_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Label</key>
	<string>com.devework.onnetworkchange</string>
	<key>ProgramArguments</key>
	<array>
		<string>/usr/bin/osascript</string>
		<string>%s</string>
	</array>
    <key>StandardOutPath</key>
    <string>%s</string>  
    <key>StandardErrorPath</key>  
    <string>%s</string>  
	<key>WatchPaths</key>
	<array>
		<string>/Library/Preferences/SystemConfiguration/com.apple.airport.preferences.plist</string>
	</array>
</dict>
</plist>""" % (appscript_file_path, stdout_log, stderr_log)

    with open('com.devework.onnetworkchange.plist', 'w') as f:
        f.write(file_content)

    print "[2] Create `com.devework.onnetworkchange.plist` file with success!"

def create_applescript_file(username):
    file_content ="""# get account password from Keychain
set _username to "%s"
set _password to do shell script "/usr/bin/security find-generic-password -l 'launchd with networkchange' -a " & _username & " -w || echo denied"

# failed to get password
if _password is "denied" then
	display dialog "Failed to get the password from Keychain" buttons {"OK"}
	return
end if

set current_path to (POSIX path of ((path to me as text) & "::"))

on FileExists(theFile) -- (String) as Boolean
	tell application "System Events"
		if exists file theFile then
			return true
		else
			return false
		end if
	end tell
end FileExists

if FileExists(current_path & "/dynamic.sh") then
	set file_path to ("'" & current_path & "/dynamic.sh" & "'")
	do shell script file_path user name _username password _password with administrator privileges
else
	set file_path to ("'" & current_path & "/example.sh" & "'")
	do shell script file_path user name _username password _password with administrator privileges
end if

""" % username

    with open('run.applescript', 'w') as f:
        f.write(file_content)

    print "[3] Create `run.applescript` file with success!"

def ln_s_file():
    plist_file_path = dir_path + "/com.devework.onnetworkchange.plist"
    shell_commend = "ln -s %s ~/Library/LaunchAgents/" % plist_file_path
    p = subprocess.Popen(shell_commend, shell=True, stdout=subprocess.PIPE)
    p.communicate()
    if p.returncode != 0:
        print "Failed to run `ln -s` script!"
    else:
        print "[4] Run `ln -s` script well."

def load_plist():
    shell_commend2 = "launchctl load -w ~/Library/LaunchAgents/com.devework.onnetworkchange.plist"
    p = subprocess.Popen(shell_commend2, shell=True, stdout=subprocess.PIPE)
    p.communicate()
    if p.returncode != 0:
        print "Failed to launchctl load!"
    else:
        print "[5] Launchctl load successfully!"

def unload_plist():
    shell_commend3 = "launchctl unload ~/Library/LaunchAgents/com.devework.onnetworkchange.plist && rm -rf ~/Library/LaunchAgents/com.devework.onnetworkchange.plist"
    p = subprocess.Popen(shell_commend3, shell=True, stdout=subprocess.PIPE)
    p.communicate()
    if p.returncode != 0:
        print "Failed to unload plist!"
    else:
        print "Unload launchctl done."

def main_install():
    script_header()

    user_name = raw_input("Please input your user name: ")
    password = getpass.getpass("Please input your password: ")
    script_one = add_to_keychain(user_name, password)
    if not script_one:
        print "Failed to add account to Keychain, please run this script again."
        delete_from_keychain(user_name)
    else:
        print "[1] Your user name is %s, Your password will be saved to keychain safely." % user_name

    create_plist_file()
    create_applescript_file(user_name)
    ln_s_file()
    load_plist()
    script_footer()

    if len(sys.argv) == 2 and sys.argv[1] == "debug":
        delete_from_keychain(user_name)
        unload_plist()
        print "Debug Mod Done."

def main_uninstall():
    user_name = raw_input("Please input your user name: ")
    script_two = delete_from_keychain(user_name)
    if not script_two:
        print "Some thing wrong when delete account from keychain."
    else:
        print "Deleted account from keychain."
    unload_plist()
    print "All done!"

if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] == "debug":
        main_install()
    elif sys.argv[1] == "uninstall":
        main_uninstall()
