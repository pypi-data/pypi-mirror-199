#!/usr/bin/env python3
#===============================================================================
# mdraft.py
#===============================================================================

"""Draft a memory policy proposal"""




# Imports ----------------------------------------------------------------------

import argparse
import json

import mutil




# Functions --------------------------------------------------------------------

def load_draft(arg):
    try:
        draft = json.loads(arg)
    except:
        with open(arg, 'r') as f:
            draft = json.load(f)
    return draft


def main(args):
    draft = load_draft(args.draft)
    draft_users = mutil.get_user_set(draft)
    total_reserved_memory = mutil.reserved_memory(draft)
    proposed_policy = mutil.load_policy(mutil.PROPOSED_POLICY_PATH)
    proposed_policy_users = mutil.get_user_set(proposed_policy)
    mutil.validate_draft_policy(
        draft, total_reserved_memory, draft_users, proposed_policy_users)
    draft['free'] = mutil.infer_free_group(
        draft, total_reserved_memory, draft_users, proposed_policy_users)
    draft['shared'] = mutil.shared_memory_in_gigabytes()
    mutil.dump_policy(draft, mutil.PROPOSED_POLICY_PATH)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Draft a memory policy proposal')
    parser.add_argument('draft')
    return parser.parse_args()




# Execute ----------------------------------------------------------------------

if __name__ == '__main__':
    args = parse_arguments()
    main(args)
