#!/usr/bin/env python3

# Copyright 2020 Proyectos y Sistemas de Mantenimiento SL (eProsima).
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
import logging
import re
import requests
import yaml


def github_get_tags(
        repository_owner,
        repository_name,
        github_token=None):
    """."""
    headers = {}
    if github_token:
        headers['Accept'] = 'application/vnd.github.v3+json'
        headers['Authorization'] = f'token {github_token}'

    url = (f'https://api.github.com/repos/{repository_owner}' +
           f'/{repository_name}/git/refs/tags')
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    tags = []
    release_pattern = re.compile('[vV][0-9]+\.[0-9]+\.[0-9]+(-.*)?$')
    for element in r.json():
        tag = element['ref'].split('/')[-1]
        tags.append(tag) if release_pattern.match(tag) else tags

    return tags


def version_as_list(semver):
    """"."""
    return semver.split('-')[0].replace('v', '').replace('V', '').split('.')


def get_current_version_latest_patch(tags, current_version):
    """."""
    ret = None
    for tag in tags:
        tag_version = version_as_list(tag)
        if (
            int(current_version[0]) == int(tag_version[0]) and
            int(current_version[1]) == int(tag_version[1]) and
            int(current_version[2]) <= int(tag_version[2])
        ):
            ret = tag_version
    return ret


if __name__ == '__main__':

    updated = False

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-r',
        '--repos_file',
        help='VCS .repos file',
        required=True
    )
    parser.add_argument(
        '-o',
        '--output_file',
        help='File to write the result',
        required=True
    )
    parser.add_argument(
        '-t',
        '--token',
        help='Github token',
        required=True,
    )
    parser.add_argument(
        '-b',
        '--branch',
        help='Tracked branch',
        required=True
    )
    # Parse arguments
    args = parser.parse_args()
    args.repos_file = 'dds-suite.repos'

    with open(args.repos_file, 'r') as input_file:
        repos_file = yaml.safe_load(input_file)

    output = ''
    for repo in repos_file['repositories']:
        url = repos_file['repositories'][repo]['url']
        url_elements = url.replace('.git', '').split('/')
        repo_name = url_elements[-1]
        repo_owner = url_elements[-2]

        # Filter out repos not owned by us, as we should manage them more
        # carefully
        if repo_owner.lower() != 'eprosima':
            continue

        tags = github_get_tags(
            repository_owner=repo_owner,
            repository_name=repo_name,
            github_token=args.token
        )

        default_branches = [
            'eprosima-dds-suite',
            'fastdds-suite',
            'xrcedds-suite'
        ]

        ver = repos_file['repositories'][repo]['version']
        current_version = version_as_list(ver)
        current_version_latest_patch = get_current_version_latest_patch(tags, current_version)
        new_version = version_as_list(tags[-1])

        if (
            # This is a new tag with a higher SEMVER on a default branch; we
            # want to update it
            (
                args.branch in default_branches and
                ver != tags[-1] and
                (
                    int(current_version[0]) < int(new_version[0]) or
                    (
                        int(current_version[0]) == int(new_version[0]) and
                        int(current_version[1]) < int(new_version[1])
                    ) or
                    (
                        int(current_version[0]) == int(new_version[0]) and
                        int(current_version[1]) == int(new_version[1]) and
                        int(current_version[2]) < int(new_version[2])
                    )
                )
            ) or
            # This is a new tag in the same minor SEMVER but with a higher
            # patch version on a non default branch; we want to update it
            (
                args.branch not in default_branches and
                ver != tags[-1] and
                (
                    int(current_version[0]) == int(current_version_latest_patch[0]) and
                    int(current_version[1]) == int(current_version_latest_patch[1]) and
                    int(current_version[2]) < int(current_version_latest_patch[2])
                )
            )
        ):
            current_version_latest_patch_str = 'v' + '.'.join(current_version_latest_patch)
            output += f'{repo},{current_version_latest_patch_str};'
            repos_file['repositories'][repo]['version'] = current_version_latest_patch_str
            updated = True

    if updated is True:
        with open(args.output_file, 'w') as output_file:
            yaml.safe_dump(repos_file, output_file)
        print(output[:-1])
    else:
        print('No updates required')

    exit(0)
