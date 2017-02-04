# Stop Motion, Timelapse and Animation using Web Cams

This software was originally created for use with Scouts - that is children
aged 10 1/2 - 14. Worked really well for them. Should work well for younger
children too.

## Features

* Linux based using normal webcams (Raspberry Pi will work fine)
* Creates AVIs - using avconv
* Able to see your progress easily
* Onion skinning - making ad hoc stop motion simpler
* Simple code
* Frame based - meaning recreating the animation time and again doesn't
  result in video degradation.

## Requires

* pygame - 1.9.1 or later    (apt-get install python-pygame)
* python 2.7 - due to pygame (apt-get install python2.7)
* Linux - since pygame's camera support works under linux
* A webcam. Many webcams available now work - but there's a particular
  standard which used to be badged as "Windows Vista certified" which
  pygame works with cleanly

## Manual Installation:

There's a makefile with various targets. The one you may want is:

    make install

This just does

    sudo python setup.py install

(type `make` by itself for a list of other targets)


## Ubuntu installation via Ubuntu PPA:

First add my sparkslabs PPA, unless you've already done this:

    sudo add-apt-repository ppa:sparkslabs/packages
    sudo apt-get update

Then install the app:

    sudo apt-get install python-camination

## Running the app:

    camination

_No arguments as yet. This will look for any available camera and use that._

## Operation

Deliberately simple:

  - space - take photo
  - p (or r) - record a preview
  - escape - quit - don't record a video

Videos are always created with a new name based on current name - to avoid accidentally overwriting a video you want!

## Note

At present it's based around stop motion, but I also have some time lapse code
(including de-duplication of frames) which will be added to this in.

It's aimed to be quick, simple and fun to use.

There are missing features - notably I think these should be added at some point:

* Audio recording
* Frame deletion/undo
* Frame counter / time into video counter
