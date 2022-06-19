from bullet import Bullets
from viewerGL import ViewerGL
import glutils
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D, Text
import numpy as np
import OpenGL.GL as GL
from zombie import Zombies
from player import Player

def main():
    viewer = ViewerGL()
    

    viewer.set_camera(Camera())
    viewer.cam.transformation.translation.y = 2
    viewer.cam.transformation.rotation_center = viewer.cam.transformation.translation.copy()

    program3d_id = glutils.create_program_from_file('shader.vert', 'shader.frag')
    programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag')


    viewer.init_player(Player(program3d_id))
    viewer.init_bullets(Bullets(program3d_id, viewer.player.transformation))
    viewer.set_zombie(Zombies(program3d_id, 8, viewer.player.transformation))

    m = Mesh()
    p0, p1, p2, p3 = [-50, 0, -50], [50, 0, -50], [50, 0, 50], [-50, 0, 50 ]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('texture/grass.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.add_object(o)


    # 4 MURS :
    m = Mesh()
    p0, p1, p2, p3 = [-50, 0, -50], [-50, 0, 50], [-50, 10, 50], [-50, 10, -50]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('texture/wall.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.add_object(o)

    m = Mesh()
    p0, p1, p2, p3 = [-50, 0, -50], [50, 0, -50], [50, 10, -50], [-50, 10, -50]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('texture/wall.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.add_object(o)

    m = Mesh()
    p0, p1, p2, p3 = [50, 0, -50], [50, 0, 50], [50, 10, 50], [50, 10, -50]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('texture/wall.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.add_object(o)

    m = Mesh()
    p0, p1, p2, p3 = [50, 0, 50], [-50, 0, 50], [-50, 10, 50], [50, 10, 50]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('texture/wall.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.add_object(o)
    # FIN 4 MURS


    #Cross air
    vao = Text.initalize_geometry()
    texture = glutils.load_texture('fontB.jpg')
    o = Text('.', np.array([-0.05, -0.05], np.float32), np.array([0.05, 0.05], np.float32), vao, 0, programGUI_id, texture)
    viewer.add_object(o)

    # Barre de vie
    o = Text('Vie', np.array([-1, 0.9], np.float32), np.array([-0.4, 1], np.float32), vao, 0, programGUI_id, texture)
    viewer.add_object(o)
    viewer.vie = o

    # Score
    o = Text('Vie', np.array([0.4, 0.9], np.float32), np.array([1, 1], np.float32), vao, 0, programGUI_id, texture)
    viewer.add_object(o)
    viewer.score = o

    # Bouton démarrer
    o = Text('Commencer', np.array([-0.7, 0.25], np.float32), np.array([0.7, 0.55], np.float32), vao, 2, programGUI_id, texture)
    viewer.objs_menu.append(o)

    # Bouton quitter
    o = Text('Quitter', np.array([-0.7, -0.5], np.float32), np.array([0.7, 0.05], np.float32), vao, 2, programGUI_id, texture)
    viewer.objs_menu.append(o)

    viewer.run()
    

if __name__ == '__main__':
    main()