#!/usr/bin/env python3
#===============================================================================
# mfree.py
#===============================================================================

"""Free up memory in the proposed policy"""




# Imports ----------------------------------------------------------------------

import argparse
import getpass

import mutil




# Functions --------------------------------------------------------------------

def main(args):
    mutil.validate_group(args.group)
    policy = mutil.load_policy(mutil.PROPOSED_POLICY_PATH)
    user = getpass.getuser()
    users = mutil.get_user_set(policy)
    mutil.validate_user(user, users)
    if not (args.group or args.users):
        if user in policy['free']['users']:
            raise Exception('You have no reserved memory to free.')
        mutil.remove_user_from_current_group(user, policy)
        policy['free']['users'].append(user)
    elif args.group and (not args.users):
        try:
            for user in policy[args.group]['users']:
                policy['free']['users'].append(user)
            del policy[args.group]
        except KeyError:
            raise Exception('The specified group does not exist.')
    elif (not args.group) and args.users:
        users = mutil.specified_users(args.users, users)
        for user in users:
            mutil.remove_user_from_current_group(user, policy)
            policy['free']['users'].append(user)
    elif args.group and args.users:
        users = mutil.specified_users(args.users, users)
        for user in users:
            mutil.remove_user_from_current_group(user, policy)
            policy['free']['users'].append(user)
    policy['free']['memory_limit'] = mutil.available_memory(policy)
    policy['shared'] = mutil.shared_memory_in_gigabytes()
    mutil.dump_policy(policy, mutil.PROPOSED_POLICY_PATH)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Free up memory in the proposed policy')
    parser.add_argument(
        '-g', '--group',
        help='group to free memory from')
    parser.add_argument(
        '-u', '--users',
        help='comma-separated list of users to free memory from')
    return parser.parse_args()




#-------------------------------- Execute -------------------------------------#

if __name__ == '__main__':
    args = parse_arguments()
    main(args)
