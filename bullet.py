import glutils
from mesh import Mesh
from cpe3d import Object3D, Transformation3D
import numpy as np
import pyrr
import random

class Bullet():
    def __init__(self, transform, program3d_id):
        self.model = Mesh.load_obj('model/bullet.obj')
        self.model.normalize()
        self.model.apply_matrix(pyrr.matrix44.create_from_scale([1, 1, 1, 1]))
        self.texture = glutils.load_texture('texture/bullet.png')
        self.transform = transform
        self.program3d_id = program3d_id
        self.object = Object3D(self.model.load_to_gpu(), self.model.get_nb_triangles(), self.program3d_id, self.texture, self.transform, "zombie")
        self.vel = 0.2
        self.show = True

    def update(self):
        self.move()

    def move(self):
        self.transform.translation += \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.transform.rotation_euler), pyrr.Vector3([0, 0, self.vel]))

class Bullets():
    def __init__(self, program3d_id):
        self.all_bullets = []
        self.program3d_id = program3d_id
    
    def add_bullet(self, player_pos):
        tr = Transformation3D()
        tr.rotation_euler[pyrr.euler.index().yaw] = player_pos.rotation_euler[pyrr.euler.index().yaw]
        bullet = Bullet(tr,self.program3d_id)
        self.all_bullets.append(bullet)
        return bullet

    def update(self):
        for bullet in self.all_bullets:
            bullet.update()