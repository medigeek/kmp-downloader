#!/usr/bin/python
# Downloads kernel from http://kernel.ubuntu.com/~kernel-ppa/mainline/
# Requires: python-bs4

# Copyright (c) 2012  Savvas Radevic <vicedar@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import urlparse
import urllib
import os
import urllib2
import platform
from bs4 import BeautifulSoup
import re
import sys
import subprocess
import tempfile
# We need to use apt.VersionCompare(a,b) to compare debian package versions
import apt_pkg

import argparse

# MODULE INIT
apt_pkg.init()

# PARSE ARGUMENTS
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-d', '--disable-filter', action='store_true',
help='Do not filter out release candidate versions')
parser.add_argument('-p', '--prefer-stable', action='store_true',
help='Prefer latest stable version instead of latest release candidate of the same version (e.g. prefer v3.9-raring instead of v3.9-rc8-raring)')
parser.add_argument('-l', '--latest-ver', action='store_true',
help='Chooses last version of each branch')
parser.add_argument('-u', '--update', action='store_true',
help='Upgrade kernel installed')
parser.add_argument('-y', '--daily', action='store_true',
help='Download daily build kernel (with next patches)')
args = parser.parse_args()
print(args)

url = "http://kernel.ubuntu.com/~kernel-ppa/mainline/"
print("Contacting {0}".format(url))
source = urllib.urlopen(url).read()
#print(source)

soup = BeautifulSoup(source, "html.parser")
kernels = list()

rel = re.sub('-\w*', '', platform.release())
print("Current system kernel release version: {0}".format(rel))
release = re.sub('([0-9])\.([0-9]{1,2})\.([0-9]{1,2})','',rel);
previous_href = ""
upgrade = ""
actual_ver = []

if args.update:
	level = 0
	k = 0
	try:
		actual_ver.append("")
		while(True):
			char = rel[k]
			if char == ".":
				level += 1
				actual_ver.append("")
			elif char == "-":
				break
			else:
				actual_ver[level] += str(rel[k])
			k += 1
	except IndexError:
		pass

if args.daily:
    # args.disable_filter = True
    pass

if args.update:
    args.latest_ver = True

selk = -1
for link in soup.find_all('a'):
    href = link.get('href')
    if href[0:5] == "daily" and args.daily:
        kernels.append(str(href)+"current/")
        selk = 0
    elif not args.disable_filter:
		#If filter is not disabled, apply all filters
			if not args.latest_ver:
				selk = 0
				#Original way
				if re.search("rc\d", href):
					#If the version is a release candidate, bypass
					continue
				if href[0] == "v":
					kver = href[1:-1] #strip first and last characters
					vc = apt_pkg.version_compare(kver, rel)
					if vc > 0:
						  # If kernel newer than current one
						  #print("{0} > {1}".format(kver, rel))
						  kernels.append(href)
			else:
				if href[0] == "v":
					level = 0
					k = 1
					version = []
					try:
						version.append("")
						while(True):
							char = href[k]
							if char == ".":
								level += 1
								version.append("")
							elif char == "-":
								break
							else:
								version[level] += str(href[k])
							k += 1
					except IndexError:
						pass
					if not args.update:
						selk = 0
						if int(version[0]) > int(previous_version[0]):
							previous_version[0] = version[0]
							previous_version[1] = -1
							kernels.append(previous_href)
						if int(version[1]) > int(previous_version[1]):
							previous_version[1] = version[1]
							kernels.append(previous_href)
						previous_href = href
					else:
						if int(version[0]) == int(actual_ver[0]) and int(version[1]) == int(actual_ver[1]):
							if int(version[0]) == 2:
								if int(version[2]) == int(actual_ver[2]):
									if int(version[3]) > int(actual_ver[3]):
										selk = href
							else:
								try:
									if int(version[2]) > int(actual_ver[2]):
										kernels = [href]
										selk = 1
								except:
									pass
    else:
        selk = 0
        kernels.append(href)
if previous_href != "":
	kernels.append(previous_href)
if selk == -1:
	print "0 UPDATES"
	print rel
else:

	if not args.update:
		# SELECT KERNEL
		i = 0
		for k in kernels:
		    i += 1
		    print("{0}. {1}".format(i, k))
		selk = -1
		while not 0 < selk <= len(kernels):
		    try:
			defaultk = len(kernels)
			if args.prefer_stable:
			    if re.search('-rc\d+-', kernels[-1]):
				# If a release candidate is the last item in list
				teststable = re.sub("-rc\d+-","-",kernels[-1])
				if teststable in kernels:
				    defaultk = kernels.index(teststable) + 1
			sel = raw_input("Please enter an integer [{0}]: ".format(defaultk))
			if sel == "":
			    selk = defaultk
			    break
			selk = int(sel)
		    except ValueError:
			continue
		print("You chose: {0}".format(kernels[selk-1]))

	else:
		print("You chose: {0}".format(kernels[selk-1]))

	# SELECT ARCH
	i = 0
	archs = ("i386", "amd64")
	sysarch = platform.machine().replace(
	    "x86_64", "amd64").replace("i686", "i386")
	print("Your system architecture: {0}".format(sysarch))
	try:
	    defaultarch = archs.index(sysarch)+1
	except:
	    defaultarch = 1
	for a in archs:
	    i += 1
	    print("{0}. {1}".format(i, a))
	sela = -1
	while not 0 < sela <= len(archs):
	    try:
		sela = raw_input("Please enter an integer [{0}]: ".format(defaultarch))
		if sela == "":
		    sela = defaultarch
		    break
		sela = int(sela)
	    except ValueError:
		continue
	print("You chose: {0}".format(archs[sela-1]))

	# SELECT PACKAGES
	sel1 = -1
	while True:
	    sel1 = raw_input("Would you like to download kernel headers [Y/n]: ")
	    if sel1 == "":
		selkh = True
		break
	    if not sel1 in tuple("yYnN"):
		continue
	    else:
		if sel1 in tuple("yY"):
		    selkh = True
		else:
		    selkh = False
		break

	sel2 = -1
	while True:
	    sel2 = raw_input("Would you like to download kernel image [Y/n]: ")
	    if sel2 == "":
		selki = True
		break
	    if not sel2 in tuple("yYnN"):
		continue
	    else:
		if sel2 in tuple("yY"):
		    selki = True
		else:
		    selki = False
		break

	sel3 = -1
	while True:
	    sel3 = raw_input("Would you like to download kernel extras [Y/n]: ")
	    if sel3 == "":
		selke = True
		break
	    if not sel3 in tuple("yYnN"):
		continue
	    else:
		if sel3 in tuple("yY"):
		    selke = True
		else:
		    selke = False
		break

	print("Kernel headers: {0}, Kernel image: {1}, Kernel extras: {2}".
		format(selkh, selki, selke))

	# selk = selected kernel
	# sela = selected arch
	# selkh = kernel headers? T/F
	# selki = kernel image? T/F
	# selke = kernel extra? T/F
	link = "http://kernel.ubuntu.com/~kernel-ppa/mainline/{0}".format(kernels[selk-1])
	print("Contacting {0}".format(link))
	source = urllib.urlopen(link).read()
	soup = BeautifulSoup(source)
	files = list()
	for l in soup.find_all('a'):
	    href = l.get('href')
	    rxstr = "linux-headers.*_(?:{0}|all)\.deb".format(archs[sela-1])
	    if selkh and re.search(rxstr, href):
		url = "{0}{1}".format(link, href)
		files.append(url)
	    rxstr = "linux-image.*_{0}\.deb".format(archs[sela-1])
	    if selki and re.search(rxstr, href):
		url = "{0}{1}".format(link, href)
		files.append(url)
	    rxstr = "linux-image-extra.*_{0}\.deb".format(archs[sela-1])
	    if selke and re.search(rxstr, href):
		url = "{0}{1}".format(link, href)
		files.append(url)

	#Create temp folder
	tempfolder = tempfile.mkdtemp()
	print("Using temporary folder: {0}".format(tempfolder))

	for url in files:
	    #Change directory to temp folder
	    os.chdir(tempfolder)
	    file_name = url.split('/')[-1]
	    u = urllib2.urlopen(url)
	    f = open(file_name, 'wb')
	    meta = u.info()
	    file_size = int(meta.getheaders("Content-Length")[0])
	    print("Downloading: {0} Bytes: {1}".format(url, file_size))

	    file_size_dl = 0
	    block_sz = 8192
	    while True:
		buffer = u.read(block_sz)
		if not buffer:
		    break

		file_size_dl += len(buffer)
		f.write(buffer)
		p = float(file_size_dl) / file_size
		status = r"{0}  [{1:.2%}]".format(file_size_dl, p)
		status = status + chr(8)*(len(status)+1)
		sys.stdout.write(status)

	    f.close()

	# INSTALL PACKAGES
	sel6 = -1
	while True:
	    sel6 = raw_input("Would you like to install the downloaded packages? [Y/n]: ")
	    if sel6 == "":
		selinst = True
		break
	    if not sel6 in tuple("yYnN"):
		continue
	    else:
		if sel6 in tuple("yY"):
		    selinst = True
		else:
		    selinst = False
		break

	if selinst:
	    print("Installing packages... please type in your password if requested")
	    subprocess.call("sudo dpkg -i {0}/*.deb".format(tempfolder), shell=True)
	else:
	    print("Will not install packages")

raw_input("All done! Press [Enter] key to exit.")
