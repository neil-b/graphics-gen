"""
  Contains class definitions Camera and Light as well as various shapes.
  Shapes can be converted to povray scene description languange compliant shapes 
  with the __str__ function.
"""

import matrix
import math

# convert list to povray vector string (eg "<1, 2, 3>")
def serializeVector(vec):
  return str(vec).replace('[', '<').replace(']', '>')

"""
  Begin Camera and Light definitions
"""

class Camera:
  def __init__(self, position, lookAt, ortho=False, maxDist=None, fov=60):
    self.position = position
    self.lookAt = lookAt
    self.useOrtho = ortho
    self.fov = fov # only for perspective (non ortho) cameras

  def __str__(self):
    return ('camera {\n'
      + '\t' + ('orthographic' if self.useOrtho else 'perspective') + '\n'
      + '\tlocation ' + serializeVector(self.position) + '\n'
      + '\tlook_at ' + serializeVector(self.lookAt) + '\n'
      + '\tangle ' + str(self.fov) + '\n'
      + '\tup ' + serializeVector([0, 1, 0]) # we encode the aspect ratio here
      + '\tright ' + serializeVector([1, 0, 0]) # and here
      + '}\n')

  def getPosition(self):
    return self.position

  def getLookAt(self):
    return self.lookAt

  def getFov(self):
    return self.fov

  def isOrtho(self):
    return self.useOrtho

class Light:
  def __init__(self, position, color=[1,1,1]):
    self.position = position
    self.color = color

  def __str__(self):
    return ('light_source { ' + serializeVector(self.position)
      + ' color rgb ' + serializeVector(self.color)
      + ' }\n')

"""
  Begin Shape definitions
"""

"""
  A group of triangles contained in a single shape.
  The input parameter triangles must be a list containing >1 triangles.
  Each triangle must be a list of size 3 containing another list of size 3,
  representing position vectors. See Cube() for example usage.

  We restrict ourselves to rendering only meshes, since every shape we raytrace needs to
  be rendered in OpenGL as well.
"""
class Shape:
  def __init__(self, triangles):
    self.triangles = triangles

    self.color = [1, 1, 1]
    self.translation = [0, 0, 0]
    self.scale = [1, 1, 1]
    self.rotation = [0, 0, 0]
    self.diffuseCoeff = 0.0
    self.ambientCoeff = 0.0
    self.materialType = None

    self.setMaterial('diffuse')

  def setMaterial(self, matType):
    self.materialType = matType
    if matType == 'simple':
      self.diffuseCoeff = 0.0
      self.ambientCoeff = 1.0
    elif matType == 'diffuse':
      self.diffuseCoeff = 0.6
      self.ambientCoeff = 0.1
    else:
      raise ValueError

  def setColor(self, c):
    assert len(c) == 3
    self.color = c

  def setTranslation(self, t):
    assert len(t) == 3
    self.translation = t

  def setScale(self, s):
    assert len(s) == 3
    self.scale = s

  def setRotation(self, r):
    assert len(r) == 3
    self.rotation = r

  def addTranslation(self, t):
    assert len(t) == 3
    self.setTranslation([x + y for x, y in zip(t, self.translation)])

  def addScale(self, s):
    assert len(s) == 3
    self.setScale([x + y for x, y in zip(s, self.scale)])

  def addRotation(self, r):
    assert len(r) == 3
    self.setRotation([x + y for x, y in zip(r, self.rotation)])

  # returns a list of 3d points, representing the triangles of the object transformed
  # by the translation, scale and rotation matrices
  def toPoints(self):
    ret = []

    # create transform matrix
    translateMatrix = matrix.makeTranslationMatrix(self.translation)
    scaleMatrix = matrix.makeScaleMatrix(self.scale)
    rotationMatrix = matrix.makeRotationMatrix(self.rotation)
    transformMatrix = translateMatrix * scaleMatrix * rotationMatrix
                      
    # transform each point
    for triangle in self.triangles: 
      retTriangle = []
      for vertex in triangle:
        retTriangle.append(matrix.transformPoint(vertex, transformMatrix))
      ret.append(retTriangle)

    return ret

  def __str__(self):
    # encode basic attributes 
    attributes = ('\tpigment { rgb ' + serializeVector(self.color) + ' }\n'
      + '\trotate ' + serializeVector(self.rotation) + '\n'
      + '\tscale ' + serializeVector(self.scale) + '\n'
      + '\ttranslate ' + serializeVector(self.translation) + '\n'
      + '\tfinish { \n'
      + '\t\tdiffuse ' + str(self.diffuseCoeff) + '\n'
      + '\t\tambient ' + str(self.ambientCoeff) + '\n'
      + '\t}\n')

    # encode triangle data
    trianglesString = ''
    for triangle in self.triangles:
      trianglesString += '\ttriangle {'
      for (i, vector) in enumerate(triangle):
        trianglesString += serializeVector(vector)
        if i + 1 < len(triangle):
          trianglesString += ', '
      trianglesString += '}\n'

    return ('mesh {\n'
      + trianglesString
      + attributes
      + '}\n')

  def getTranslation(self):
    return self.translation

  def getScale(self):
    return self.scale

  def getRotation(self):
    return self.rotation

  def getColor(self):
    return self.color

  def getTriangles(self):
    return self.triangles

"""
  A cube mesh spanning from [-0.5, -0.5, -0.5] to [0.5, 0.5, 0.5]
"""
class Cube(Shape):
  triangles = [
    # front 
    [[-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [-0.5, 0.5, 0.5]],
    [[0.5, 0.5, 0.5], [0.5, -0.5, 0.5], [-0.5, 0.5, 0.5]],

    # back
    [[-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [-0.5, 0.5, -0.5]],
    [[0.5, 0.5, -0.5], [0.5, -0.5, -0.5], [-0.5, 0.5, -0.5]],
    
    # left side
    [[-0.5, -0.5, -0.5], [-0.5, -0.5, 0.5], [-0.5, 0.5, -0.5]],
    [[-0.5, 0.5, 0.5], [-0.5, -0.5, 0.5], [-0.5, 0.5, -0.5]],

    # right side
    [[0.5, 0.5, -0.5], [0.5, -0.5, 0.5], [0.5, -0.5, -0.5]],
    [[0.5, 0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, -0.5]],

    # bottom side
    [[-0.5, -0.5, -0.5], [-0.5, -0.5, 0.5], [0.5, -0.5, -0.5]],
    [[0.5, -0.5, 0.5], [-0.5, -0.5, 0.5], [0.5, -0.5, -0.5]],

    # top side
    [[-0.5, 0.5, -0.5], [-0.5, 0.5, 0.5], [0.5, 0.5, -0.5]],
    [[0.5, 0.5, 0.5], [-0.5, 0.5, 0.5], [0.5, 0.5, -0.5]],
  ]

  def __init__(self):
    Shape.__init__(self, Cube.triangles)

"""
  A Cube with no front side.
  Spans from (-0.5, -0.5, -0.5) to (0.5, 0.5, 0.5)
"""
class ViewingBox(Shape):
  triangles = [
    # front 
    #[[-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [-0.5, 0.5, 0.5]],
    #[[0.5, 0.5, 0.5], [0.5, -0.5, 0.5], [-0.5, 0.5, 0.5]],

    # back
    #[[-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [-0.5, 0.5, -0.5]],
    #[[0.5, 0.5, -0.5], [0.5, -0.5, -0.5], [-0.5, 0.5, -0.5]],

    # left side
    [[-0.5, -0.5, -0.5], [-0.5, -0.5, 0.5], [-0.5, 0.5, -0.5]],
    [[-0.5, 0.5, 0.5], [-0.5, -0.5, 0.5], [-0.5, 0.5, -0.5]],

    # right side
    [[0.5, 0.5, -0.5], [0.5, -0.5, 0.5], [0.5, -0.5, -0.5]],
    [[0.5, 0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, -0.5]],

    # bottom side
    [[-0.5, -0.5, -0.5], [-0.5, -0.5, 0.5], [0.5, -0.5, -0.5]],
    [[0.5, -0.5, 0.5], [-0.5, -0.5, 0.5], [0.5, -0.5, -0.5]],

    # top side
    [[-0.5, 0.5, -0.5], [-0.5, 0.5, 0.5], [0.5, 0.5, -0.5]],
    [[0.5, 0.5, 0.5], [-0.5, 0.5, 0.5], [0.5, 0.5, -0.5]],
  ]

  def __init__(self):
    Shape.__init__(self, ViewingBox.triangles)


"""
  A sphere mesh centered at (0, 0, 0) with radius 0.5
"""
class Sphere(Shape):
  def __init__(self, rings=12, sectors=24):
    triangles = []

    # see http://gamedev.stackexchange.com/questions/16585/how-do-you-programmatically-generate-a-sphere
    for r in range(rings):
      theta1 = (r / float(rings)) * math.pi
      theta2 = ((r + 1) / float(rings)) * math.pi

      for s in range(sectors):
        phi1 = (s / float(sectors)) * math.pi * 2.0
        phi2 = ((s+1) / float(sectors)) * math.pi * 2.0

        def sphericalToCartesian(radius, theta, phi):#phi, theta):
          x = radius * math.sin(phi) * math.cos(theta)
          y = radius * math.sin(phi) * math.sin(theta)
          z = radius * math.cos(phi)
          return [x, y, z]

        v1 = sphericalToCartesian(1., theta1, phi1)
        v2 = sphericalToCartesian(1., theta1, phi2)
        v3 = sphericalToCartesian(1., theta2, phi2)
        v4 = sphericalToCartesian(1., theta2, phi1)

        if r == 0:
          triangles.append([v1, v3, v4])
          triangles.append([v1, v3, v2])
        elif r + 1 == rings:
          triangles.append([v3, v1, v2])
          triangles.append([v3, v1, v4])
          pass
        else:
          triangles.append([v1, v2, v4])
          triangles.append([v2, v3, v4])

    Shape.__init__(self, triangles)

