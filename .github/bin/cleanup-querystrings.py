#!/usr/bin/python3
""" 
Often after performing a wget -p -k http://example.com
The resulting files will include static resources with query strings appended.
For example: 
wp-content/themes/salient/css/fonts/fontawesome-webfont.woff?v=4.2
etc..
This script strips away the query strings so that you can serve the site statically.
This is the first step in porting a theme from another CMS to a Diazo based Plone theme
"""
import os

# change directory to dist
os.chdir("dist")

for root, dirs, files in os.walk("."):
    for file in files:
        if '?' in file:
            newname = file.split('?')[0]
            oldpath = root + os.sep + file
            newpath = root + os.sep + newname
            if os.path.isfile(newpath):
                os.remove(oldpath)
            else:
                os.rename(oldpath,newpath)
