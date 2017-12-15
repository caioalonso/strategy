#!/usr/bin/env python
# Will add milliseconds to timestamps that don't have them
# eg:
# 2017-11-01 00:10:03
# to
# 2017-11-01 00:10:03.000000
import sys
import re
import os
csv = open(sys.argv[1], 'r')
out = open('tempfile', 'w')
out.write(re.sub(r':(\d{2}),', r':\g<1>.000000,', csv.read()))
csv.close()
out.close()
os.rename('tempfile', sys.argv[1])
