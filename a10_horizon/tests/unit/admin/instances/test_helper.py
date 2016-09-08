# Copyright (C) 2015, A10 Networks Inc. All rights reserved.
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

import mock
import unittest

from a10_horizon.dashboard.admin.a10networks.instances import helper
from a10_horizon.dashboard.admin.a10networks.instances.horizon_ops import HorizonOps
from fake_objs import FakeA10Device
from fake_objs import FakeA10DeviceBuilt
from fake_objs import FakeNovaServer
from fake_objs import FakeHypervisor
import a10_horizon.tests.test_case as test_case

class TestAdminHelper(test_case.TestCase):

    def setUp(self):
        self.a10_device = FakeA10Device()
        self.a10_patched = FakeA10DeviceBuilt()
        self.nova_server = FakeNovaServer()
        self.hyper = FakeHypervisor()
        self.request = mock.MagicMock()
        self.horiz = HorizonOps()
        self.nova_api = self.horiz.get_nova = mock.MagicMock()
        self.keystone_api = self.horiz.get_keystone = mock.MagicMock()

    def tearDown(self):
        self.a10_device = None
        self.a10_patched = None
        self.nova_server = None

    def test_get_hosts(self):
        self.nova_api.hypervisor_list = mock.MagicMock(return_value=[self.hyper])
        host_list = helper.get_hosts(self.request, self.nova_api)

        self.assertEqual(host_list, ["comp1"])

    def test_get_hosts_filtered(self):
        self.nova_api.hypervisor_list = mock.MagicMock(return_value=[self.hyper])
        host_id = helper.get_hosts(self.request, self.nova_api, self.a10_patched.comp_name)

        self.assertEqual(host_id, "3")

    # (TODO:Hunter) What do we care about during testing? What are the outliers?
    # We aren't testing the api. We are just testing that the a10_device changes
    # We coudl test if it has all the attributes but that'll take a while. 
    def test_patch(self):
        tenant_mock = mock.MagicMock()
        tenant_mock.name = "own1"
        self.keystone_api.tenant_get = mock.MagicMock(return_value=tenant_mock)

        self.nova_api.server_get = mock.MagicMock(return_value=self.nova_server)
        self.nova_api.flavor_get = mock.MagicMock(return_value="grande")

        helper.get_hosts = mock.MagicMock(return_value='3')
        results = helper.patch(self.request, self.nova_api, self.keystone_api, [self.a10_device])

        self.assertAttributeEqual(results[0], self.a10_patched)

    def test_patch_emptylist(self):
        self.keystone_api.tenant_get = mock.MagicMock()
        self.keystone_api.tenant_get.name = mock.MagicMock()

        self.nova_api.server_get = mock.MagicMock()
        self.nova_api.flavor_get = mock.MagicMock()

        helper.get_hosts = mock.MagicMock()
        results = helper.patch(self.request, self.nova_api, self.keystone_api)

        self.assertTrue(results == [])

    def test_migrate(self):
        self.nova_api.server_live_migrate = mock.MagicMock()
        helper.migrate(self.request, self.nova_api,
                       self.a10_patched.nova_instance_id,
                       self.a10_patched.comp_name)

        self.nova_api.server_live_migrate.assert_called_with(self.request,
                                                             self.a10_patched.nova_instance_id,
                                                             self.a10_patched.comp_name,
                                                             block_migration=True)

