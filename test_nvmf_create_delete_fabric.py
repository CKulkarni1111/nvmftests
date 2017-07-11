# Copyright (c) 2015-2016 Western Digital Corporation or its affiliates.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.
#
#   Author: Chaitanya Kulkarni <chaitanya.kulkarni@hgst.com>
#
"""
NVMeOF Create/Delete Host, Target :-

    1. From the config file create Target.
    2. From the config file create host and connect to target.
    3. Delete Host.
    4. Delete Target.
"""

import time
from loopback import Loopback
from nvmf_test import NVMeOFTest
from target import NVMeOFTarget
from host import NVMeOFHost
from nose.tools import assert_equal


class TestNVMFCreateDeleteFabric(NVMeOFTest):

    """ Represents Create Delete Fabric testcase """

    def __init__(self):
        NVMeOFTest.__init__(self)
        self.loopdev = None
        self.host_subsys = None
        self.target_subsys = None

        self.setup_log_dir(self.__class__.__name__)
        self.loopdev = Loopback(self.mount_path, self.data_size,
                                self.block_size, self.nr_devices)
        time.sleep(1)

    def setUp(self):
        print("configuering loopback")
        self.loopdev.init_loopback()
        time.sleep(1)
        target_type = "loop"
        self.target_subsys = NVMeOFTarget(target_type)
        self.target_subsys.config()
        self.host_subsys = NVMeOFHost(target_type)

    def tearDown(self):
        time.sleep(1)
        self.host_subsys.delete()
        time.sleep(1)
        self.target_subsys.delete()
        print("deleting loopback")
        self.loopdev.del_loopback()

    def test_create_delete_fabric(self):
        """ Testcase main """
        ret = self.host_subsys.config_host()
        assert_equal(ret, True, "ERROR : config host failed")
