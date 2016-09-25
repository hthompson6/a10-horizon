#    Copyright (C) 2015, A10 Networks Inc. All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import unittest


def assertAttributeEqual(a, b):
    if a.__dict__ != b.__dict__:
        raise Exception("Expected {0} to have attributes of {1}".format(a.__dict__, b.__dict__))

class TestCase(unittest.TestCase):

    def __init__(self, *args):
        super(TestCase, self).__init__(*args)

        self._patch("assertAttributeEqual", assertAttributeEqual)

    def _patch(self, key, val):
        if not hasattr(self, key):
            setattr(self, key, val)
