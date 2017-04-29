#!/usr/bin/env python

################################################################################
#
# Base utility module (rendering, timers).
# Written by Huki, file inception on 2015-07-12.
#
# TODO:
# - implement vertical sync
# - automatically detect initial window size
# - support right alignment of text
#
################################################################################

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import time

# timer variables
timer_start = time.time()
timer_cur, timer_last = 0.0, 0.0
timer_step = 0.0

frame_time, frame_time_last = 0.0, 0.0
frame_count, frame_count_last = 0, 0
frame_rate = 0

# id of the glut window
window = 0

# fullscreen toggle
fullscreen = False

################################################################################

# get the time elapsed since the last call
def UpdateTimers():
  global timer_cur, timer_last, timer_step
  timer_last, timer_cur = timer_cur, time.time()-timer_start
  timer_step = timer_cur - timer_last

# get the frame rate
def UpdateFrameRate():
  global frame_time, frame_time_last
  global frame_count, frame_count_last
  global frame_rate

  frame_time = timer_cur;
  diff = frame_time - frame_time_last
  if (diff > 0.5):
    frame_rate = (frame_count-frame_count_last) // diff;
    frame_time_last = frame_time;
    frame_count_last = frame_count;

  frame_count += 1

# render text
def RenderText(text, x, y):
  width, height = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
  x = int(float(x) * 9.0 * float(height)/float(width)) if width else 0
  y = int(float(y+1) * 15.0 * float(width)/float(height)) if height else 0

  glMatrixMode(GL_PROJECTION)
  glPushMatrix()
  glLoadIdentity()
  glOrtho(0.0, height, width, 0.0, -1.0, 1.0)

  glMatrixMode(GL_MODELVIEW)
  glPushMatrix()
  glLoadIdentity()
  glRasterPos(x, y)

  lines = 1
  for c in text:
    if c == '\n':
      glRasterPos(x, y*lines)
      lines += 1
    else:
      glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(c))

  glPopMatrix()
  glMatrixMode(GL_PROJECTION)
  glPopMatrix()
  glMatrixMode(GL_MODELVIEW)

# event loop
def EventLoop():
  UpdateTimers()
  glutPostRedisplay()

# dummy draw event
def HandleDraw():
  if __name__ == '__main__':
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

  RenderText('time elapsed: ' + '{:.3f}'.format(timer_cur), 0, 0)
  RenderText('time step: ' + '{:.4f}'.format(timer_step), 0, 1)
  RenderText('frame rate: ' + '{:.0f}'.format(frame_rate), 0, 2)

  UpdateFrameRate()
  glutSwapBuffers()

# resize event
def HandleResize(width, height):
  glViewport(0, 0, width, height)

# input event
def HandleInputs(*args):
  global fullscreen

  if args[0] == b'f':
    fullscreen = not fullscreen
    if (fullscreen):
      glutFullScreen()
    else:
      glutReshapeWindow(640, 480)

  elif args[0] == b'\x1b':
    glutDestroyWindow(window)
    sys.exit(0)

# initialize GL states
def InitGL():
  glClearColor(0.0, 0.0, 0.0, 0.0)
  glClearDepth(1.0)

# init glut window
def InitGLUT(argv):
  global window
  width, height = 640, 480

  glutInit(argv)
  glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

  glutInitWindowSize(width, height)
  glutInitWindowPosition(-1, -1)

  window = glutCreateWindow('Python OpenGL Window')
  if fullscreen:
    glutFullScreen()

  print('GL Version: ' + str(extensions.GLQuerier.getVersion()))

  glutIdleFunc(EventLoop)
  glutDisplayFunc(HandleDraw)
  glutReshapeFunc(HandleResize)
  glutKeyboardFunc(HandleInputs)

  HandleResize(width, height)

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
