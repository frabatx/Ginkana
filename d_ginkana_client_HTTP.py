#!/usr/bin/python3.5
'''
CODE = port sent by previouse step
Step 3: HTTP Client
---------------------

- You must download the file
  "http://atclab.esi.uclm.es:5000/CODE".

The file contains the instructions to continue.
You have 6 seconds.

Restrictions:
- It is not allowed to use urllib, urllib2 and urllib3 modules.

'''
import requests as req


# Main function to download file with module requests
# @input: port(string)
# @output: ???
def init(port):
    print("\n------------------STEP 3------------------\n")
    print("Beginning download...")
    url = "http://atclab.esi.uclm.es:5000/{}".format(port)
    r = req.get(url)

    f = open("inst_step4.txt", "w+b")
    f.write(r.content)
    print("Download complete")
    f.close()
    return r.content.decode().partition("\n")[0]
