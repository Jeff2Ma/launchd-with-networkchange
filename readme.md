# launchd with networkchange

A tool with shell script and launchd to trigger actions whenever a Mac's network information is changed.

[[简体中文版使用说明] 请点击这里](https://github.com/Jeff2Ma/launchd-with-networkchange/blob/master/readme.zh.md)

## Introduction

This repo is an easy way to deal with contexts like:

> At workplace, your Mac Device has to make some settings such as change proxy address, set specical pac file, open some apps and so on. While at home your have change it again to others.

With the help of [launchd](https://developer.apple.com/library/content/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html), those operations can be automated. And that's what this repo do! It is fast, easy and safe.

## Features

- Easy to install and uninstall.

- Password of your system account will be saved in keychain safely.

- Add example so that your can easily change the code according to your conditions.

## How to start

```bash
$ git clone https://github.com/Jeff2Ma/launchd-with-networkchange

$ cd launchd-with-networkchange

$ python install.py
```
Then input the info when is asked.

![](_screenshots/install.png)

After that, please edit the code in `example.sh ` according to your conditions.

When your Mac's network change, a notification will show when it run shell script with success.

![](_screenshots/notice.png)

## Notices

1) When the first run of the script, system will ask you like:

![](_screenshots/first.png)

Remember to choose `Always Allow`.

2）you can make a  `example.sh` copy one and rename it to `dynamic.sh`,it will be run instead of `example.sh`[see how it work](https://github.com/Jeff2Ma/launchd-with-networkchange/blob/master/_demo/run.applescript#L23-L29).

3) If you want to uninstall it, you can run `python install.py uninstall`.

4) Check `/var/log/system.log` if you are having issues with `plist`.

## Contributing

[Issues](https://github.com/Jeff2Ma/launchd-with-networkchange/issues) and [Pull requests](https://github.com/Jeff2Ma/launchd-with-networkchange/pulls) are welcome.