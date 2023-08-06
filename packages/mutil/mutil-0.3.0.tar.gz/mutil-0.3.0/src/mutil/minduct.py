#!/usr/bin/env python3
#===============================================================================
# minduct.py
#===============================================================================

"""Induct a user into the memory policy"""




# Imports ----------------------------------------------------------------------

import argparse
import getpass

import mutil




# Function ---------------------------------------------------------------------

def main(args):
    new_users = set(user for user in args.users.split(','))
    policy = mutil.load_policy(mutil.PROPOSED_POLICY_PATH)
    existing_users = mutil.get_user_set(policy)
    for user in new_users.intersection(existing_users):
        print('{} is already in the memory policy.'.format(user))
    policy['free']['users'].extend(list(new_users - existing_users))
    mutil.dump_policy(policy, mutil.PROPOSED_POLICY_PATH)
    for user in new_users - existing_users:
        print('{} has been inducted into the memory policy.'.format(user))


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=(
            'Induct a new user into the memory policy'))
    parser.add_argument(
        '-u', '--users', default=getpass.getuser(),
        help='comma-separated list of users to induct')
    return parser.parse_args()




# Execute ----------------------------------------------------------------------

if __name__ == '__main__':
    args = parse_arguments()
    main(args)
