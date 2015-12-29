#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#

from __future__ import print_function
from six.moves  import input           # use raw_input when I say input
from os.path    import expanduser      # Cross-platform home directory finder

import sys

__appname__    = "Example use"
__author__     = "Kevin Cole"
__copyright__  = "Copyright 2015, NOVA Web Development, LLC"
__credits__    = ["Kevin Cole"]  # Authors and bug reporters
__license__    = "GPL"
__version__    = "0.1"
__maintainer__ = "Kevin Cole"
__email__      = "dc.loco@gmail.com"
__status__     = "Prototype"  # "Prototype", "Development" or "Production"
__module__     = ""

from specs import *

if len(sys.argv) == 2:
    fid = sys.argv[1]
else:
    fid = input("Input file [sample_data_2015-12-18.dat]: ")
if not fid:
    fid = "sample_data_2015-12-18.dat"
data = open(fid, "r")

records = []  # A list to hold all records read from data

for lineno, row in enumerate(data):
    try:
        record = fetch(row)     # Parse a row into a record with fields
    except DataError as e:
        prompt = "\nRecord number {0} - {1}\n\nContinue? "
        yorn = input(prompt.format(lineno + 1, e))
        if yorn[0] in ("N", "n"):
            sys.exit(1)                # Exit with extreme prejudice
    record.Last_Name.value   = "Nixon"
    record.First_Name.value  = "Richard"
    record.Student_SSN.value = 111223333
    records.append(record)  # Add to records list
    print(record.Last_Name, record.First_Name, record.Student_SSN)

# The following lets you test it yourself
#

prompt1 = "\nField to change ([ENTER] for next record, QUIT to abort): "
prompt2 = "New value: "
for record in records:
    print("\n{0}".format(record))
    while True:
        field = input(prompt1)
        if field == "":
            break
        elif field == "QUIT":
            sys.exit()
        else:
            value = input(prompt2)
            if field in dir(record):
                eval("record.{0}".format(field)).setval(value)
                print("\n{0}".format(record))
            else:
                print("'{0}' is not a valid field name".format(field))
