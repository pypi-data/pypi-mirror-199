#!/usr/bin/env python3
#===============================================================================
# menact.py
#===============================================================================

"""Enact the proposed memory policy"""




# Imports ----------------------------------------------------------------------

import argparse
import shutil

import mutil




# Functions --------------------------------------------------------------------

def main(args):
    mutil.require_super_user()
    shutil.move(mutil.CURRENT_POLICY_PATH, mutil.PREVIOUS_POLICY_PATH)
    shutil.copy(mutil.PROPOSED_POLICY_PATH, mutil.CURRENT_POLICY_PATH)
    policy = mutil.load_policy(mutil.CURRENT_POLICY_PATH)
    mutil.enact_policy(policy, no_daemon=args.no_daemon)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=('Enact the proposed memory policy'))
    parser.add_argument(
        '--no-daemon', action='store_true',
        help='Don\'t restart the daemon. (This is for use in setup).')
    return parser.parse_args()




# Execute ----------------------------------------------------------------------

if __name__ == '__main__':
    args = parse_arguments()
    main(args)
