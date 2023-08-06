#!/usr/bin/env python3
#===============================================================================
# mproposed.py
#===============================================================================

"""Display the proposed memory policy"""




# Imports ----------------------------------------------------------------------

import argparse

import mutil




# Function definitions ---------------------------------------------------------

def main():
    policy = mutil.load_policy(mutil.PROPOSED_POLICY_PATH)
    mutil.print_policy(policy)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=(
            'Display the proposed memory policy'))
    return parser.parse_args()




# Execute ----------------------------------------------------------------------

if __name__ == '__main__':
    parse_arguments()
    main()
