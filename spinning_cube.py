import core
import bulk_generate

if __name__ == '__main__':
  # setup camera
  camera = core.Camera([0.5, 0.5, -1.2], [0.5, 0.5, 1.])

  # setup light
  light = core.Light([2, 4, -3])

  # setup cube
  cube = core.Cube()
  cube.setTranslation([0.5, 0.5, 0.5])
  cube.setScale([0.4, 0.4, 0.4])
  cube.setRotation([30, 60, 10])
  cube.setMaterial('diffuse')

  frames = 50
  for i in range(frames):
    bulk_generate.generate('spin_cube', camera, [light], [cube], filePostfix=str(i), volumeDepth=5)
    # animate cube
    cube.addRotation([0, 1.0 / float(frames) * 360, 0])
