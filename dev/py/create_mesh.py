import sys
from typing import List
import numpy as np
import gmsh

def create_mesh(foilname: str,
                span: float = 5,
                n_span: int = 20,
                n_chord_1: int = 20,
                n_chord_2: int = 5,
                n_chord_3: int = 12,
                coef_le: float = 3.0,
                coef_te: float = 1.1):
    
    """
        Define geometry and mesh parameters
    """
    # Airfoil
    foil = np.loadtxt(foilname)

    # Mesh regions
    n_1 = int(foil.shape[0] / 5)
    n_2 = int(n_1 * 1.5)
    n_3 = foil.shape[0] - n_2 - 1
    n_4 = foil.shape[0] - n_1 - 1
    
    # Foil points
    point_1 = foil[0, :]
    point_2 = foil[n_1, :]
    point_3 = foil[n_2, :]
    point_4 = foil[n_3, :]
    point_5 = foil[n_4, :]

    # Foil curves
    curve_1 = foil[1:n_1, :]
    curve_2 = foil[n_1 + 1:n_2, :]
    curve_3 = foil[n_2 + 1:n_3, :]
    curve_4 = foil[n_3 + 1:n_4, :]
    curve_5 = foil[n_4 + 1:-1, :]

    """
        Create mesh
    """
    gmsh.initialize()
    gmsh.option.setNumber('General.Verbosity', 1)

    # Points
    p1_e = gmsh.model.geo.add_point(point_1[0], point_1[1], - span / 2)
    p2_e = gmsh.model.geo.add_point(point_2[0], point_2[1], - span / 2)
    p3_e = gmsh.model.geo.add_point(point_3[0], point_3[1], - span / 2)
    p4_e = gmsh.model.geo.add_point(point_4[0], point_4[1], - span / 2)
    p5_e = gmsh.model.geo.add_point(point_5[0], point_5[1], - span / 2)

    p1_d = gmsh.model.geo.add_point(point_1[0], point_1[1], span / 2)
    p2_d = gmsh.model.geo.add_point(point_2[0], point_2[1], span / 2)
    p3_d = gmsh.model.geo.add_point(point_3[0], point_3[1], span / 2)
    p4_d = gmsh.model.geo.add_point(point_4[0], point_4[1], span / 2)
    p5_d = gmsh.model.geo.add_point(point_5[0], point_5[1], span / 2)

    # Lines
    l1 = gmsh.model.geo.add_line(p1_e, p1_d)
    l2 = gmsh.model.geo.add_line(p2_e, p2_d)
    l3 = gmsh.model.geo.add_line(p3_e, p3_d)
    l4 = gmsh.model.geo.add_line(p4_e, p4_d)
    l5 = gmsh.model.geo.add_line(p5_e, p5_d)

    # Curves
    c1_e = gmsh.model.geo.add_polyline([p1_e] + [gmsh.model.geo.add_point(p[0], p[1], - span / 2) for p in curve_1] + [p2_e])
    c2_e = gmsh.model.geo.add_polyline([p2_e] + [gmsh.model.geo.add_point(p[0], p[1], - span / 2) for p in curve_2] + [p3_e])
    c3_e = gmsh.model.geo.add_polyline([p3_e] + [gmsh.model.geo.add_point(p[0], p[1], - span / 2) for p in curve_3] + [p4_e])
    c4_e = gmsh.model.geo.add_polyline([p4_e] + [gmsh.model.geo.add_point(p[0], p[1], - span / 2) for p in curve_4] + [p5_e])
    c5_e = gmsh.model.geo.add_polyline([p5_e] + [gmsh.model.geo.add_point(p[0], p[1], - span / 2) for p in curve_5] + [p1_e])

    c1_d = gmsh.model.geo.add_polyline([p1_d] + [gmsh.model.geo.add_point(p[0], p[1], span / 2) for p in curve_1] + [p2_d])
    c2_d = gmsh.model.geo.add_polyline([p2_d] + [gmsh.model.geo.add_point(p[0], p[1], span / 2) for p in curve_2] + [p3_d])
    c3_d = gmsh.model.geo.add_polyline([p3_d] + [gmsh.model.geo.add_point(p[0], p[1], span / 2) for p in curve_3] + [p4_d])
    c4_d = gmsh.model.geo.add_polyline([p4_d] + [gmsh.model.geo.add_point(p[0], p[1], span / 2) for p in curve_4] + [p5_d])
    c5_d = gmsh.model.geo.add_polyline([p5_d] + [gmsh.model.geo.add_point(p[0], p[1], span / 2) for p in curve_5] + [p1_d])

    # Curve loops
    cl1 = gmsh.model.geo.addCurveLoop([-l1, c1_e, l2, -c1_d])
    cl2 = gmsh.model.geo.addCurveLoop([-l2, c2_e, l3, -c2_d])
    cl3 = gmsh.model.geo.addCurveLoop([-l3, c3_e, l4, -c3_d])
    cl4 = gmsh.model.geo.addCurveLoop([-l4, c4_e, l5, -c4_d])
    cl5 = gmsh.model.geo.addCurveLoop([-l5, c5_e, l1, -c5_d])

    # Surfaces
    s1 = gmsh.model.geo.add_surface_filling([cl1])
    s2 = gmsh.model.geo.add_surface_filling([cl2])
    s3 = gmsh.model.geo.add_surface_filling([cl3])
    s4 = gmsh.model.geo.add_surface_filling([cl4])
    s5 = gmsh.model.geo.add_surface_filling([cl5])

    gmsh.model.geo.synchronize()

    # Transfinite curves
    gmsh.model.mesh.set_transfinite_curve(l1, n_span)
    gmsh.model.mesh.set_transfinite_curve(l2, n_span)
    gmsh.model.mesh.set_transfinite_curve(l3, n_span)
    gmsh.model.mesh.set_transfinite_curve(l4, n_span)
    gmsh.model.mesh.set_transfinite_curve(l5, n_span)

    gmsh.model.mesh.set_transfinite_curve(c1_e, n_chord_3, 'Progression', coef_te)
    gmsh.model.mesh.set_transfinite_curve(c5_e, n_chord_3, 'Progression', - coef_te)

    gmsh.model.mesh.set_transfinite_curve(c2_e, n_chord_2)
    gmsh.model.mesh.set_transfinite_curve(c4_e, n_chord_2)

    gmsh.model.mesh.set_transfinite_curve(c3_e, n_chord_1, 'Bump', - coef_le)

    gmsh.model.mesh.set_transfinite_curve(c1_d, n_chord_3, 'Progression', coef_te)
    gmsh.model.mesh.set_transfinite_curve(c5_d, n_chord_3, 'Progression', - coef_te)

    gmsh.model.mesh.set_transfinite_curve(c2_d, n_chord_2)
    gmsh.model.mesh.set_transfinite_curve(c4_d, n_chord_2)

    gmsh.model.mesh.set_transfinite_curve(c3_d, n_chord_1, 'Bump', - coef_le)

    # Transfinite surfaces
    gmsh.model.mesh.set_transfinite_surface(s1)
    gmsh.model.mesh.set_transfinite_surface(s2)
    gmsh.model.mesh.set_transfinite_surface(s3)
    gmsh.model.mesh.set_transfinite_surface(s4)
    gmsh.model.mesh.set_transfinite_surface(s5)

    # Create quads
    gmsh.model.mesh.set_recombine(2, s1)
    # gmsh.model.mesh.set_recombine(2, s2)
    gmsh.model.mesh.set_recombine(2, s3)
    gmsh.model.mesh.set_recombine(2, s4)
    gmsh.model.mesh.set_recombine(2, s5)

    gmsh.model.mesh.generate(2)

    # if "-nopopup" not in sys.argv:
    #     gmsh.fltk.initialize()
    #     while gmsh.fltk.isAvailable():
    #         gmsh.fltk.wait()
    
    """
        Get mesh data
    """
    # Vertices
    data = gmsh.model.mesh.get_nodes()
    vertices = data[1].reshape((data[0].size, 3))

    # Faces
    gmsh.model.mesh.create_faces()
    data = gmsh.model.mesh.get_all_faces(4)
    faces4 = data[1].reshape((data[0].size, 4)).astype(np.int32) - 1
    data = gmsh.model.mesh.get_all_faces(3)
    faces3 = data[1].reshape((data[0].size, 3)).astype(np.int32) - 1

    # Trailing edge
    trailing_edge_group = gmsh.model.add_physical_group(1, [l1])
    trailing_edge = gmsh.model.mesh.get_nodes_for_physical_group(1, trailing_edge_group)[0] - 1

    gmsh.finalize()

    return [vertices, faces3, faces4, [trailing_edge]]
