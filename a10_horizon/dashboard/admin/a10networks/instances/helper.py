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

import logging

LOG = logging.getLogger(__name__)

from horizon_ops import HorizonOps

def get_hosts(request, nova_api, hostname=None):
    hyper_list = nova_api.hypervisor_list(request)

    host_list = []
    for elem in hyper_list:
        if elem.hypervisor_hostname == hostname:
            return elem.id

        host_list.append(elem.hypervisor_hostname)

    return host_list

def patch(request, nova_api, keystone_api, device_list=[]):
    result_list = []
    for instance in device_list:
        server = nova_api.server_get(request, instance["nova_instance_id"])
        flavor = server.flavor
        flavor_id = flavor["id"]

        tenants = keystone_api.tenant_list(request)

        setattr(instance, "flavor", nova_api.flavor_get(request, flavor_id))
        setattr(instance, "image", server.image_name)
        setattr(instance, "owner", keystone_api.tenant_get(request, server.tenant_id).name)
        setattr(instance, "comp_name", server.host_server)
        setattr(instance, "comp_id", get_hosts(request, nova_api, server.host_server))
        result_list.append(instance)
    return result_list

def migrate(request, nova_api, id):
    try:
        nova_api.server_migrate(request, id)
        return True
    except Exception:
        LOG.exception("Failure to migrate.")

    return False

