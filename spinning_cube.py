#!/usr/bin/env python

################################################################################
#
# Spinning cube demo.
# Written by Huki, file inception on 2015-07-12.
#
# TODO:
# - Draw using polygons instead of lines.
# - Use the mouse movement to rotate the cube.
#
################################################################################

import Base
from Base import *

# vertices and edge indices of our cube
vertices = (
  ( 1, -1, -1),
  ( 1,  1, -1),
  (-1,  1, -1),
  (-1, -1, -1),
  ( 1, -1,  1),
  ( 1,  1,  1),
  (-1, -1,  1),
  (-1,  1,  1)
)

edges = (
  (0, 1),
  (0, 3),
  (0, 4),
  (2, 1),
  (2, 3),
  (2, 7),
  (6, 3),
  (6, 4),
  (6, 7),
  (5, 1),
  (5, 4),
  (5, 7)
)

################################################################################

# render the cube
def RenderCube():
  glBegin(GL_LINES)
  for edge in edges:
    for v in edge:
      glVertex(vertices[v])
  glEnd()

# display event
def HandleDraw():
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

  angle = Base.timer_step * 100.0
  glRotate(angle, 3, 1, 1)
  RenderCube()

  Base.HandleDraw()

# resize event
def HandleResize(width, height):
  Base.HandleResize(width, height)

  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)

  glMatrixMode(GL_MODELVIEW)
  glLoadIdentity()

  glTranslate(0.0, 0.0, -5.0)

# the entry point
def main():
  InitGLUT(sys.argv)
  InitGL()
  
  glutDisplayFunc(HandleDraw)
  glutReshapeFunc(HandleResize)
  glutMainLoop()

################################################################################

# call the main function
if __name__ == '__main__':
  main()
