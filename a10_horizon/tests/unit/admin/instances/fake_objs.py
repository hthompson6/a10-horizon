# Copyright (C) 2014-2016, A10 Networks Inc. All rights reserved.
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

class FakeA10Device(object):

    def __init__(self):
        self.id = '1'
        self.name = "instance01"
        self.ip_address = "10.0.0.5"
        self.nova_instance_id = "nova1"

    def __getitem__(self, key):
        return getattr(self, key)


class FakeA10DeviceBuilt(object):

    def __init__(self):
        self.id = '1'
        self.name = "instance01"
        self.ip_address = "10.0.0.5"
        self.nova_instance_id = "nova1"
        self.comp_name = "comp1"
        self.comp_id = '3'
        self.owner = "own1"
        self.flavor = "grande"
        self.image = "img1"

    def __getitem__(self, key):
        return getattr(self, key)


class FakeNovaServer(object):

    def __init__(self):
        self.id = '1'
        self.image_name = "img1"
        self.host_server = "comp1"
        self.flavor = {"id": "grande"}
        self.tenant_id = "ten1"


class FakeHypervisor(object):

    def __init__(self):
        self.id = '3'
        self.hypervisor_hostname = "comp1"
