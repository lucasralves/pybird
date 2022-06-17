from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GL import shaders
import numpy as np

from pybird.mesh.main import Mesh
from pybird.view.utilities.opengl_ui import Geometry, OpenGL_UI


class View:

    def __init__(self, mesh: Mesh) -> None:
        self.__mesh = mesh
    
    def mesh(self) -> None:
        opengl = OpenGL_UI(
            geos=[
                Geometry(
                    vertices=self.__mesh.vertices,
                    edges=self.__mesh.edges,
                    faces=self.__mesh.faces,
                )
            ],
        )
        opengl.ui()