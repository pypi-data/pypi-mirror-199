#!/usr/bin/env python3
#===============================================================================
# mrepeal.py
#===============================================================================

"""Repeal the last enacted memory policy"""




# Imports ----------------------------------------------------------------------

import argparse
import shutil

import mutil




# Function definitions ---------------------------------------------------------

def main():
    mutil.require_super_user()
    shutil.copy(mutil.PREVIOUS_POLICY_PATH, mutil.CURRENT_POLICY_PATH)
    policy = mutil.load_policy(mutil.CURRENT_POLICY_PATH)
    cgconfig, cgrules = mutil.generate_config_files(policy)
    with open(mutil.CGCONFIG_PATH, 'w') as f:
        f.write(cgconfig)
    with open(mutil.CGRULES_PATH, 'w') as f:
        f.write(cgrules)
    mutil.restart_daemons()


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=(
            'Repeal the last enacted memory policy'))
    return parser.parse_args()




# Execute ----------------------------------------------------------------------

if __name__ == '__main__':
    parse_arguments()
    main()
