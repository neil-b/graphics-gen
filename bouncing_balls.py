import core
import bulk_generate
from random import uniform

if __name__ == '__main__':
  # setup camera 
  camera = core.Camera([0.5, 0.5, -1.2], [0.5, 0.5, 1.])

  # setup light
  light = core.Light([2, 4, -3])

  # setup box from (0,0,0) to (1,1,1) to hold the balls
  box = core.ViewingBox()
  box.setTranslation([0.5, 0.5, 0.5])

  # add balls
  balls = []
  numBalls = 10
  ballDiameter = 0.07
  ballRadius = ballDiameter / 2.0
  for i in range(numBalls):
    ball = core.Sphere()
    ball.setScale([ballDiameter, ballDiameter, ballDiameter])
    ball.setColor([1.0, 1.0, 0.0])

    # add these two attributes to the Sphere class:
    ball.velocity = [uniform(-0.05, 0.05), uniform(-0.05, 0.05), uniform(-0.05, 0.05)]
    ball.position = [uniform(0.0 + ballRadius, 1.0 - ballRadius),
                      uniform(0.0 + ballRadius, 1.0 - ballRadius),
                      uniform(0.0 + ballRadius, 1.0 - ballRadius)]

    balls.append(ball)

  frames = 50
  for i in range(frames):
    # make the balls move and bounce:
    for ball in balls:
      # add velocity to position
      ball.position = [p + v for p, v in zip(ball.position, ball.velocity)]
      # flip a velocity dimension if bumping into wall
      ball.velocity = [-v if p + ballDiameter >= 1.0 or p - ballDiameter <= 0 else v
                         for p, v in zip(ball.position, ball.velocity)]

      # change velocity if bumping into ball:
      for ball2 in balls:
        if ball2.position != ball.position: # ignore collisions with itself
          from matrix import length
          # if two balls collide:
          if length([p1 - p2 for p1, p2 in zip(ball.position, ball2.position)]) < ballRadius * 2:
            ball.velocity = [-v for v in ball.velocity]

      # apply changes to position
      ball.setTranslation(ball.position)

    # render
    shapes = balls[:]
    shapes.append(box)
    bulk_generate.generate('bouncing_balls', camera, [light], shapes, filePostfix=str(i), volumeDepth=5)

