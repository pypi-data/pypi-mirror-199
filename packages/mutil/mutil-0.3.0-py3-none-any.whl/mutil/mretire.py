#!/usr/bin/env python3
#===============================================================================
# mretire.py
#===============================================================================

"""Retire a user from the memory policy"""




# Imports ----------------------------------------------------------------------

import argparse
import getpass

import mutil




# Function definitions ---------------------------------------------------------

def main(args):
    users_to_retire = set(user for user in args.users.split(','))
    if getpass.getuser() in users_to_retire:
        raise Exception("You can't retire yourself")
    policy = mutil.load_policy(mutil.PROPOSED_POLICY_PATH)
    existing_users = mutil.get_user_set(policy)
    for user in users_to_retire - existing_users:
        print('{} is not in the memory policy.'.format(user))
    for user in users_to_retire.intersection(existing_users):
        mutil.remove_user_from_current_group(user, policy)
        print('{} has been retired from the memory policy.'.format(user))
    mutil.dump_policy(policy, mutil.PROPOSED_POLICY_PATH)


# Parse arguments
def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Retire a user from the memory policy')
    parser.add_argument(
        '-u', '--users', default=getpass.getuser(), required=True,
        help='comma-separated list of users to retire')
    return parser.parse_args()




# Execute ----------------------------------------------------------------------

if __name__ == '__main__':
    args = parse_arguments()
    main(args)
