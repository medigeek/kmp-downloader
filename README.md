Kernel mainline ppa downloader
=====

Requirements
----

`python3-bs4` (beautiful soup)
`python3-apt`

```sh
sudo apt install python3-bs4 python3-apt
```

Instructions
----

You may download it using this quick link: https://github.com/medigeek/kmp-downloader/tarball/master

Save the archive and extract the files. Double click on `kmpd.py` (execute in terminal). If you're not sure about an option, press Enter and it will select the default answer.

..or execute this command (one-liner):

```sh
cd /tmp; rm -rf medigeek-kmp*; \
    wget --no-check-certificate https://github.com/medigeek/kmp-downloader/tarball/master -O kmpd.tar.gz; \
    tar xzf kmpd.tar.gz; cd medigeek-*; \
    python kmpd.py
```

If you want more options, e.g. disable the release candidate filter and/or prefer the latest stable release, check out the available arguments:

```sh
python3 kmpd.py --help
```

Uninstall
----
To uninstall the kernel packages, remember to boot to a different kernel image first. Then you can use your favourite package manager to uninstall the packages. For example if you installed version 5.10.4, you can uninstall it using this command:

```sh
sudo apt-get purge linux-.*-5\.10\.4
```

More info
----
Ubuntu-gr forum topic: http://forum.ubuntu-gr.org/viewtopic.php?f=6&t=24119

