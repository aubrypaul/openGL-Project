import glutils
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D, Text
import numpy as np
import OpenGL.GL as GL
import pyrr
import random

class Zombie():
    def __init__(self, transform, program3d_id):
        self.model = Mesh.load_obj('model/zombie.obj')
        self.model.normalize()
        self.model.apply_matrix(pyrr.matrix44.create_from_scale([1, 1, 1, 1]))
        self.texture = glutils.load_texture('texture/zombie.png')
        self.transform = transform
        self.program3d_id = program3d_id
        self.transform.translation.y = -np.amin(self.model.vertices, axis=0)[1]
        self.object = Object3D(self.model.load_to_gpu(), self.model.get_nb_triangles(), self.program3d_id, self.texture, self.transform, "zombie")

    def move(self):
        self.transform.translation += \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.transform.rotation_euler), pyrr.Vector3([0, 0, 0.02]))

class Zombies():
    def __init__(self, program3d_id, n):
        self.all_zombies = []
        for i in range(n):
            tr = Transformation3D()
            theta = random.random()*2*np.pi
            tr.translation.x = 25*np.cos(theta)
            tr.translation.z = 25*np.sin(theta)
            tr.rotation_euler[pyrr.euler.index().yaw] += theta + np.pi/2
            self.all_zombies.append(Zombie(tr,program3d_id))

    def update(self):
        self.move()

    def move(self):
        for zombie in self.all_zombies:
            zombie.move()
    
