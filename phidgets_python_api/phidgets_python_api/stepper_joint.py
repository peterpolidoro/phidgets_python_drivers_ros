# Copyright (c) 2020, Howard Hughes Medical Institute
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from phidget_python_api.stepper import Stepper, StepperInfo
from phidget_python_api.digital_input import DigitalInput, DigitalInputInfo

class StepperJointInfo():
    def __init__(self):
        self.stepper_info = StepperInfo()
        self.home_switch_info = DigitalInputInfo()
        self.home_velocity_limit = 1000
        self.home_target_position = -10000

class StepperJoint:
    def __init__(self, stepper_joint_info):
        self.stepper = Stepper(stepper_joint_info.stepper_info)
        self.home_switch = DigitalInput(stepper_joint_info.home_switch_info)
        self._stepper_joint_info = stepper_joint_info

    def home(self):
        if self.home_switch.getState():
            self.stepper.set_velocity_limit(self._stepper_joint_info.home_velocity_limit)
            self.stepper.set_target_position(self._stepper_joint_info.home_target_position)
            while self.home_switch.getState():
                pass
            self.stepper.set_velocity_limit(0.0)
            self.stepper.add_position_offset(-self.stepper.get_position())
            self.stepper.set_target_position(0.0)
            self.stepper.set_velocity_limit(self._stepper_joint_info.stepper_info.velocity_limit)

    def close(self):
        self.stepper.close()
        self.home_switch.close()
