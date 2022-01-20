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
capturesize = (1280, 800)

basedir = os.path.expanduser("~")

state, older_state = [], []

device = pygame.camera.list_cameras()[0]
print("Using device:", device )

def Log(*args):
    x = " ".join([str(x) for x in args])+"\n"
    f = open(basedir+"/snaplog.txt","a+")
    f.write(x)
    f.close()    

camera = pygame.camera.Camera(device, capturesize)
camera.start()
      
for i in xrange(20): # Taking multiple images allows the camera to settle
    snap = camera.get_image()


def simplify(img,nx,ny,smooth):
    render_img = pygame.transform.scale(img, (nx, ny)) 
    ave_surface= pygame.Surface((nx,ny))
    for x in range(nx-smooth):
        for y in range(ny-smooth):
            c = []
            for i in range(smooth):
                for j in range(smooth):
                    color = render_img.get_at((x+i,y+j))
                    average = sum(color[0:3])/3
                    c.append(average)
            ave = int(sum(c)/len(c))
            ave_surface.set_at((x,y), (ave,ave,ave))

    for x in range(nx-smooth,nx):
        for y in range(ny-smooth):
            c = []
            for i in range(smooth):
                for j in range(smooth):
                    color = render_img.get_at((x-i,y+j))
                    average = sum(color[0:3])/3
                    c.append(average)
            ave = int(sum(c)/len(c))
            ave_surface.set_at((x,y), (ave,ave,ave))

    for x in range(nx-smooth):
        for y in range(ny-smooth,ny):
            c = []
            for i in range(smooth):
                for j in range(smooth):
                    color = render_img.get_at((x+i,y-j))
                    average = sum(color[0:3])/3
                    c.append(average)
            ave = int(sum(c)/len(c))
            ave_surface.set_at((x,y), (ave,ave,ave))

    for x in range(nx-smooth,nx):
        for y in range(ny-smooth,ny):
            c = []
            for i in range(smooth):
                for j in range(smooth):
                    color = render_img.get_at((x-i,y-j))
                    average = sum(color[0:3])/3
                    c.append(average)
            ave = int(sum(c)/len(c))
            ave_surface.set_at((x,y), (ave,ave,ave))

    return ave_surface

def delta_image(dlast, buffer):
    deltas = []
    for x in range(64):
        for y in range(40):
            c1 = dlast.get_at((x,y))[0]
            c2 = buffer.get_at((x,y))[0]
            d = abs(c1-c2)
            deltas.append(d)
            deltas.sort()
            deltas.reverse()
    deltas = [x for x in deltas if x > 0]

    x = {}
    for i in deltas:
        x[i] = x.get(i,0)+1
    k = list(x.keys())
    k.sort()
    k.reverse()
    k_ = [(i, x[i]) for i in k ]

    return k_

def filter_deltas(deltas, cutoff=19):
    r = [x for x in deltas if x[0] > cutoff]
    return r


x = time.time()
buffer = None
while True:
    capture = False
    snap = camera.get_image()
    time.sleep(0.2)
    ave_surface = simplify(snap,64,40,4)
    if buffer == None:
        buffer = pygame.Surface((64,40))
        buffer.blit(ave_surface, (0,0))
        dlast = pygame.Surface((64,40))
        dlast.blit(ave_surface, (0,0))
        capture = True
    else:
        for x in range(64):
            for y in range(40):
                c1 = ave_surface.get_at((x,y))
                c2 = buffer.get_at((x,y))
                nc = int((c1[0]+c2[0])/2)
                buffer.set_at((x,y), (nc,nc,nc))

    if not capture:
        image_deltas = delta_image(dlast, buffer)
        deltas = filter_deltas(image_deltas)
        if len(deltas) > 1:
            capture = True
            dlast.blit(ave_surface, (0,0))


    if capture:
        now = time.time()
        t = time.localtime(now)
        date = "%d%02d%02d" % (t.tm_year, t.tm_mon, t.tm_mday,)
        ext=str(now - int(now))
        milli = ext[2:5]
        filename = "%04d%02d%02d.%02d%02d%02d.%s.jpg" %(t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min,t.tm_sec, milli)
        day_directory = basedir+"/Snaps/"+date

        if not os.path.exists(day_directory):
            os.mkdir(day_directory)

        full_filename = basedir+"/Snaps/"+date + "/" + filename
        now_str = "%02d:%02d:%02d.%s %02d/%02d/%d" % (t.tm_hour, t.tm_min, t.tm_sec, milli, t.tm_mday, t.tm_mon, t.tm_year)
        text_surface = font.render(now_str , 0, (240, 128, 0), (0,0,0))
        text_surface.set_colorkey((0,0,0))
        snap.blit(text_surface, (5,5))

        Log("save", full_filename)
        pygame.image.save(snap, full_filename)
#        try:
#            os.unlink("/home/michael/Snaps/latest.jpg")
#        except OSError:
#            pass
#        os.link(full_filename, "/home/michael/Snaps/latest.jpg")


    time.sleep(0.04)

#>>> os.link("/home/michael/Snaps/20210723/20210723.221417.978.jpg", "/home/michael/Snaps/latest.jpg")
#>>> os.unlink("/home/michael/Snaps/latest.jpg"
#... )
#>>> os.unlink("/home/michael/Snaps/latest.jpg")
#Traceback (most recent call last):
#  File "<stdin>", line 1, in <module>
#OSError: [Errno 2] No such file or directory: '/home/michael/Snaps/latest.jpg'
#>>> 
