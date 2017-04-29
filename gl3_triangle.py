#!/usr/bin/env python

################################################################################
#
# OpenGL 3 triangle demo.
# Written by Huki, file inception on 2015-07-12.
#
# TODO:
# - Support OpenGL 2 hardware by checking for extensions.
#
################################################################################

import Base
from Base import *

# vertex and color data
vertices = (
  -1.0, 0.0, 0.0,
   0.0, 1.0, 0.0,
   0.0, 0.0, 0.0
)

vertices2 = (
  0.0,  0.0, 0.0,
  0.0, -1.0, 0.0,
  1.0,  0.0, 0.0 
)

colors = (
  1.0, 0.0, 0.0,
  0.0, 1.0, 0.0,
  0.0, 0.0, 1.0
)

# vertex arrays for each triangle
vertex_arrays = None

# vertex coord and color buffers
vertex_buffers = None

# the shader program
program = None

################################################################################

# init shaders
def InitShaders():
  if not glInitGl30VERSION():
    print('OpenGL 3+ support required!')
    return

  def loadFile(filename):
    with open(filename) as fp:
      return fp.read()

  vs = glCreateShader(GL_VERTEX_SHADER)
  ps = glCreateShader(GL_FRAGMENT_SHADER)

  glShaderSource(vs, loadFile('data/minimal.vert'))
  glShaderSource(ps, loadFile('data/minimal.frag'))

  glCompileShader(vs)
  if glGetShaderiv(vs, GL_COMPILE_STATUS) != GL_TRUE:
    print('Vertex shader not compiled!')
    print(glGetShaderInfoLog(vs))
    return
  glCompileShader(ps)
  if glGetShaderiv(ps, GL_COMPILE_STATUS) != GL_TRUE:
    print('Pixel shader not compiled!')
    print(glGetShaderInfoLog(ps))
    return

  global program
  program = glCreateProgram()

  glBindAttribLocation(program, 0, 'in_Position')
  glBindAttribLocation(program, 1, 'in_Color')

  glAttachShader(program, vs)
  glAttachShader(program, ps)

  glLinkProgram(program)


# initialize GL states
def InitGL():
  global vertex_arrays, vertex_buffers
  vertex_arrays = glGenVertexArrays(2)
  vertex_buffers = glGenBuffers(3)

  def arrayType(data):
    return (GLfloat * len(data))(*data)

  glBindVertexArray(vertex_arrays[0])
  glBindBuffer(GL_ARRAY_BUFFER, vertex_buffers[0])
  glBufferData(GL_ARRAY_BUFFER, arrayType(vertices), GL_STATIC_DRAW)
  glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
  glEnableVertexAttribArray(0)

  glBindBuffer(GL_ARRAY_BUFFER, vertex_buffers[1])
  glBufferData(GL_ARRAY_BUFFER, arrayType(colors), GL_STATIC_DRAW)
  glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
  glEnableVertexAttribArray(1)

  glBindVertexArray(vertex_arrays[1])
  glBindBuffer(GL_ARRAY_BUFFER, vertex_buffers[2])
  glBufferData(GL_ARRAY_BUFFER, arrayType(vertices2), GL_STATIC_DRAW)
  glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
  glEnableVertexAttribArray(0)

  glBindVertexArray(0)
  InitShaders()

# display event
def HandleDraw():
  glClear(GL_COLOR_BUFFER_BIT)
  if program:
    glUseProgram(program)

  glBindVertexArray(vertex_arrays[0])
  glDrawArrays(GL_TRIANGLES, 0, 3)
  
  glBindVertexArray(vertex_arrays[1])
  glVertexAttrib3f(1, 1.0, 0.0, 0.0)
  glDrawArrays(GL_TRIANGLES, 0, 3)

  glBindVertexArray(0)
  glUseProgram(0)
  Base.HandleDraw()

# the entry point
def main():
  InitGLUT(sys.argv)
  InitGL()
  
  glutDisplayFunc(HandleDraw)
  glutMainLoop()

################################################################################

# call the main function
if __name__ == '__main__':
  main()
