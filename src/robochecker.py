#!/usr/bin/env python
# -*- encoding: utf8 -*-
__author__ = 'ramonmariagallart'

import argparse
import os
import requests

from io import StringIO

ERROR = 'ERROR'
WARNING = 'WARNING'
INFO = 'INFO'
LOCATED = 'LOCATED'
NOT_LOCATED = 'NOT LOCATED'

def print_message(msg, level=''):
    if level:
        msg = level + " " + msg

    print(msg)


class RoboChecker():
    def __init__(self, baseurl):
        super(RoboChecker, self).__init__()
        self.baseurl = baseurl
        self.response_text = None

    def _test_url_schema(self):
        if not self.baseurl.startswith('http'):
            print_message("The url has not schema."
                " Checking with 'http://{}'".format(self.baseurl),
                level=WARNING)
            self.baseurl = 'http://' + self.baseurl

    def _test_url_exists(self):
        url = os.path.join(self.baseurl, 'robots.txt')
        try:
            r = requests.get(url, verify=False)
            self.response_text = StringIO(r.content.decode(r.encoding))
            return r.ok
        except Exception as ex:
            print_message("Error requesting url: {}".format(ex),
                level=ERROR)
        return False

    def _parse_robots_file(self):
        for line in self.response_text:
            if 'Disallow: ' in line:
                try:
                    url_part = line.split(':')
                    if url_part[1]:
                        url_path = url_part[1].strip()
                        if url_path.startswith('/'):
                            url_path = url_path[1:]
                        url_check = os.path.join(self.baseurl, url_path)
                        r = requests.get(url_check, verify=False)
                        if r.ok:
                            print_message("{}".format(url_check),
                                level=LOCATED)
                        else:
                            print_message("{}: {}".format(
                                url_check, r.reason), level=NOT_LOCATED)
                    else:
                        pass
                except Exception as ex:
                    pass
        pass

    def check(self):
        self._test_url_schema()
        if not self._test_url_exists():
            print_message("The URL {} does not exist or has an error".format(self.baseurl), level=INFO)
            return None
        self._parse_robots_file()
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("BASEURL",
                        help="URL from wich to get robots.txt")
    args = parser.parse_args()

    baseurl = args.BASEURL

    try:
        r = RoboChecker(baseurl=baseurl)
        r.check()
    except Exception as ex:
        print("Error checking robots.txt file: {}".format(ex))
