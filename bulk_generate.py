"""
  Source to generate data from a scene. See generate()'s description
"""

import gl_render, ray_render
import os, errno

"""
  Create a directory if it doesn't already exist (aka mkdir -p)
  http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
"""
def mkdirp(directory):
  try:
    os.makedirs(directory)
  except OSError as exc:
    if exc.errno == errno.EEXIST and os.path.isdir(directory):
      pass
    else: 
      raise

"""
  Writes the following data to outDir:
    - raytraced scene
    - povray scene description language file
    - rasterized perspective scene
    - rasterized orthographic scene
    - rasterized wireframe
    - 3d volume (a set of rasterized images where the near and far values of the frustum
      do not overlap between images and in total span from 0 to 1). The number of images
      can be set by the volumeDepth parameter
"""
def generate(outDir, camera, lights, shapes, filePostfix='', volumeDepth=10):
  # create directory
  mkdirp(outDir)

  # draw perspective rasterized image and wireframe
  gl_render.init(camera)
  gl_render.render(shapes, outDir + '/rast' + filePostfix + '.png', wireFrame=False)
  gl_render.render(shapes, outDir + '/rast_wire' + filePostfix + '.png', wireFrame=True)

  # draw orthographic rasterized image
  gl_render.init(camera, ortho=True, near=0., far=1.)
  gl_render.render(shapes, outDir + '/rast_ortho' + filePostfix + '.png')
    
  # draw 3d volume 
  # note: the 3d volume only spans from (0, 0, 0) to (1, 1, 1)
  # any fragments outside the range will not be represented in the 3d volume
  for i in range(volumeDepth):
    gl_render.init(camera, ortho=True, near=(i/float(volumeDepth)), 
                                       far=((i+1)/float(volumeDepth)))
    gl_render.render(shapes, outDir + '/volume' + filePostfix + '_' + str(i) + '.png')

  # draw raytraced scene
  ray_render.render(camera, lights, shapes, outDir + '/ray' + filePostfix)

  # write vertices in world space
  pointsFile = open(outDir + '/points' + filePostfix + '.txt', 'w')
  for shape in shapes:
    pointsFile.write(str(shape.toPoints()) + '\n\n')
  pointsFile.close()

