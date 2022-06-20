#!/usr/bin/env python3
import OpenGL.GL as GL
import glfw
import pyrr
import numpy as np
from cpe3d import Object3D
import glutils
from zombie import Zombies
from bullet import Bullets
import time

class ViewerGL:
    def __init__(self):

        self.WIDTH = 1024
        self.HEIGHT = 768
        self.lastX, self.lastY = 0, 0
        self.SENSI = 0.005

        self.vie = None
        self.score = None
        self.score_end = None
        self.score_chiffre = 0
        self.scene = 0

        self.texte_timer = None
        self.temps_partie = 30
        self.temps_depart = None
        self.temps_pause = None



        # initialisation de la librairie GLFW
        glfw.init()
        # paramétrage du context OpenGL
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        # création et paramétrage de la fenêtre
        glfw.window_hint(glfw.RESIZABLE, False)
        self.window = glfw.create_window(self.WIDTH, self.HEIGHT, 'OpenGL', None, None)
        # paramétrage de la fonction de gestion des évènements
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.set_mouse_button_callback(self.window, self.click_callback)

        #souris
        # glfw.set_cursor_pos_callback(self.window, self.mouse_callback)
        # glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

        # activation du context OpenGL pour la fenêtre
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        # activation de la gestion de la profondeur
        GL.glEnable(GL.GL_DEPTH_TEST)
        # choix de la couleur de fond
        GL.glClearColor(0.5, 0.6, 0.9, 1.0)
        print(f"OpenGL: {GL.glGetString(GL.GL_VERSION).decode('ascii')}")

        self.objs = []
        self.objs_menu = []
        self.objs_end_game_menu = []
        self.touch = {}
        

        if (glfw.raw_mouse_motion_supported()):
            glfw.set_input_mode(self.window, glfw.RAW_MOUSE_MOTION, glfw.TRUE);
    
    def run_menu(self):
        #self.scene = 1
        # nettoyage de la fenêtre : fond et profondeur
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        for obj in self.objs_menu:
            GL.glUseProgram(obj.program)
            obj.draw()
        
        glfw.swap_buffers(self.window)
        glfw.poll_events() 
        
    def run_game(self):

        
        self.temps_depart = time.time()
        self.temps_origine = time.time()
        
        # boucle d'affichage
        while self.scene == 1:
            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            self.update_key()
            
            print(self.scene)
            self.update_zombie()
            self.update_bullet()
            self.update_player()
            self.update_life()
            self.update_score()
            self.update_timer()


            for obj in self.objs:
                GL.glUseProgram(obj.program)
                if type(obj) == Object3D:
                    self.update_camera(obj.program)
                obj.draw()

                

            if self.player.player_death() == False:
                self.scene = 2
                

            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
            # gestion des évènements
            glfw.poll_events()
    
    def run_end_game(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        for obj in self.objs_end_game_menu:
            GL.glUseProgram(obj.program)
            obj.draw()
        
        glfw.swap_buffers(self.window)
        glfw.poll_events() 


    def run(self):

        while not glfw.window_should_close(self.window):
            
            while not glfw.window_should_close(self.window) and self.scene == 0:
                self.run_menu()
            
            glfw.set_cursor_pos_callback(self.window, self.mouse_callback_game)
            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

            while not glfw.window_should_close(self.window) and self.scene == 1:
                self.run_game()

            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_NORMAL)

            while not glfw.window_should_close(self.window) and self.scene == 2:
                self.run_end_game()


        
    def key_callback(self, win, key, scancode, action, mods):
        # sortie du programme si appui sur la touche 'échappement'
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            self.scene = 0
        self.touch[key] = action

    def click_callback(self, win, key, action, mods):
        self.touch[key] = action
        if key == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            self.fire_bullet()
        if self.scene == 0:
            x , y = glfw.get_cursor_pos(self.window)
            x = (x-self.WIDTH/2)/self.WIDTH*2
            y = (-y+self.HEIGHT/2)/self.HEIGHT*2
            b_play = self.objs_menu[0]
            b_quit = self.objs_menu[1]
            if b_play.bottomLeft[0]<x<b_play.topRight[0] and b_play.bottomLeft[1]<y<b_play.topRight[1]:
                self.scene = 1
            if b_quit.bottomLeft[0]<x<b_quit.topRight[0] and b_quit.bottomLeft[1]<y<b_quit.topRight[1]:
                glfw.set_window_should_close(self.window, glfw.TRUE)
        if self.scene == 2:
            x , y = glfw.get_cursor_pos(self.window)
            x = (x-self.WIDTH/2)/self.WIDTH*2
            y = (-y+self.HEIGHT/2)/self.HEIGHT*2
            b_play = self.objs_end_game_menu[1]
            b_quit = self.objs_end_game_menu[2]
            if b_play.bottomLeft[0]<x<b_play.topRight[0] and b_play.bottomLeft[1]<y<b_play.topRight[1]:
                self.scene = 1
            if b_quit.bottomLeft[0]<x<b_quit.topRight[0] and b_quit.bottomLeft[1]<y<b_quit.topRight[1]:
                glfw.set_window_should_close(self.window, glfw.TRUE)
    
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
                self.score_chiffre += 10
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
        self.player.update(self.zombies)


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


        
            
            


        # if glfw.KEY_SPACE in self.touch and self.touch[glfw.KEY_SPACE] > 0:

    def mouse_callback_game(self, window, xpos, ypos):

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

    
    def player_life(self):
        self.vie_joueur = self.player.vie(self.zombies)
        # print(self.vie_joueur)
        return str(self.vie_joueur)

    def update_life(self):
        self.vie.value = 'VIE : ' + self.player_life() + '/ 50'
    
    def update_score(self):
        self.score.value = 'SCORE : ' + str(self.score_chiffre)
        self.score_end.value = 'SCORE : ' + str(self.score_chiffre)


    def update_timer(self):
        temps = self.temps_partie + self.temps_depart - time.time()
        self.texte_timer.value = str(temps)[:4]
        self.texte_timer.bottomLeft = np.array([-0.17, 0.80], np.float32)
        self.texte_timer.topRight = np.array([0.17, 0.95], np.float32)
        self.texte_timer.texture = glutils.load_texture('fontB.jpg')

        if temps < 0:
            self.scene = 2
