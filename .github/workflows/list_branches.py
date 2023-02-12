#!/usr/bin/env python3

# Copyright 2023 Proyectos y Sistemas de Mantenimiento SL (eProsima).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""."""

import argparse
import re
import requests
import json

supported_branches = [
    'eprosima-dds-suite',
    'fastdds-suite',
    'xrcedds-suite'
]


def github_get_branches(
        github_token=None):
    """."""
    headers = {}
    if github_token:
        headers['Accept'] = 'application/vnd.github.v3+json'
        headers['Authorization'] = f'token {github_token}'

    url = ('https://api.github.com/repos/eProsima/DDS-Suite/branches')
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    branches = []
    regex = '|'.join('{}'.format(branch+'.*') for branch in supported_branches)
    release_pattern = re.compile(regex)
    for element in r.json():
        branches.append(
            element['name']
        ) if release_pattern.match(
            element['name']
        ) else branches

    return branches


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-t',
        '--token',
        help='Github token',
        required=False,
    )
    # Parse arguments
    args = parser.parse_args()

    output = ''
    branches = github_get_branches(
        github_token=args.token
    )

    json_output = json.dumps(branches)
    print(json_output)
    exit(0)
