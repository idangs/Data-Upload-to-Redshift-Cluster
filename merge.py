#!/usr/bin/env python
"""
Combines multiple folders into one folder
Date: 03/09/2019
"""

# Import libraries
import os
import shutil
import sys


reorg_dir = sys.argv[1]
target_dir = sys.argv[2]

for root, dirs, files in os.walk(reorg_dir):
    for name in files:
        subject = root+"/"+name
        n = 1; name_orig = name
        while os.path.exists(target_dir+"/"+name):
            name = "duplicate_"+str(n)+"_"+name_orig; n = n+1
        newfile = target_dir+"/"+name; shutil.move(subject, newfile)