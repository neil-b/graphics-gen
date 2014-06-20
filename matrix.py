"""
  Some matrix math functions

  requires numpy
"""

import math
import numpy.linalg

"""
  vector math
"""
def cross(v1, v2):
  x = v1[1]*v2[2] - v1[2]*v2[1]
  y = v1[2]*v2[0] - v1[0]*v2[2]
  z = v1[0]*v2[1] - v1[1]*v2[0]
  return [x, y, z]

def length(v):
  return math.sqrt(v[0]**2.0 + v[1]**2.0 + v[2]**2.0);

def normalize(v):
  ret = None
  l = length(v)
  if l > 0:
    ret = [x / l for x in v]
  return ret

def dot(a, b):
  return sum([x * y for x, y in zip(a, b)])

def add(a, b):
  return [x + y for x, y in zip(a, b)]

def sub(a, b):
  return [x - y for x, y in zip(a, b)]

"""
  matrix math
"""
def transformPoint(v, matrix):
  assert len(v) == 3
  point = v[:]
  point.append(1) # convert to homogenous 4d coordinate
  point = matrix.dot(numpy.array(point))
  # convert from numpy.array to list and from 4d to 3d and return
  return [x for x in point.tolist()][0][:3]

def transformVector(v, matrix):
  assert len(v) == 3
  vec = v[:]
  vec.append(0) # convert to homogenous 4d coordinate
  vec = matrix.dot(numpy.array(vec))
  # convert from numpy.array to list and from 4d to 3d and return
  return [x for x in vec.tolist()][0][:3]


def makeScaleMatrix(s):
  return numpy.matrix([
    [s[0], 0., 0., 0.],
    [0., s[1], 0., 0.],
    [0., 0., s[2], 0.],
    [0., 0., 0., 1.]
  ])

def makeTranslationMatrix(t):
  return numpy.matrix([
    [1., 0., 0., t[0]],
    [0., 1., 0., t[1]],
    [0., 0., 1., t[2]],
    [0., 0., 0., 1.]
  ])

def makeXRotationMatrix(theta):
  ct = math.cos(math.radians(theta))
  st = math.sin(math.radians(theta))
  return numpy.matrix([
    [1., 0., 0., 0.],
    [0., ct, st, 0.],
    [0., -st, ct, 0.],
    [0., 0., 0., 1.]
  ])

def makeYRotationMatrix(theta):
  ct = math.cos(math.radians(theta))
  st = math.sin(math.radians(theta))
  return numpy.matrix([
    [ct, 0., st, 0.],
    [0., 1., 0., 0.],
    [-st, 0., ct, 0.],
    [0., 0., 0., 1.]
  ])

def makeZRotationMatrix(theta):
  ct = math.cos(math.radians(theta))
  st = math.sin(math.radians(theta))
  return numpy.matrix([
    [ct, st, 0, 0],
    [-st, ct, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
  ])

def makeRotationMatrix(thetas):
  return (makeXRotationMatrix(thetas[0]) 
          * makeYRotationMatrix(thetas[1])
          * makeZRotationMatrix(thetas[2]))

