import glutils
from mesh import Mesh
from cpe3d import Object3D, Transformation3D
import numpy as np
import pyrr
import random

class Bullet():
    def __init__(self, transform, program3d_id, vao, nb_triangles, texture):
        self.transform = transform
        self.program3d_id = program3d_id
        self.vao = vao
        self.nb_triangles = nb_triangles
        self.texture = texture
        self.object = Object3D(self.vao, self.nb_triangles, self.program3d_id, self.texture, self.transform)
        self.vel = 1
        self.show = True

    def update(self, zombies):
        self.move()
        self.check_collision(zombies)

    def move(self):
        self.transform.translation += \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.transform.rotation_euler), pyrr.Vector3([self.vel,0, 0]))

    def check_collision(self, zombies):
        for zombie in zombies.all_zombies:
            tr = zombie.transform
           
            
            

class Bullets():
    def __init__(self, program3d_id, player_tr):
        self.model = Mesh.load_obj('model/bullet.obj')
        self.model.normalize()
        self.model.apply_matrix(pyrr.matrix44.create_from_scale([0.2, 0.2, 0.2, 1]))
        self.texture = glutils.load_texture('texture/bullet.jpg')
        self.vao = self.model.load_to_gpu()
        self.nb_triangles = self.model.get_nb_triangles()
        self.all_bullets = []
        self.program3d_id = program3d_id
        self.player_tr = player_tr
    
    def add_bullet(self):
        tr = Transformation3D()
        tr.rotation_euler[pyrr.euler.index().yaw] = self.player_tr.rotation_euler[pyrr.euler.index().yaw] + np.pi/2
        tr.translation.y = 1.5
        tr.translation.x = self.player_tr.translation.x
        tr.translation.z = self.player_tr.translation.z
        bullet = Bullet(tr,self.program3d_id,self.vao, self.nb_triangles,self.texture)
        self.all_bullets.append(bullet)
        return bullet

    def update(self, zombies):
        for bullet in self.all_bullets:
            bullet.update(zombies)