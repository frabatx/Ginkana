#!/usr/bin/python3.5
#
# Authors: Francesco Battista
# Group: A1
#
# The program sends, receives and elaborates messages with server
# The entire project is been update in Github at link https://github.com/frabatx/Ginkana.git
# If you want to do the step4 you need root permission with "sudo" word

import a_ginkana_client as a
import b_ginkana_server as b
import c_ginkana_client as c
# import d_ginkana_client_HTTP as d
# import e_ginkana_ping as e


def main():
    server_works_good = False
    while server_works_good is False:
        try:
            code1 = a.init()                # STEP 0
            code2 = b.init(code1)           # STEP 1
            code3 = c.init(code2)           # STEP 2
            # code4 = d.init(code3)         # STEP 3
            # code5 = e.init(code4)         # STEP 4
            server_works_good = True
        except SyntaxError:
            print("Server sent invalid message...")
            print("Try again")


main()
