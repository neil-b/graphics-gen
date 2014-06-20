"""
  Code to produce raytraced scenes.
  Camera, lights and shapes are converted into the povray scene description
  language (see __str__() in shapes.py) and written to a text file.
  The text file is then passed to povray to be rendered

  requires povray (command line program)
"""

import os

def render(camera, lights, shapes, fileName):
  textFileName = fileName + '.txt'
  f = open(textFileName, 'w')
  f.write(str(camera))
  for light in lights:
    f.write(str(light))
  for shape in shapes:
    f.write(str(shape))
  f.close()

  os.system('povray -W500 -H500 +I' + textFileName)
