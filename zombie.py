import glutils
from mesh import Mesh
from cpe3d import Object3D, Transformation3D
import numpy as np
import pyrr
import random

class Zombie():
    def __init__(self, transform, program3d_id, vao, nb_triangles, texture, player_tr):
        self.transform = transform
        self.program3d_id = program3d_id
        self.vao = vao
        self.nb_triangles = nb_triangles
        self.texture = texture
        self.object = Object3D(self.vao, self.nb_triangles, self.program3d_id, self.texture, self.transform)
        self.vel =  0#.1 + random.random()*0.05
        self.alive = True
        self.player_tr = player_tr

    def move(self):
        self.transform.translation += \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.transform.rotation_euler), pyrr.Vector3([0, 0, self.vel]))
    
    def in_limit(self):
        if abs(self.transform.translation.x) > 50 or abs(self.transform.translation.z) > 50:
            self.alive = False


class Zombies():
    def __init__(self, program3d_id, n, player_tr):
        self.model = Mesh.load_obj('model/zombie.obj')
        self.model.normalize()
        self.model.apply_matrix(pyrr.matrix44.create_from_scale([1, 1, 1, 1]))
        self.texture = glutils.load_texture('texture/zombie.png')
        self.vao = self.model.load_to_gpu()
        self.nb_triangles = self.model.get_nb_triangles()
        self.all_zombies = []
        self.program3d_id = program3d_id
        self.player_tr = player_tr
        for i in range(n):
            self.add_zombie()


    def update(self):
        self.move()
        self.in_limit()

    def move(self):
        for zombie in self.all_zombies:
            zombie.move()
    
    def in_limit(self):
        for zombie in self.all_zombies:
            zombie.in_limit()
    
    def kill_zombie(self,zombie):
        for i in range(len(self.all_zombies)):
            if self.all_zombies[i] == zombie:
                del self.all_zombies[i]
                break

    def add_zombie(self):
            tr = Transformation3D()
            theta = random.random()*2*np.pi
            tr.translation.x = 20*np.cos(theta) + self.player_tr.translation.x
            tr.translation.z = 20*np.sin(theta) + self.player_tr.translation.z
            tr.rotation_euler[pyrr.euler.index().yaw] += theta + np.pi/2
            tr.translation.y = -np.amin(self.model.vertices, axis=0)[1]
            zombie = Zombie(tr,self.program3d_id,self.vao,self.nb_triangles,self.texture, self.player_tr)
            self.all_zombies.append(zombie)
            return zombie
    
