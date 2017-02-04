#!/usr/bin/python
#
# Copyright 2017 Michael Sparks - sparks.m@gmail.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#
# Note: The functionality from this app is not yet integrated into the main app
# in case you were wondering why this doesn't seem to work.
#
# It will work stand alone though it makes a number of assumptions.
#

import os
import sys
import pygame, time
import pygame.camera
pygame.init()
pygame.camera.init()

displaysize = (800, 600)
capturesize = (640, 480)
imagesize = (352, 288)
imageorigin = (0,0)
device = "/dev/video0"

basedir = os.path.expanduser("~")

# display = pygame.display.set_mode(displaysize)
camera = pygame.camera.Camera(device, capturesize)
camera.start()

while 1:
    for i in range(5):
        time.sleep(0.5)
        sys.stdout.write(".")
        sys.stdout.flush()

    print " SNAP"

    for i in xrange(20):
        snapshot = camera.get_image()

    t = time.localtime()
    filename = "%04d%02d%02d.%02d%02d%02d.jpg" %(t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min,t.tm_sec)

    pygame.image.save(snapshot, basedir+"/Snaps/"+filename)
