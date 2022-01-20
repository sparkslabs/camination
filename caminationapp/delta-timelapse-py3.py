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

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_VIDEODRIVER"] = "directfb"

import pygame, time
import pygame.camera


pygame.init()
pygame.camera.init()


fontname =  "/home/michael/saxmono.ttf"
font = pygame.font.Font(fontname, 48)

displaysize = (800, 600)
capturesize = (640, 480)

capturesize = (1280, 800)

imagesize = (352, 288)
imageorigin = (0,0)
#device = "/dev/video0"
device = "/dev/video1"
# device = "/dev/video2"
device = pygame.camera.list_cameras()[0]

print("HERE", device )
basedir = os.path.expanduser("~")

state, older_state = [], []
prepend = ""

def Print(*args):
    x = prepend + " ".join([str(x) for x in args])+"\n"
    f = open(basedir+"/snaplog.txt","a+")
    f.write(x)
    f.close()    


def bw_pixel(p):
    average = (sum(p[0:3])/3)**2
    return average


def ave_surface(surface):
    width = surface.get_width()
    height = surface.get_height()
    pixels = []
    for x in range(width):
        for y in range(height):
            pixels.append(bw_pixel(surface.get_at((x,y))))

    return int((1.0*sum(pixels)) / len(pixels))

def fragment_aves(surface):
    chunks = []
    width = surface.get_width()
    height = surface.get_height()
    for x in range(0, width, 32):
        for y in range(0, height, 25):
             fragment = pygame.surface.Surface((32, 25))
             fragment.blit(surface, (0,0),(x,y, 32,25))
             #full_filename = basedir+("/Snaps/frag-%d-%d.jpg"  % (x,y))
             #pygame.image.save(fragment, full_filename)
             a = ave_surface(fragment)
             chunks.append(a)


    chunks.sort()
    return chunks

def mean(seq):
    return (1.0*sum(seq))/len(seq)

def std_deviation(seq):
    ave = mean(seq)
    return mean([(ave-i)**2 for i in seq ])

def change(oldsnap, newsnap):
   global state
   Print("checking", time.time())
   smaller_50 = pygame.transform.scale(newsnap, (320, 200))

   new_state = fragment_aves(smaller_50)

   #full_filename = basedir+"/Snaps/WIP-raw.jpg"
   #pygame.image.save(smaller_50, full_filename)

   if state == []:
       Print("INIT")
       state = new_state
       return True
   else:
       state_ds = []
       for i in range(len(new_state)):
           Print("abs(new_state[i] - state[i])", abs(new_state[i] - state[i]), new_state[i], state[i]   )
           if abs(new_state[i] - state[i])>1:  # Reduce changes due to image noise
                state_ds.append(abs(new_state[i] - state[i]))

       if len(state_ds) == 0:
           Print("Um....")
           return False
       mean_ds = int(mean(state_ds))
       std_dev_ds = int(std_deviation(state_ds))

       Print("State DS", state_ds)
       Print("State DS (mean)", mean_ds)
       Print("State DS (std_deviation)", std_dev_ds)
       if std_dev_ds > 1000:
           Print("Capture?", mean_ds, std_dev_ds)

       if mean_ds * std_dev_ds > 110000:
           state = new_state
           Print("checking_return_true")
           return True

   Print("checking_return_false", time.time())
   return False

camera = pygame.camera.Camera(device, capturesize)
camera.start()
      
for i in xrange(20): # Taking multiple images allows the camera to settle
    snap = camera.get_image()


x = time.time()
oldsnap = None
oldersnap = None
while True:
    for i in xrange(4): # Taking multiple images allows the camera to settle
        snap = camera.get_image()

    if time.time() -x >= 1:
        x = time.time()
        Print(x)

    now = time.time()
    t = time.localtime(now)
    ext=str(now - int(now))
    milli = ext[2:5]
    filename = "%04d%02d%02d.%02d%02d%02d.%s.jpg" %(t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min,t.tm_sec, milli)
    full_filename = basedir+"/Snaps/"+filename
    
    now_str = "%02d:%02d:%02d.%s %02d/%02d/%d" % (t.tm_hour, t.tm_min, t.tm_sec, milli, t.tm_mday, t.tm_mon, t.tm_year)

    antialias = False
    color = (240, 128, 0)
    bgcolor = (0,0,0)
    location = (5,5)
    text_surface = font.render(now_str , antialias, color, bgcolor)
    text_surface.set_colorkey(bgcolor)
    snap.blit(text_surface, location)

    print("save", full_filename)
    pygame.image.save(snap, full_filename)

    if oldsnap == None:
       oldsnap = oldersnap = snap
       Print(" SNAP")
       time.sleep(0.02)
       continue

    print("change(oldsnap, snap)")
    if change(oldsnap, snap):
        if change(oldsnap, snap):
            print("change(oldsnap, snap)")
            Print(" SNAP")
            oldersnap = oldsnap
            oldsnap = snap
            if False:
               os.system( 'curl -F "file=@' + full_filename + '" http://3.8.19.118/cgi-bin/manage.py/' )
            time.sleep(0.02)
        else:
            Print(" UN-SNAP OLDER")
            os.unlink(full_filename)
    else:
        Print(" UN-SNAP")
        os.unlink(full_filename)

