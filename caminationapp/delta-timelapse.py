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

def average_color(p1, p2):
    average = [ (p1[i]+p2[i]) / 2 for i in [0,1,2]]

def change(oldsnap, newsnap):
   global maxd
   if oldsnap is None:
      print "First frame"
      return True

   if oldsnap.get_size() != newsnap.get_size():
      print "change in size"
      return True

   p10 = oldsnap.get_at((0,0))
   p20 = newsnap.get_at((0,0))
   if p10 != p20:
       p1sum = sum([x for x in p10])
       p2sum = sum([x for x in p20])
       d = abs(p2sum-p1sum)
       if d > maxd:
           maxd = d
       if d > 636/7:
            print "Colour change", p10, p20, p1sum, p2sum, d,maxd
            return True

# display = pygame.display.set_mode(displaysize)
camera = pygame.camera.Camera(device, capturesize)
camera.start()
      
maxd = 0
for i in xrange(20): # Taking multiple images allows the camera to settle
    snap = camera.get_image()

oldsnap = None
while 1:
    #for i in range(5):
        #time.sleep(0.5)
        #sys.stdout.write(".")
        #sys.stdout.flush()

    #for i in xrange(20): # Taking multiple images allows the camera to settle
    if 1:
        snap = camera.get_image()

    if change(oldsnap, snap):
        print " SNAP"
        oldsnap = snap
        t = time.localtime()
        filename = "%04d%02d%02d.%02d%02d%02d.jpg" %(t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min,t.tm_sec)

        maxd = 0
        for i in xrange(20): # Taking multiple images allows the camera to settle
            snap = camera.get_image()
        pygame.image.save(snap, basedir+"/Snaps/"+filename)
