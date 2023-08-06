#!/usr/bin/env python3
#===============================================================================
# musage.py
#===============================================================================

"""Display current memory usage"""




# Imports ----------------------------------------------------------------------

import argparse
import getpass

import mutil





# Functions --------------------------------------------------------------------

def print_with_highlighting(obj):
    print(obj)


def stringify_usage(converted_usage, kilobytes=False, megabytes=False):
    return '{}{}'.format(
        converted_usage,
        ('KB' * kilobytes + 'MB' * megabytes) if kilobytes or megabytes
        else 'GB'
    )


def display_usage_for_a_user(user, kilobytes=False, megabytes=False):
    usage = mutil.get_usage_for_a_user(user)
    print_with_highlighting(
        '{}: {}'.format(
            user,
            stringify_usage(
                mutil.convert_usage(
                    usage, kilobytes=kilobytes, megabytes=megabytes
                ),
                kilobytes=kilobytes, megabytes=megabytes
            )
        ),
        memory_usage_gb=mutil.convert_usage(usage)
    )


def display_usage_for_a_group(policy, group, kilobytes=False, megabytes=False):
    group_usage = sum(
        mutil.get_usage_for_a_user(user)
        for user in policy[group]['users']
    )
    print_with_highlighting(
        '{}: {}'.format(
            group,
            stringify_usage(
                mutil.convert_usage(
                    group_usage, kilobytes=kilobytes, megabytes=megabytes
                ),
                kilobytes=kilobytes, megabytes=megabytes
            )
        ),
        memory_usage_gb=mutil.convert_usage(group_usage)
    )
    for user in policy[group]['users']:
        usage = mutil.get_usage_for_a_user(user)
        print_with_highlighting(
            '  {}: {}'.format(
                user,
                stringify_usage(
                    mutil.convert_usage(
                        usage, kilobytes=kilobytes, megabytes=megabytes
                    ),
                    kilobytes=kilobytes, megabytes=megabytes
                )
            ),
            memory_usage_gb=mutil.convert_usage(usage)
        )


def display_total_usage_for_users(users, kilobytes=False, megabytes=False):
    total_usage = sum(mutil.get_usage_for_a_user(user) for user in users)
    print_with_highlighting(
        '{}: {}'.format(
            'TOTAL',
            stringify_usage(
                mutil.convert_usage(
                    total_usage, kilobytes=kilobytes, megabytes=megabytes
                ),
                kilobytes=kilobytes, megabytes=megabytes
            )
        ),
        memory_usage_gb=mutil.convert_usage(total_usage)
    )


def main(args):
    if not (args.groups or args.users):
        display_usage_for_a_user(
            getpass.getuser(), kilobytes=args.kilobytes,
            megabytes=args.megabytes
        )
    elif args.groups and (not args.users):
        groups = args.groups.split(',')
        policy = mutil.load_policy(mutil.CURRENT_POLICY_PATH)
        if set(groups) - set(policy.keys()):
            raise Exception(
                'group(s) {} not present in the policy'.format(
                    ', '.join(set(groups) - set(policy.keys()))
                )
            )
        users = {user for group in groups for user in policy[group]['users']}
        for group in groups:
            display_usage_for_a_group(
                policy, group, kilobytes=args.kilobytes,
                megabytes=args.megabytes
            )
        if len(groups) > 1:
            display_total_usage_for_users(
                users, kilobytes=args.kilobytes, megabytes=args.megabytes
            )
    elif (not args.groups) and args.users:
        users = set(user for user in args.users.split(','))
        for user in users:
            display_usage_for_a_user(
                user, kilobytes=args.kilobytes, megabytes=args.megabytes
            )
        if len(users) > 1:
            display_total_usage_for_users(
                users, kilobytes=args.kilobytes, megabytes=args.megabytes
            )
    elif args.groups and args.users:
        groups = args.groups.split(',')
        users = set(user for user in args.users.split(','))
        policy = mutil.load_policy(mutil.CURRENT_POLICY_PATH)
        if set(groups) - set(policy.keys()):
            raise Exception(
                'group(s) {} not present in the policy'.format(
                    ', '.join(set(groups) - set(policy.keys()))
                )
            )
        group_users = {
            user
            for group in groups
            for user in policy[group]['users']
        }
        total_users = (
            {
                user
                for group in groups
                for user in policy[group]['users']
            }
            |
            set(users)
        )
        for group in groups:
            display_usage_for_a_group(
                policy, group, kilobytes=args.kilobytes,
                megabytes=args.megabytes
            )
        for user in sorted(set(users) - set(group_users)):
            display_usage_for_a_user(
                user, kilobytes=args.kilobytes,
                megabytes=args.megabytes
            )
        display_total_usage_for_users(
            total_users, kilobytes=args.kilobytes,
            megabytes=args.megabytes
        )


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=('display memory usage for users or groups')
    )
    parser.add_argument(
        '-g', '--groups',
        help='comma-separated list of groups for usage display'
    )
    parser.add_argument(
        '-u', '--users',
        help='comma-separated list of usernames for usage display'
    )
    display_group = parser.add_mutually_exclusive_group()
    display_group.add_argument(
        '-k', '--kilobytes', action='store_true',
        help='display usage in kilobytes'
    )
    display_group.add_argument(
        '-m', '--megabytes', action='store_true',
        help='display usage in megabytes'
    )
    return parser.parse_args()




# Execute ----------------------------------------------------------------------

if __name__ == '__main__':
    args = parse_arguments()
    main(args)
