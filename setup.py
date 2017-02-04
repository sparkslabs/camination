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

from distutils.core import setup
from distutils.version import LooseVersion
import os

def is_package(path):
    return (
        os.path.isdir(path) and
        os.path.isfile(os.path.join(path, '__init__.py'))
        )

def find_packages(path, base="" ):
    """ Find all packages in path """
    packages = {}
    for item in os.listdir(path):
        dir = os.path.join(path, item)
        if os.path.isdir(dir):
            if base:
                module_name = "%(base)s.%(item)s" % vars()
            else:
                module_name = item
            if is_package( dir ):
                packages[module_name] = dir
            packages.update(find_packages(dir, module_name))
    return packages


packages = find_packages(".")
package_names = packages.keys()

setup(name = "camination",
      version = "0.1.1",
      description = "Stop Motion, Timelapse and Animation using Webcams",
      url='http://www.sparkslabs.com/camination/',
      author='Michael Sparks (sparkslabs)',
      author_email="sparks.m@gmail.com",
      license='Apache Software License',

      scripts = [
                  'bin/camination',
                ],

      packages = package_names,
      package_dir = packages,
      package_data={},
      long_description = """
Stop Motion, Timelapse and Animation using Web Cams
---------------------------------------------------

This software was originally created for use with Scouts - that is children
aged 10 1/2 - 14. Worked really well for them.


Features
~~~~~~~~

- Linux based using normal webcams (Raspberry Pi will work fine)

- Creates AVIs - using avconv

- Able to see your progress easily

- Onion skinning - making ad hoc stop motion simpler

- Simple operation

    - space - take photo

    - p (or r) - record a preview

    - escape - quit - don't record a video 

- Simple code - using python and pygame

- Frame based - meaning recreating the animation time and again doesn't
  result in video degradation.

At present it's based around stop motion, but I also have some time lapse
code (including de-duplication of frames) which will be added to this.

It's aimed to be quick, simple and fun to use. 

There are missing features.

Notably I think these should be added at some point:

- Audio recording
- Frame deletion/undo
- Frame counter / time into video counter


Release History
---------------

Release History:

-  0.1.0 - UNRELEASED - Initial version used with scouts.

-  0.1.1 - TBD - Packaged up, and documented.


Michael Sparks, February 2017
"""
      )
