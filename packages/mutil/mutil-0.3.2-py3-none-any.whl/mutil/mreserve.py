#!/usr/bin/env python3
#===============================================================================
# mreserve.py
#===============================================================================

"""Add a reservation to the proposed memory policy"""




# Imports ----------------------------------------------------------------------

import argparse
import getpass

import mutil




# Functions --------------------------------------------------------------------

def validate_memory_quantity(memory_in_gigabytes):
    if memory_in_gigabytes < 1:
        raise Exception(
            'It doesn\'t make sense to make a reservation with < 1 GB memory. Use '
            'mfree if you need to free up some memory.'
        )


def remove_users_from_current_groups(users, policy):
    for user in users:
        mutil.remove_user_from_current_group(user, policy)


def reserve(memory_in_gigabytes, group, users, policy):
    policy[group] = {'memory_limit': memory_in_gigabytes, 'users': users}


def main(args):
    validate_memory_quantity(args.memory_in_gigabytes)
    mutil.validate_group(args.group)
    policy = mutil.load_policy(mutil.PROPOSED_POLICY_PATH)
    user = getpass.getuser()
    users = mutil.get_user_set(policy)
    mutil.validate_user(user, users)
    if (
        (args.group in users)
        and
        (args.group not in (args.users.split(',') if args.users else {user}))
    ): 
        raise Exception(
            'Better not use a username as a group name unless that user is in '
            'the group.'
        )
    if not (args.group or args.users):
        if user in policy['free']['users']:
            reserve(args.memory_in_gigabytes, user, [user], policy)
            policy['free']['users'].remove(user)
        else:
            for group in (mutil.get_group_set(policy) - {'free'}):
                if user in policy[group]['users']:
                    policy[group]['memory_limit'] = args.memory_in_gigabytes
                    break
    elif args.group and (not args.users):
        try:
            policy[args.group]['memory_limit'] = args.memory_in_gigabytes
        except KeyError:
            remove_users_from_current_groups([user], policy)
            reserve(args.memory_in_gigabytes, args.group, [user], policy)
    elif (not args.group) and args.users:
        users = mutil.specified_users(args.users, users)
        group = '_'.join(users)
        try:
            policy[group]['memory_limit'] = args.memory_in_gigabytes
        except KeyError:
            remove_users_from_current_groups(users, policy)
            reserve(args.memory_in_gigabytes, group, users, policy)
    elif args.group and args.users:
        users = mutil.specified_users(args.users, users)
        try:
            for user in set(policy[args.group]['users']) - set(users):
                policy[args.group]['users'].remove(user)
                policy['free']['users'].append(user)
            for user in set(users) - set(policy[args.group]['users']):
                mutil.remove_user_from_current_group(user, policy)
                policy[args.group]['users'].append(user)
        except KeyError:
            remove_users_from_current_groups(users, policy)
            reserve(args.memory_in_gigabytes, args.group, users, policy)
    policy['free']['memory_limit'] = mutil.available_memory(policy)
    mutil.dump_policy(policy, mutil.PROPOSED_POLICY_PATH)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=(
            'Add a reservation to the proposed memory policy'))
    parser.add_argument(
        'memory_in_gigabytes', type=int)
    parser.add_argument(
        '-g', '--group', help='group name for memory reservation')
    parser.add_argument(
        '-u', '--users',
        help='comma-separated list of usernames for memory reservation')
    return parser.parse_args()




# Execute ----------------------------------------------------------------------

if __name__ == '__main__':
    args = parse_arguments()
    main(args)
