"""
  Code to produce rasterized equivalents of povray scenes.
  use init() first to setup the camera settings,
  then call render() as many times as needed

  Being able to get rasterized output is useful to us for a couple of reasons:
  - wireframe output
  - 3d volumes can easily be generated by using the near and far parameters

  requires opengl
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import Image, ImageOps

SIZE = (500, 500)
initialized = False
windowHandle = None

"""
  Initialize an OpenGL context. After the first call to init(), all following calls will
  destroy the previous init call's OpenGL context.

  Set ortho to true to enable orthographic projection
  The near and far parameters will only be used if ortho is set to true.
"""
def init(camera, near=0., far=1., ortho=False):
  global initialized, SIZE, windowHandle

  cameraPos = camera.getPosition()
  lookAt = camera.getLookAt()
  fov = camera.getFov()

  # destroy the previous window if it exists
  # letting the previous windows accumulate will result in glitchy output!
  if windowHandle:
    glutDestroyWindow(windowHandle)

  glutInit()
  glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
  glutInitWindowSize(SIZE[0], SIZE[1])
  windowHandle = glutCreateWindow('')
  glutHideWindow()

  upVector = [0., 1., 0.]
  aspect = SIZE[0] / float(SIZE[1])
  glDisable(GL_LIGHTING)
  glDisable(GL_CULL_FACE)
  glEnable(GL_BLEND)
  glEnable(GL_DEPTH_TEST)
  glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

  if ortho:
    # orthographic setup
    glMatrixMode(GL_PROJECTION)
    glOrtho(1., 0.,
            0., 1.,
            -near, -far)
    glMatrixMode(GL_MODELVIEW)
  else:
    # perspective setup
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fov, aspect, 1.0, 10.0)
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(cameraPos[0], cameraPos[1], cameraPos[2],
              lookAt[0], lookAt[1], lookAt[2],
              upVector[0], upVector[1], upVector[2])

  glClearColor(0.0, 0.0, 0.0, 1.0)

  initialized = True

"""
  Render a list of shapes and write to disk as fileName
"""
def render(meshes, fileName, wireFrame=False):
  global initialized, SIZE
  assert initialized

  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
  for mesh in meshes:
    glPolygonMode(GL_FRONT_AND_BACK, (GL_LINE if wireFrame else GL_FILL))
    glPushMatrix()

    # apply transformations
    glColor3f(*mesh.getColor())
    glTranslatef(*mesh.getTranslation())
    glScalef(*mesh.getScale())
    glRotatef(mesh.getRotation()[2], 0, 0, 1)
    glRotatef(mesh.getRotation()[1], 0, 1, 0)
    glRotatef(mesh.getRotation()[0], 1, 0, 0)

    # send triangles
    glBegin(GL_TRIANGLES)
    for triangle in mesh.getTriangles():
      for vertex in triangle:
        glVertex3f(vertex[0], vertex[1], vertex[2])
    glEnd()

    glPopMatrix()

  glFlush()
  glutSwapBuffers()

  # save the framebuffer to disk
  data = glReadPixels(0, 0, SIZE[0], SIZE[1], GL_RGB, GL_BYTE)
  img = Image.frombuffer('RGB', SIZE, data, 'raw', 'RGB')
  flipped = ImageOps.mirror(ImageOps.flip(img))
  flipped.save(fileName)

