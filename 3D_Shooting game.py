from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

# Camera-related variables
camera_pos = (0,500,500)
camera_mode = 'third'  

fovY = 120
GRID_LENGTH = 600
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 800

rand_var=423
cheat_mode = False
cheat_vision = False
player_pos = [0.0, 0.0]  # x, y
gun_angle = 0  # in degrees
player_life = 5
bullets_missed = 0
score = 0
game_over = False

bullets = []  # list of (x, y, angle)
enemies = []  # list of (x, y, scale_dir, scale)

def init_enemies():
    global enemies
    enemies = []
    for _ in range(5):
        spawn_enemy()

def spawn_enemy():
    x = random.randint(-GRID_LENGTH//2, GRID_LENGTH//2)
    y = random.randint(-GRID_LENGTH//2, GRID_LENGTH//2)
    enemies.append([x, y, 1, 1.0])

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_grid():
    tile_size = 60
    glBegin(GL_QUADS)
    for x in range(-GRID_LENGTH, GRID_LENGTH, tile_size):
        for y in range(-GRID_LENGTH, GRID_LENGTH, tile_size):
            if ((x + y) // tile_size) % 2 == 0:
                glColor3f(0.8, 0.8, 0.8)
            else:
                glColor3f(0.7, 0.5, 1.0)
            glVertex3f(x, y, 0)
            glVertex3f(x + tile_size, y, 0)
            glVertex3f(x + tile_size, y + tile_size, 0)
            glVertex3f(x, y + tile_size, 0)
    glEnd()

def draw_player():
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], 0)

    # --- Legs ---
    glPushMatrix()
    glColor3f(0.4, 0.2, 0.1)  
    glTranslatef(-7, 0, 0)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 4, 4, 20, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.4, 0.2, 0.1) # Brown
    glTranslatef(7, 0, 0)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 4, 4, 20, 10, 10)
    glPopMatrix()

    # --- Body ---
    glPushMatrix()
    glTranslatef(0, 0, 20)
    glColor3f(0, 1, 0)  # Green
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 10, 30, 10, 10)
    glPopMatrix()

    # --- Head ---
    glPushMatrix()
    glTranslatef(0, 0, 55)
    glColor3f(1, 0.5, 0)  # Orange
    gluSphere(gluNewQuadric(), 10, 10, 10)
    glPopMatrix()

    # --- Gun ---
    glPushMatrix()
    glTranslatef(0, 0, 40)
    glColor3f(0, 0, 1)  # Blue
    glRotatef(gun_angle, 0, 0, 1)
    glTranslatef(30, 0, 0)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 3, 3, 30, 10, 10)
    glPopMatrix()

    glPopMatrix()



def draw_enemy(x, y, scale):
    glPushMatrix()
    glTranslatef(x, y, 20)
    glScalef(scale, scale, scale)
    glColor3f(1, 0, 0)
    quadric = gluNewQuadric()
    gluSphere(quadric, 20, 10, 10)
    glTranslatef(0, 0, 20)
    glColor3f(0.5, 0, 0)
    gluSphere(quadric, 10, 10, 10)
    glPopMatrix()

def draw_bullet(x, y):
    glPushMatrix()
    glTranslatef(x, y, 30)
    glColor3f(1, 1, 0)
    glutSolidCube(8)
    glPopMatrix()

def draw_scene():
    draw_grid()
    for x, y, sdir, scale in enemies:
        draw_enemy(x, y, scale)
    for x, y, a in bullets:
        draw_bullet(x, y)
    if not game_over:
        draw_player()


def update_bullets():
    global bullets, score, bullets_missed,game_over
    new_bullets = []
    for b in bullets:
        x, y, a = b
        x += 10 * math.cos(math.radians(a))
        y += 10 * math.sin(math.radians(a))
        hit = False
        for e in enemies:
            if math.hypot(x - e[0], y - e[1]) < 25:
                enemies.remove(e)
                spawn_enemy()
                score += 1
                hit = True
                break
        if not hit:
            if abs(x) < GRID_LENGTH and abs(y) < GRID_LENGTH:
                new_bullets.append((x, y, a))
            else:
                bullets_missed += 1
                if bullets_missed>=10:
                    game_over = True
                    
    bullets = new_bullets

def update_enemies():
    global player_life, game_over
    for e in enemies:
        dx = player_pos[0] - e[0]
        dy = player_pos[1] - e[1]
        dist = math.hypot(dx, dy)
        if dist > 0:
            e[0] += 0.05 * dx / dist
            e[1] += 0.05 * dy / dist
        if dist < 30 and not game_over:
            player_life -= 1
            enemies.remove(e)
            spawn_enemy()
            if player_life <= 0:
                game_over = True
          
        e[3] += 0.03 * e[2]
        if e[3] > 1.2 or e[3] < 0.8:
            e[2] *= -1


def update_cheat_mode():
    global gun_angle
    if cheat_mode and not game_over:
        gun_angle += .4
        if gun_angle >= 360:
            gun_angle = 0

        # Check if any enemy is in line of fire
        for e in enemies:
            dx = e[0] - player_pos[0]
            dy = e[1] - player_pos[1]
            angle_to_enemy = math.degrees(math.atan2(dy, dx)) % 360
            angle_diff = abs((gun_angle - angle_to_enemy + 180) % 360 - 180)

            if angle_diff <0.16:  # small margin to allow for close alignment
                fire_bullet()

def fire_bullet():
    
    bullets.append((player_pos[0] + 30*math.cos(math.radians(gun_angle)),
                    player_pos[1] + 30*math.sin(math.radians(gun_angle)),
                    gun_angle))

def restart_game():
    global player_life, bullets, enemies, bullets_missed, score, game_over
    player_life = 5
    bullets = []
    bullets_missed = 0
    score = 0
    game_over = False
    init_enemies()

def keyboardListener(key, x, y):
    global gun_angle, player_pos, cheat_mode, cheat_vision, game_over
    if key == b'a':
        gun_angle += 2
    elif key == b'd':
        gun_angle -= 2
    elif key == b'w':
        player_pos[0] += 6 * math.cos(math.radians(gun_angle))
        player_pos[1] += 6 * math.sin(math.radians(gun_angle))
    elif key == b's':
        player_pos[0] -= 6 * math.cos(math.radians(gun_angle))
        player_pos[1] -= 6 * math.sin(math.radians(gun_angle))
    elif key == b'c':
        cheat_mode = not cheat_mode
    elif key == b'v':
        
        if camera_mode == 'first' and cheat_mode and cheat_vision:
            cheat_vision = False
        else:
            cheat_vision=True
    elif key == b'r' and game_over:
        restart_game()

def specialKeyListener(key, x, y):
    global camera_pos
    x, y, z = camera_pos
    if key == GLUT_KEY_LEFT:
        x -= 10
    elif key == GLUT_KEY_RIGHT:
        x += 10
    elif key == GLUT_KEY_UP:
        z += 10
    elif key == GLUT_KEY_DOWN:
        z -= 10
    camera_pos = (x, y, z)

def mouseListener(button, state, x, y):
    global camera_mode
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and game_over==False:
        fire_bullet()
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        camera_mode = 'first' if camera_mode == 'third' else 'third'

def setupCamera():
    global camera_mode, cheat_mode, cheat_vision
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if camera_mode == 'third':
        x, y, z = camera_pos
        gluLookAt(x, y, z, player_pos[0], player_pos[1], 0, 0, 0, 1)
    else:
        # First-person view
        eye_x = player_pos[0]
        eye_y = player_pos[1]
        eye_z = 120

        # Only follow gun if cheat_mode and cheat_vision are both on
        if camera_mode == 'first' and cheat_mode and cheat_vision:
            cx = player_pos[0] + 100 * math.cos(math.radians(gun_angle))
            cy = player_pos[1] + 100 * math.sin(math.radians(gun_angle))
        else:
            cx = player_pos[0] + math.cos(math.radians(gun_angle))
            cy = player_pos[1] + math.sin(math.radians(gun_angle))

        gluLookAt(eye_x, eye_y, eye_z, cx, cy, 120, 0, 0, 1)

def idle():
    update_bullets()
    update_enemies()
    update_cheat_mode()
    glutPostRedisplay()

def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 800)  # Set viewport size
    setupCamera() # Configure camera perspective
    # Draw a random points
    glPointSize(20)
    glBegin(GL_POINTS)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glEnd()

    draw_scene()
    if game_over==False:
        draw_text(10, 770, f"Player Life Remaining: {player_life}")
        draw_text(10, 740, f"Game Score:  Score: {score}")
        draw_text(10, 710, f"Player Bullet Missed:  {bullets_missed}")
    else:
        draw_text(10, 770, f"Game is over. Your score is {score}")
        draw_text(10, 740, f"Press "R" to RESTART the Game")
    glutSwapBuffers()

    
# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"Bullet Frenzy 3D")
    
    init_enemies()
    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically
    
    glutMainLoop() # Enter the GLUT main loop

if __name__ == '__main__':
    main()
