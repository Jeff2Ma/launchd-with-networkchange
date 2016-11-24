# get account password from Keychain
set _username to "JeffMa"
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

