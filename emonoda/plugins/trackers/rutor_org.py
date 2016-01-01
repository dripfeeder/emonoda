"""
    Emonoda -- A set of tools to organize and manage your torrents
    Copyright (C) 2015  Devaev Maxim <mdevaev@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


import re

from ...optconf import Option

from . import BaseTracker
from . import WithHash


# =====
class Plugin(BaseTracker, WithHash):
    PLUGIN_NAME = "rutor.org"

    _SITE_VERSION = 3
    _SITE_ENCODING = "utf-8"

    _SITE_FINGERPRINT_URL = "http://fast-bit.org"
    _SITE_FINGERPRINT_TEXT = "<a href=\"/\"><img src=\"/s/logo.jpg\" alt=\"rutor.org logo\" /></a>"

    _COMMENT_REGEXP = re.compile(r"^http://rutor\.org/torrent/(\d+)$")

    _TORRENT_HASH_URL = "http://fast-bit.org/torrent/479259"
    _TORRENT_HASH_REGEXP = re.compile(r"<div id=\"download\">\s+<a href=\"magnet:\?xt=urn:btih:([a-fA-F0-9]{40})")

    # ===

    def __init__(self, **kwargs):  # pylint: disable=super-init-not-called
        self._init_bases(**kwargs)
        self._init_opener(with_cookies=False)

    @classmethod
    def get_options(cls):
        return cls._get_merged_options({
            "user_agent": Option(default="Googlebot/2.1", help="User-agent for site"),
        })

    # ===

    def fetch_new_data(self, torrent):
        self._assert_match(torrent)
        torrent_id = self._COMMENT_REGEXP.match(torrent.get_comment()).group(1)
        data = self._read_url("http://fast-bit.org/download/{}".format(torrent_id))
        self._assert_valid_data(data)
        return data