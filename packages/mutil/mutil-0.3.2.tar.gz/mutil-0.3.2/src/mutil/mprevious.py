#!/usr/bin/env python3
#===============================================================================
# mprevious.py
#===============================================================================

"""Display the previous memory policy"""




# Imports ----------------------------------------------------------------------

import argparse

import mutil




# Functions --------------------------------------------------------------------

def main():
    policy = mutil.load_policy(mutil.PREVIOUS_POLICY_PATH)
    mutil.print_policy(policy)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=(
            'Display the previous memory policy'))
    return parser.parse_args()




# Execute ----------------------------------------------------------------------

if __name__ == '__main__':
    parse_arguments()
    main()
