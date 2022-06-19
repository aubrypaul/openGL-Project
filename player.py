import glutils
from mesh import Mesh
from cpe3d import Object3D, Transformation3D
import numpy as np
import pyrr

class Player():
    def __init__(self, program3d_id):
            self.program = program3d_id
            self.model = Mesh.load_obj('model/stegosaurus.obj')
            self.model.normalize()
            self.model.apply_matrix(pyrr.matrix44.create_from_scale([2, 2, 2, 1]))
            self.transformation = Transformation3D()
            self.transformation.translation.y = -np.amin(self.model.vertices, axis=0)[1]
            self.transformation.translation.z = 0
            self.transformation.rotation_center.z = 0.2
            self.texture = glutils.load_texture('texture/stegosaurus.jpg')
            self.object = Object3D(self.model.load_to_gpu(), self.model.get_nb_triangles(), program3d_id, self.texture, self.transformation)
            self.alive = True
            self.life = 50

    def update(self, zombies):
        self.check_collision()
        self.vie(zombies)
        self.player_death()
        # print(self.life, self.alive)
    
    def check_collision(self):
        if self.transformation.translation.x > 50 - 1:
            self.transformation.translation.x = 50 - 1
        if self.transformation.translation.x < -50 + 1:
            self.transformation.translation.x = -50 + 1
        if self.transformation.translation.z > 50 - 1:
            self.transformation.translation.z = 50 - 1
        if self.transformation.translation.z < -50 + 1:
            self.transformation.translation.z = -50 + 1

    def vie(self, zombies):
        for zombie in zombies.all_zombies:
            tr = zombie.transform
            if tr.translation.x > self.transformation.translation.x - 0.5 and tr.translation.x < self.transformation.translation.x + 0.5 and tr.translation.z > self.transformation.translation.z - 0.5 and tr.translation.z < self.transformation.translation.z + 0.5:
                self.life -= 1
        return self.life
    
    def player_death(self):
        if self.life <= 0:
            self.alive = False
        return self.alive