# Copyright (c) 2024 Daniel Seichter
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import urllib3
import json
import logging


VERSION = "v2024-05-24"
UPDATEURL = 'https://api.github.com/repos/dseichter/vatservice-gui/releases/latest'
RELEASES = 'https://github.com/dseichter/vatservice-gui/releases'
NAME = 'VAT Service GUI'
LICENCE = 'GPL-3.0'


# load value from json file with given key
def load_value_from_json_file(key):
    with open('config.json', 'r') as f:
        data = json.load(f)

    if key not in data:
        return None

    return data[key]


def check_for_new_release():
    try:
        http = urllib3.PoolManager()
        r = http.request('GET', UPDATEURL)
        data = json.loads(r.data.decode('utf-8'))
        latest_version = data['tag_name']
        return latest_version != VERSION
    except Exception as e:
        logging.error(f"Error checking for new release: {e}")
        return False
