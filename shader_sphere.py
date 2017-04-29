#!/usr/bin/env python

################################################################################
#
# Some shaded objects using pyOpenGL helper utilities.
# Written by Huki, file inception on 2015-07-12.
#
# TODO:
# - Implement a camera system.
# - Modify shaders at runtime.
#
################################################################################

import Base
from Base import *

from OpenGL.GL.shaders import *

# the shader program
program = None
vertex_shader = '''
  varying vec3 normal;
  void main() {
    normal = gl_NormalMatrix * gl_Normal;
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
  }
'''
pixel_shader = '''
  varying vec3 normal;
  void main() {
    float intensity;
    vec4 color;
    vec3 n = normalize(normal);
    vec3 l = normalize(gl_LightSource[0].position).xyz;

    // quantize to 5 steps (0, .25, .5, .75 and 1)
    intensity = (floor(dot(l, n) * 4.0) + 1.0)/4.0;
    color = vec4(intensity*1.0, intensity*0.5, intensity*0.5,intensity*1.0);

    gl_FragColor = color;
  }
'''

################################################################################

# init shaders
def InitShaders():
  if not glUseProgram:
    print('Missing shader extensions!')
    return

  global program
  program = compileProgram(
    compileShader(vertex_shader, GL_VERTEX_SHADER),
    compileShader(pixel_shader, GL_FRAGMENT_SHADER),
  )

# initialize GL states
def InitGL():
  glClearColor(0.0, 0.0, 0.0, 0.0)
  glClearDepth(1.0)
  glDepthFunc(GL_LESS)
  glEnable(GL_DEPTH_TEST)
  glShadeModel(GL_SMOOTH)

  InitShaders()

# display event
def HandleDraw():
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
  if program:
    glUseProgram(program)

  glLoadIdentity()
  glTranslate(-1.5, 0.0, -6.0)
  glutSolidSphere(1.0, 32, 32)

  glTranslate(1, 0, 2)
  glutSolidCube(1.0)

  glUseProgram(0)
  Base.HandleDraw()

# resize event
def HandleResize(width, height):
  Base.HandleResize(width, height)

  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)

  glMatrixMode(GL_MODELVIEW)
  glLoadIdentity()

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
