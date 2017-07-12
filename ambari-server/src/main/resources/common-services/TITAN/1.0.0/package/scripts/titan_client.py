"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Ambari Agent

"""

import sys
import os
from resource_management import *
from resource_management.libraries.functions import conf_select
from resource_management.libraries.functions import stack_select
from resource_management.libraries.functions import StackFeature
from resource_management.libraries.functions.stack_features import check_stack_feature
import titan

from ambari_commons.os_family_impl import OsFamilyFuncImpl, OsFamilyImpl

class TitanClient(Script):
    def get_component_name(self):
        return "titan-client"

    def configure(self, env):
        import params
        env.set_params(params)
        titan.titan()

    def status(self, env):
        raise ClientComponentHasNoStatus()

@OsFamilyImpl(os_family=OsFamilyImpl.DEFAULT)
class TitanClientLinux(TitanClient):

    def pre_rolling_restart(self, env):
        import params
        env.set_params(params)

        if params.version and check_stack_feature(StackFeature.ROLLING_UPGRADE, params.version):
            conf_select.select(params.stack_name, "titan", params.version)
            stack_select.select("titan-client", params.version)

    def install(self, env):
        self.install_packages(env)
        self.configure(env)

if __name__ == "__main__":
    TitanClient().execute()
