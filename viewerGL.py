#!/usr/bin/env python3
import OpenGL.GL as GL
import glfw
import pyrr
import numpy as np
from cpe3d import Object3D
from zombie import Zombies
from bullet import Bullets
import time

class ViewerGL:
    def __init__(self):


        self.lastX, self.lastY = 0, 0



        # initialisation de la librairie GLFW
        glfw.init()
        # paramétrage du context OpenGL
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        # création et paramétrage de la fenêtre
        glfw.window_hint(glfw.RESIZABLE, False)
        self.window = glfw.create_window(900, 900, 'OpenGL', None, None)
        # paramétrage de la fonction de gestion des évènements
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.set_mouse_button_callback(self.window, self.click_callback)

        #souris
        glfw.set_cursor_pos_callback(self.window, self.mouse_callback)
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

        # activation du context OpenGL pour la fenêtre
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        # activation de la gestion de la profondeur
        GL.glEnable(GL.GL_DEPTH_TEST)
        # choix de la couleur de fond
        GL.glClearColor(0.5, 0.6, 0.9, 1.0)
        print(f"OpenGL: {GL.glGetString(GL.GL_VERSION).decode('ascii')}")

        self.objs = []
        self.touch = {}

        if (glfw.raw_mouse_motion_supported()):
            glfw.set_input_mode(self.window, glfw.RAW_MOUSE_MOTION, glfw.TRUE);
        
    def run(self):
        # boucle d'affichage
        while not glfw.window_should_close(self.window):
            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            self.update_key()

            self.update_zombie()
            self.update_bullet()
            self.update_player()

            for obj in self.objs:
                GL.glUseProgram(obj.program)
                if type(obj) == Object3D:
                    self.update_camera(obj.program)
                obj.draw()

            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
            # gestion des évènements
            glfw.poll_events()
        
    def key_callback(self, win, key, scancode, action, mods):
        # sortie du programme si appui sur la touche 'échappement'
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(win, glfw.TRUE)
        self.touch[key] = action

    def click_callback(self, win, key, action, mods):
        self.touch[key] = action

    
    def add_object(self, obj):
        self.objs.append(obj)

    def set_zombie(self, zombies):  
        self.zombies = zombies
        for zombie in self.zombies.all_zombies:
            self.objs.append(zombie.object)

    def delete_zombie(self, zombie):
        for i in range(len(self.objs)):
            if self.objs[i] == zombie.object:
                self.zombies.kill_zombie(zombie)
                del self.objs[i]
                break
    
    def update_zombie(self):
        self.zombies.update()
        for zombie in self.zombies.all_zombies:
            if zombie.alive == False:
                self.delete_zombie(zombie)
                self.add_zombie()
    
    def add_zombie(self):
        zombie = self.zombies.add_zombie()
        self.objs.append(zombie.object)

    def init_bullets(self, bullets):
        self.bullets = bullets

    def fire_bullet(self):
        bullet = self.bullets.add_bullet()
        self.objs.append(bullet.object)
    
    def update_bullet(self):
        self.bullets.update(self.zombies)
        for bullet in self.bullets.all_bullets:
            if bullet.alive == False:
                self.delete_bullet(bullet)

    def delete_bullet(self, bullet):
        for i in range(len(self.objs)):
            if self.objs[i] == bullet.object:
                self.bullets.destroy_bullet(bullet)
                del self.objs[i]
                break
    
    def init_player(self,player):
        self.player = player
        self.objs.append(player.object)
    
    def update_player(self):
        self.player.update()

    def set_camera(self, cam):
        self.cam = cam

    def update_camera(self, prog):
        GL.glUseProgram(prog)
        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "translation_view")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : translation_view")
        # Modifie la variable pour le programme courant
        translation = -self.cam.transformation.translation
        GL.glUniform4f(loc, translation.x, translation.y, translation.z, 0)

        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "rotation_center_view")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_center_view")
        # Modifie la variable pour le programme courant
        rotation_center = self.cam.transformation.rotation_center
        GL.glUniform4f(loc, rotation_center.x, rotation_center.y, rotation_center.z, 0)

        rot = pyrr.matrix44.create_from_eulers(-self.cam.transformation.rotation_euler)
        loc = GL.glGetUniformLocation(prog, "rotation_view")
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_view")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, rot)
    
        loc = GL.glGetUniformLocation(prog, "projection")
        if (loc == -1) :
            print("Pas de variable uniforme : projection")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, self.cam.projection)

    def update_key(self):
        if glfw.KEY_W in self.touch and self.touch[glfw.KEY_W] > 0:
            if glfw.KEY_LEFT_SHIFT in self.touch and self.touch[glfw.KEY_LEFT_SHIFT] > 0:
                self.objs[0].transformation.translation += \
                    pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, 0.3]))
            else:
                self.objs[0].transformation.translation += \
                    pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, 0.2]))
        if glfw.KEY_S in self.touch and self.touch[glfw.KEY_S] > 0:
            self.objs[0].transformation.translation -= \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, 0.2]))
        if glfw.KEY_A in self.touch and self.touch[glfw.KEY_A] > 0:
            self.objs[0].transformation.translation += \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0.1, 0, 0]))
        if glfw.KEY_D in self.touch and self.touch[glfw.KEY_D] > 0:
            self.objs[0].transformation.translation -= \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0.1, 0, 0]))

        if glfw.MOUSE_BUTTON_RIGHT in self.touch and self.touch[glfw.MOUSE_BUTTON_RIGHT]:
            self.SENSI=0.0005
            self.cam.transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy() 
            self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += np.pi
            self.cam.transformation.rotation_center = self.objs[0].transformation.translation + self.objs[0].transformation.rotation_center
            self.cam.transformation.translation = self.objs[0].transformation.translation + pyrr.Vector3([0, 1, 2])
            
        else:
            self.SENSI=0.005
            self.cam.transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy() 
            self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += np.pi
            self.cam.transformation.rotation_center = self.objs[0].transformation.translation + self.objs[0].transformation.rotation_center
            self.cam.transformation.translation = self.objs[0].transformation.translation + pyrr.Vector3([0, 1, 5])
            

        # if glfw.KEY_Q in self.touch and self.touch[glfw.KEY_Q] > 0:
        
        #     else:
        #         self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] -= 0.1
        # if glfw.KEY_D in self.touch and self.touch[glfw.KEY_D] > 0:
        #     if glfw.KEY_LEFT_CONTROL in self.touch and self.touch[glfw.KEY_LEFT_CONTROL]:
        #         self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] += 0.015
        #     else:
        #         self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] += 0.1


        #BOUGER LA CAM ------------------------
        # if glfw.KEY_I in self.touch and self.touch[glfw.KEY_I] > 0:
        #     self.cam.transformation.rotation_euler[pyrr.euler.index().roll] -= 0.1
        # if glfw.KEY_K in self.touch and self.touch[glfw.KEY_K] > 0:
        #     self.cam.transformation.rotation_euler[pyrr.euler.index().roll] += 0.1
        # if glfw.KEY_J in self.touch and self.touch[glfw.KEY_J] > 0:
        #     self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] -= 0.1
        # if glfw.KEY_L in self.touch and self.touch[glfw.KEY_L] > 0:
        #     self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += 0.1

        if glfw.MOUSE_BUTTON_LEFT in self.touch and self.touch[glfw.MOUSE_BUTTON_LEFT] > 0:
            self.fire_bullet()

        # if glfw.KEY_SPACE in self.touch and self.touch[glfw.KEY_SPACE] > 0:

        
    def mouse_callback(self, window, xpos, ypos):

        xoffset = (xpos - self.lastX)*self.SENSI
        yoffset = (ypos - self.lastY)*self.SENSI

        self.lastX = xpos
        self.lastY = ypos

        roll = self.cam.transformation.rotation_euler[pyrr.euler.index().roll]

        if roll + yoffset >= -0.2 and roll + yoffset <= 1:
            self.cam.transformation.rotation_euler[pyrr.euler.index().roll] += yoffset
        self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += xoffset

        #Forcer personnage à suivre la cam
        self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] = self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] + np.pi
