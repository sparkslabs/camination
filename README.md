# Stop Motion, Timelapse and Animation using Web Cams

This software was originally created for use with Scouts - that is children
aged 10 1/2 - 14. Worked really well for them.

## Features

* Linux based using normal webcams (Raspberry Pi will work fine)
* Creates AVIs - using avconv
* Able to see your progress easily
* Onion skinning - making ad hoc stop motion simpler
* Simple operation
  - space - take photo
  - p (or r) - record a preview
  - escape - quit - don't record a video 
* Simple code - using python and pygame
* Frame based - meaning recreating the animation time and again doesn't
  result in video degradation.

At present it's based around stop motion, but I also have some time lapse
code (including de-duplication of frames) which will be added to this.

It's aimed to be quick, simple and fun to use. 

There are missing features.

Notably I think these should be added at some point:

* Audio recording
* Frame deletion/undo
* Frame counter / time into video counter
