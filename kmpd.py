#!/usr/bin/python
#http://kernel.ubuntu.com/~kernel-ppa/mainline/
# Requires: python-bs4
import urlparse
import urllib
import platform
from bs4 import BeautifulSoup
import re

url = "http://kernel.ubuntu.com/~kernel-ppa/mainline/"
source = urllib.urlopen(url).read()
#print(source)

soup = BeautifulSoup(source)
kernels = list()

rel = platform.release().replace("-generic","")
for link in soup.find_all('a'):
    href = link.get('href')
    if re.search("rc\d", href):
        #If release candidate
        continue
    if href[0] == "v":
        kver = href[1:-1] #strip first and last characters
        rel = platform.release().replace("-generic","")
        if kver > rel:
            # If kernel newer than current one
            #print("{0} > {1}".format(kver, rel))
            kernels.append(href)

# SELECT KERNEL
i = 0
for k in kernels:
    i += 1
    print("{0}. {1}".format(i, k))
selk = -1
while not 0 < selk <= len(kernels):
    try:
        selk = int(raw_input("Please enter an integer: "))
    except ValueError:
        continue
print("You chose: {0}".format(kernels[selk-1]))

# SELECT ARCH
i = 0
archs = ("i386", "amd64")
sysarch = platform.machine().replace("x86_64", "amd64")
try:
    defaultarch = archs.index(sysarch)
except:
    defaultarch = 0
for a in archs:
    i += 1
    print("{0}. {1}".format(i, a))
sel = -1
while not 0 < sel <= len(archs):
    try:
        sel = raw_input("Please enter an integer [{0}]: ".format(defaultarch))
        if sel == "":
            sela = defaultarch
            break
        sela = int(sel)
    except ValueError:
        continue
print("You chose: {0}".format(archs[sel-1]))

# SELECT PACKAGES
sel = -1
while True:
    sel = raw_input("Would you like to install kernel headers [Y/n]: ")
    if sel == "":
        selkh = True
        break
    if not sel in tuple("yYnN"):
        continue
    else:
        if sel in tuple("yY"):
            selkh = True
        else:
            selkh = False
        break

sel = -1
while True:
    sel = raw_input("Would you like to install kernel image [Y/n]: ")
    if sel == "":
        selki = True
        break
    if not sel in tuple("yYnN"):
        continue
    else:
        if sel in tuple("yY"):
            selki = True
        else:
            selki = False
        break

sel = -1
while True:
    sel = raw_input("Would you like to install kernel extras [Y/n]: ")
    if sel == "":
        selke = True
        break
    if not sel in tuple("yYnN"):
        continue
    else:
        if sel in tuple("yY"):
            selke = True
        else:
            selke = False
        break

print("Kernel headers: {0}, Kernel image: {1}, Kernel extras: {2}".
        format(selkh, selki, selke))

	#21-Jul-2012 22:49 	5 	 
#[ ]	linux-headers-3.5.0-030500-generic_3.5.0-030500.201207211835_amd64.deb	21-Jul-2012 22:42 	912K	 
#[ ]	linux-headers-3.5.0-030500-generic_3.5.0-030500.201207211835_i386.deb	21-Jul-2012 22:49 	901K	 
#[ ]	linux-headers-3.5.0-030500_3.5.0-030500.201207211835_all.deb	21-Jul-2012 22:35 	12M	 
#[ ]	linux-image-3.5.0-030500-generic_3.5.0-030500.201207211835_amd64.deb	21-Jul-2012 22:42 	12M	 
#[ ]	linux-image-3.5.0-030500-generic_3.5.0-030500.201207211835_i386.deb	21-Jul-2012 22:49 	11M	 
#[ ]	linux-image-extra-3.5.0-030500-generic_3.5.0-030500.201207211835_amd64.deb	21-Jul-2012 22:42 	27M	 
#[ ]	linux-image-extra-3.5.0-030500-generic_3.5.0-030500.201207211835_i386.deb
