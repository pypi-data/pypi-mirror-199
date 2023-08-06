#!/usr/bin/env python3
#===============================================================================
# update_shared.py
#===============================================================================

"""Update the shared memory value in the memory policy"""




# Imports ----------------------------------------------------------------------

import argparse
import itertools

import mutil




# Functions --------------------------------------------------------------------

def update_policy(policy_path, shared_memory, enact=False):
    policy = mutil.load_policy(policy_path)
    if policy['shared'] == shared_memory:
        return
    
    shared_memory_overage = shared_memory - policy['shared']
    
    if policy['free']['memory_limit'] - shared_memory_overage >= 16:
        policy['free']['memory_limit'] -= shared_memory_overage
        policy['shared'] = shared_memory
        mutil.dump_policy(policy, policy_path)
        if enact:
            mutil.enact_policy(policy)
            mutil.enact_policy(policy)
        return
    
    policy['free']['memory_limit'] = 16
    policy['shared'] = shared_memory
    for group in itertools.islice(
        itertools.cycle(mutil.get_group_set(policy) - {'free'}),
        shared_memory_overage - policy['free']['memory_limit'] + 16
    ):
        policy[group]['memory_limit'] -= 1
    mutil.dump_policy(policy, policy_path)
    if enact:
        mutil.enact_policy(policy)
        mutil.enact_policy(policy)
    

def main(args):
    mutil.require_super_user()
    shared_memory = (
        mutil.shared_memory_in_gigabytes() if not args.shared
        else args.shared
    )
    update_policy(mutil.PROPOSED_POLICY_PATH, shared_memory)
    update_policy(mutil.CURRENT_POLICY_PATH, shared_memory, enact=True)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=(
            'Update the shared memory value in current and proposed policies'))
    parser.add_argument(
        '--shared', type=int,
        help='Impose a shared memory value for testing')
    return parser.parse_args()




# Execute ----------------------------------------------------------------------

if __name__ == '__main__':
    args = parse_arguments()
    main(args)
