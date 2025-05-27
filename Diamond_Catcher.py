from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

class AABB:
 def __init__(self,x1,x2,y1,y2):
    self.x1=x1
    self.x2=x2
    self.y1=y1
    self.y2=y2

 def collides_with(self,other):
    return ((self.x1<other.x2<self.x2) or (self.x1<other.x1<self.x2)) and (self.y1<other.y2<self.y2)

def draw_line(x1,y1,x2,y2):
   zone=find_zone(x1, y1, x2, y2)
   x_1,y_1=convert_to_z0(x1,y1,zone)
   x_2,y_2=convert_to_z0(x2,y2,zone)
   dx=x_2-x_1
   dy=y_2-y_1
   d=(2*dy)-dx
   inc_E=2*dy
   inc_NE=2*(dy-dx)
   x=x_1
   y=y_1

   while x<=x_2:
       c_x,c_y=convert_to_og(zone,x,y)
       glPointSize(2)
       glBegin(GL_POINTS)
       glVertex2f(c_x,c_y)
       glEnd()
       if d<=0:
           d+=inc_E
       else:
           d+=inc_NE
           y+=1
       x+=1

def find_zone(x1,y1,x2,y2):
   dx=x2-x1
   dy=y2-y1

   if abs(dx)>abs(dy):
       if dx>0:
           if dy>0:
               return 0
           else:
               return 7
       else:
           if dy>0:
               return 3
           else:
               return 4
   else:
       if dx>0:
           if dy>0:
               return 1
           else:
               return 6
       else:
           if dy>0:
               return 2
           else:
               return 5

def convert_to_og(og,x,y):
   if og==0:
       return x,y
   if og==1:
       return y,x
   if og==2:
       return -y,x
   if og==3:
       return -x,y
   if og==4:
       return -x,-y
   if og==5:
       return -y,-x
   if og==6:
       return y,-x
   if og==7:
       return x,-y

def convert_to_z0(x,y,zone):
   if zone==0:
       return x,y
   if zone==1:
       return y,x
   if zone==2:
       return -y,x
   if zone==3:
       return -x,y
   if zone==4:
       return -x,-y
   if zone==5:
       return -y,-x
   if zone==6:
       return -y,x
   if zone==7:
       return x,-y

def reset_diamond():
    global diamond_x, diamond_y,color
    diamond_x=random.randint(20, 480)
    diamond_y=620
    color=[random.uniform(0.4,1),random.uniform(0.4,1),random.uniform(0.4,1)]
    
r,g,b=[random.uniform(0.4,1),random.uniform(0.4,1),random.uniform(0.4,1)]
color=(r,g,b)
catcher_x=230
catcher_y=50
diamond_x=random.randint(20,480)
diamond_y=620
catcher_speed=10
diamond_speed=0.3

box1=AABB(catcher_x-30,catcher_x+40,catcher_y-49,catcher_y-39)
box2=AABB(diamond_x-10,diamond_x+10,diamond_y+10,diamond_y-10)

collision=False
over=False
score=0
catcher_color=(1,1,1)
restart=False
play=True

def lower_box():
   global catcher_x,catcher_y,collision,box1,box2
   global diamond_y,score

   glColor3f(*catcher_color)
   draw_line(catcher_x-30,catcher_y-39,catcher_x+50,catcher_y-39)
   draw_line(catcher_x-20,catcher_y-49,catcher_x+40,catcher_y-49)
   
   draw_line(catcher_x+50,catcher_y-40,catcher_x+40,catcher_y-49)
   draw_line(catcher_x-30,catcher_y-40,catcher_x-20,catcher_y-49)
   
def diamond_box():
   global diamond_x, diamond_y
   glColor3f(*color)
   draw_line(diamond_x-7, diamond_y, diamond_x, diamond_y+7)
   draw_line(diamond_x, diamond_y+7, diamond_x+7, diamond_y)
   draw_line(diamond_x+7, diamond_y, diamond_x, diamond_y-7)
   draw_line(diamond_x-7, diamond_y, diamond_x, diamond_y-7)

def restart_game():
   global score,diamond_speed,diamond_x,diamond_y,color,catcher_color,restart,catcher_x,catcher_y
   diamond_speed=0.3
   score=0
   catcher_x=230
   catcher_y=50
   reset_diamond()
   catcher_color=(1.0,1.0,1.0)
   restart=False

def mouseListener(button,state,x,y):
   global restart,play,score,over
   if button==GLUT_LEFT_BUTTON and state==GLUT_DOWN and 10<x<60 and 1<y<70:
       print('Starting over!')
       restart=True
       over=False

   elif button==GLUT_LEFT_BUTTON and state==GLUT_DOWN and 220<x<260 and 10<y<70:
       if play==False:
           play=True
       else:
           play=False

   elif button==GLUT_LEFT_BUTTON and state==GLUT_DOWN and 440<x<480 and 10<y<60:
       print("Goodbye! Your final score is:",score)
       glutLeaveMainLoop()


def keyboard_special_keys(key,x,y):
   global catcher_x,catcher_y

   if not over:
       if play==True:
        if key==GLUT_KEY_LEFT and catcher_x>30:
            catcher_x-=catcher_speed
        elif key==GLUT_KEY_RIGHT and catcher_x<450:
            catcher_x+=catcher_speed

   glutPostRedisplay()

def animate():
   global diamond_x,diamond_y, diamond_speed,score,restart,play,over,catcher_color
   if not over and play:
       check_collision()
       if restart:
           restart_game()
       if diamond_y<=0:
           over=True
           catcher_color=(1,0,0)
           print('Game Over! Score:',score)
       diamond_y-=diamond_speed

   global box2, box1
   box1=AABB(catcher_x-30,catcher_x+40,catcher_y-49, catcher_y-39)
   box2=AABB(diamond_x-7,diamond_x+7,diamond_y+7,diamond_y-7)
   glutPostRedisplay()

def check_collision():
   global box1,box2,collision, score,catcher_y,diamond_y,catcher_color,diamond_x,diamond_speed,over, play

   if box1.collides_with(box2):
       collision=True
       score+=1
       print("Score:",score)
       reset_diamond()
       box2=AABB(diamond_x-7, diamond_x+7, 550+7, 550-7)
       diamond_speed+=0.1

   else:
       collision=False

       if diamond_y<catcher_y-39:
           over=True
           catcher_color=(1,0,0)
           print(f"Game Over! Score: {score}")
           
def result():
   glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
   glLoadIdentity()
   iterate()
   glColor3f(1.0,1.0,1.0)
   if over==False:
       diamond_box()
   lower_box()

   #drawing restart_button
   glColor3f(0.0,131,141)

   draw_line(10,660,30,680)
   draw_line(10,660,60,660)
   draw_line(10,660,30,640)

   # drawing play_button
   glColor3f(1.0,0.75,0)

   if play:
       draw_line(240,670,240,630)
       draw_line(260,670,260,630)
   else:
       draw_line(220,670,220,630)
       draw_line(220,670,260,650)
       draw_line(220,630,260,650)

   glColor3f(1,0,0)

   draw_line(440,640,480,670)
   draw_line(440,670,480,640)
   glutSwapBuffers()
def iterate():
   glViewport(0,0,500,700)
   glMatrixMode(GL_PROJECTION)
   glLoadIdentity()
   glOrtho(0.0,500,0.0,700,0.0,1.0)
   glMatrixMode(GL_MODELVIEW)
   glLoadIdentity()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500,700)
glutInitWindowPosition(0,0)
wind=glutCreateWindow(b"OpenGL Coding Practice")
glutDisplayFunc(result)
glutIdleFunc(animate)
glutSpecialFunc(keyboard_special_keys)
glutMouseFunc(mouseListener)
glEnable(GL_DEPTH_TEST)
glutMainLoop()

