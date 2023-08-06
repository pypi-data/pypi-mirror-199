# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 07:56:22 2022

@author: bruno
"""

import main_dp4 as dp4
import sys 


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    print("This is the main routine.")
    print("It should do something interesting.")


    dp4.main()
    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do. Return values are exit codes.


if __name__ == "__main__":
    sys.exit(main())