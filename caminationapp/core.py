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

import os
import pygame
import pygame.camera
import time

pygame.init()
pygame.camera.init()

displaysize = (1280, 720)
capturesize = (640, 480)

#imagesize = (640, 480)
imagesize = (1280, 720)
imageorigin = (0,0)
device = pygame.camera.list_cameras()[0] # "/dev/video0"

display = pygame.display.set_mode(displaysize)
camera = pygame.camera.Camera(device, capturesize)
camera.start()

team ="Snap"
last_picture = None

home = os.path.expanduser("~")
snap_dir = os.path.join(home, team)
video_dir = os.path.join(home, "StopMotion")

try:
  os.makedirs(video_dir)
except OSError:
  pass

try:
  os.makedirs(snap_dir)
except OSError:
  pass

textFont = pygame.font.Font(None, 200)

class DoneCapture(Exception):
  pass

class ExitApplication(Exception):
  pass

files = os.listdir(snap_dir)
files.sort()
k = iter(files)
for i in range(1,len(files)+1):
    x = "%04d.png" %i
    os.rename( os.path.join(snap_dir, k.next()), os.path.join(snap_dir, x))

while True:
    try:
      while 1:
        file_num = len(os.listdir(snap_dir))+1

        snapshot = camera.get_image()
        cropped = snapshot.subsurface(0,60,640,360)

        snapshot = pygame.transform.scale(cropped, imagesize)
        snapshot = pygame.transform.scale(snapshot, imagesize)
        if last_picture != None:
            display.blit(last_picture, imageorigin)
            snapshot.set_alpha(190)
        display.blit(snapshot, imageorigin)
        snapshot.set_alpha(255)
        pygame.display.flip()
        if pygame.event.peek():
          for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q or event.key == pygame.K_r or event.key == pygame.K_c or event.key == pygame.K_v :
                    raise DoneCapture("Done")

                if event.key == pygame.K_ESCAPE:
                    raise ExitApplication("Done")

                print "SNAP!"

                filename = "%04d.png" % file_num
                pygame.image.save(snapshot, os.path.join(snap_dir, filename))
                last_picture = snapshot

    except DoneCapture:
      black = pygame.Surface(displaysize)
      black.fill((0,0,0))
      black.set_alpha(128)
      display.blit(black, (0,0))

      the_text = textFont.render("CREATING VIDEO", True, (255,255,255))
      display.blit(the_text, (30,300))
      pygame.display.flip()

      files = os.listdir(snap_dir)
      files.sort()
      k = iter(files)
      for i in range(1,len(files)+1):
          x = "%04d.png" %i
          os.rename( os.path.join(snap_dir, k.next()), os.path.join(snap_dir, x))

      print "OK, creating video!"
      x = time.localtime(time.time())
      filename = "%04d%02d%02d.%02d%02d.avi" % (x.tm_year, x.tm_mon,x.tm_mday,x.tm_hour, x.tm_min) 
      filename = os.path.join(video_dir, filename)

#      os.system("avconv -r 8 -f image2 -i " + snap_dir+ "/%04d.png -y -same_quant -s 1280x720 -aspect 16:9 "+ filename)
      os.system("avconv -r 8 -f image2 -i " + snap_dir+ "/%04d.png -y -qscale 0 -s 640x480 -aspect 4:3 "+ filename)

      print "Done!"
      print "Playing!"

      os.system("mplayer -fs -loop 0  "+filename)
