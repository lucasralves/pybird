import sys
import gmsh
from numpy import asarray

from pybird.geometry.main import Geometry
from pybird.helpers import vector

def build_mesh(geo: Geometry, size: float, refinement_ratio: float = 0.5) -> None:
    
    gmsh.initialize(sys.argv)
    gmsh.model.add("model")

    gmsh.option.setNumber("Mesh.Algorithm", 5)

    # Mesh size
    lc = size

    #################################################################
    # Wing
    #################################################################
    # Define points
    p1e = gmsh.model.geo.addPoint(geo.wing_params.p1e[0], geo.wing_params.p1e[1], geo.wing_params.p1e[2], lc)
    p3e = gmsh.model.geo.addPoint(geo.wing_params.p3e[0], geo.wing_params.p3e[1], geo.wing_params.p3e[2], lc)
    p4e = gmsh.model.geo.addPoint(geo.wing_params.p4e[0], geo.wing_params.p4e[1], geo.wing_params.p4e[2], lc)
    p5e = gmsh.model.geo.addPoint(geo.wing_params.p5e[0], geo.wing_params.p5e[1], geo.wing_params.p5e[2], lc)
    p6e = gmsh.model.geo.addPoint(geo.wing_params.p6e[0], geo.wing_params.p6e[1], geo.wing_params.p6e[2], lc)
    p7e = gmsh.model.geo.addPoint(geo.wing_params.p7e[0], geo.wing_params.p7e[1], geo.wing_params.p7e[2], lc)
    p8e = gmsh.model.geo.addPoint(geo.wing_params.p8e[0], geo.wing_params.p8e[1], geo.wing_params.p8e[2], lc)
    v1e = gmsh.model.geo.addPoint(geo.wing_params.v1e[0], geo.wing_params.v1e[1], geo.wing_params.v1e[2], lc)
    v2e = gmsh.model.geo.addPoint(geo.wing_params.v2e[0], geo.wing_params.v2e[1], geo.wing_params.v2e[2], lc)
    v3e = gmsh.model.geo.addPoint(geo.wing_params.v3e[0], geo.wing_params.v3e[1], geo.wing_params.v3e[2], lc)
    v4e = gmsh.model.geo.addPoint(geo.wing_params.v4e[0], geo.wing_params.v4e[1], geo.wing_params.v4e[2], lc)

    p1d = gmsh.model.geo.addPoint(geo.wing_params.p1d[0], geo.wing_params.p1d[1], geo.wing_params.p1d[2], lc)
    p3d = gmsh.model.geo.addPoint(geo.wing_params.p3d[0], geo.wing_params.p3d[1], geo.wing_params.p3d[2], lc)
    p4d = gmsh.model.geo.addPoint(geo.wing_params.p4d[0], geo.wing_params.p4d[1], geo.wing_params.p4d[2], lc)
    p5d = gmsh.model.geo.addPoint(geo.wing_params.p5d[0], geo.wing_params.p5d[1], geo.wing_params.p5d[2], lc)
    p6d = gmsh.model.geo.addPoint(geo.wing_params.p6d[0], geo.wing_params.p6d[1], geo.wing_params.p6d[2], lc)
    p7d = gmsh.model.geo.addPoint(geo.wing_params.p7d[0], geo.wing_params.p7d[1], geo.wing_params.p7d[2], lc)
    p8d = gmsh.model.geo.addPoint(geo.wing_params.p8d[0], geo.wing_params.p8d[1], geo.wing_params.p8d[2], lc)
    v1d = gmsh.model.geo.addPoint(geo.wing_params.v1d[0], geo.wing_params.v1d[1], geo.wing_params.v1d[2], lc)
    v2d = gmsh.model.geo.addPoint(geo.wing_params.v2d[0], geo.wing_params.v2d[1], geo.wing_params.v2d[2], lc)
    v3d = gmsh.model.geo.addPoint(geo.wing_params.v3d[0], geo.wing_params.v3d[1], geo.wing_params.v3d[2], lc)
    v4d = gmsh.model.geo.addPoint(geo.wing_params.v4d[0], geo.wing_params.v4d[1], geo.wing_params.v4d[2], lc)

    points1e = []
    size = len(geo.wing_params.curve1e)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.wing_params.curve1e[i, 0], geo.wing_params.curve1e[i, 1], geo.wing_params.curve1e[i, 2], lc * refinement_ratio)
            points1e.append(index)
    
    points2e = []
    size = len(geo.wing_params.curve2e)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.wing_params.curve2e[i, 0], geo.wing_params.curve2e[i, 1], geo.wing_params.curve2e[i, 2], lc)
            points2e.append(index)
        
    points3e = []
    size = len(geo.wing_params.curve3e)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.wing_params.curve3e[i, 0], geo.wing_params.curve3e[i, 1], geo.wing_params.curve3e[i, 2], lc)
            points3e.append(index)
    
    points4e = []
    size = len(geo.wing_params.curve4e)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.wing_params.curve4e[i, 0], geo.wing_params.curve4e[i, 1], geo.wing_params.curve4e[i, 2], lc)
            points4e.append(index)
    
    points5e = []
    size = len(geo.wing_params.curve5e)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.wing_params.curve5e[i, 0], geo.wing_params.curve5e[i, 1], geo.wing_params.curve5e[i, 2], lc)
            points5e.append(index)
    
    points6e = []
    size = len(geo.wing_params.curve6e)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.wing_params.curve6e[i, 0], geo.wing_params.curve6e[i, 1], geo.wing_params.curve6e[i, 2], lc)
            points6e.append(index)

    points7e = []
    size = len(geo.wing_params.curve7e)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.wing_params.curve7e[i, 0], geo.wing_params.curve7e[i, 1], geo.wing_params.curve7e[i, 2], lc)
            points7e.append(index)
    
    points8e = []
    size = len(geo.wing_params.curve8e)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.wing_params.curve8e[i, 0], geo.wing_params.curve8e[i, 1], geo.wing_params.curve8e[i, 2], lc)
            points8e.append(index)
    
    points9e = []
    size = len(geo.wing_params.curve9e)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.wing_params.curve9e[i, 0], geo.wing_params.curve9e[i, 1], geo.wing_params.curve9e[i, 2], lc)
            points9e.append(index)
    
    points10e = []
    size = len(geo.wing_params.curve10e)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.wing_params.curve10e[i, 0], geo.wing_params.curve10e[i, 1], geo.wing_params.curve10e[i, 2], lc)
            points10e.append(index)
    
    points11e = []
    size = len(geo.wing_params.curve11e)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.wing_params.curve11e[i, 0], geo.wing_params.curve11e[i, 1], geo.wing_params.curve11e[i, 2], lc)
            points11e.append(index)
    
    points12e = []
    size = len(geo.wing_params.curve12e)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.wing_params.curve12e[i, 0], geo.wing_params.curve12e[i, 1], geo.wing_params.curve12e[i, 2], lc)
            points12e.append(index)
    
    points13e = []
    size = len(geo.wing_params.curve13e)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.wing_params.curve13e[i, 0], geo.wing_params.curve13e[i, 1], geo.wing_params.curve13e[i, 2], lc)
            points13e.append(index)
    
    points14e = []
    size = len(geo.wing_params.curve14e)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.wing_params.curve14e[i, 0], geo.wing_params.curve14e[i, 1], geo.wing_params.curve14e[i, 2], lc)
            points14e.append(index)
    
    points1d = []
    size = len(geo.wing_params.curve1d)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.wing_params.curve1d[i, 0], geo.wing_params.curve1d[i, 1], geo.wing_params.curve1d[i, 2], lc)
            points1d.append(index)
    
    points2d = []
    size = len(geo.wing_params.curve2d)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.wing_params.curve2d[i, 0], geo.wing_params.curve2d[i, 1], geo.wing_params.curve2d[i, 2], lc)
            points2d.append(index)
        
    points3d = []
    size = len(geo.wing_params.curve3d)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.wing_params.curve3d[i, 0], geo.wing_params.curve3d[i, 1], geo.wing_params.curve3d[i, 2], lc)
            points3d.append(index)
    
    points4d = []
    size = len(geo.wing_params.curve4d)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.wing_params.curve4d[i, 0], geo.wing_params.curve4d[i, 1], geo.wing_params.curve4d[i, 2], lc)
            points4d.append(index)
    
    points5d = []
    size = len(geo.wing_params.curve5d)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.wing_params.curve5d[i, 0], geo.wing_params.curve5d[i, 1], geo.wing_params.curve5d[i, 2], lc)
            points5d.append(index)
    
    points6d = []
    size = len(geo.wing_params.curve6d)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.wing_params.curve6d[i, 0], geo.wing_params.curve6d[i, 1], geo.wing_params.curve6d[i, 2], lc)
            points6d.append(index)

    points7d = []
    size = len(geo.wing_params.curve7d)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.wing_params.curve7d[i, 0], geo.wing_params.curve7d[i, 1], geo.wing_params.curve7d[i, 2], lc)
            points7d.append(index)
    
    points8d = []
    size = len(geo.wing_params.curve8d)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.wing_params.curve8d[i, 0], geo.wing_params.curve8d[i, 1], geo.wing_params.curve8d[i, 2], lc)
            points8d.append(index)
    
    points9d = []
    size = len(geo.wing_params.curve9d)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.wing_params.curve9d[i, 0], geo.wing_params.curve9d[i, 1], geo.wing_params.curve9d[i, 2], lc)
            points9d.append(index)
    
    points10d = []
    size = len(geo.wing_params.curve10d)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.wing_params.curve10d[i, 0], geo.wing_params.curve10d[i, 1], geo.wing_params.curve10d[i, 2], lc)
            points10d.append(index)
    
    points11d = []
    size = len(geo.wing_params.curve11d)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.wing_params.curve11d[i, 0], geo.wing_params.curve11d[i, 1], geo.wing_params.curve11d[i, 2], lc)
            points11d.append(index)
    
    points12d = []
    size = len(geo.wing_params.curve12d)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.wing_params.curve12d[i, 0], geo.wing_params.curve12d[i, 1], geo.wing_params.curve12d[i, 2], lc)
            points12d.append(index)
    
    points13d = []
    size = len(geo.wing_params.curve13d)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.wing_params.curve13d[i, 0], geo.wing_params.curve13d[i, 1], geo.wing_params.curve13d[i, 2], lc)
            points13d.append(index)
    
    points14d = []
    size = len(geo.wing_params.curve14d)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.wing_params.curve14d[i, 0], geo.wing_params.curve14d[i, 1], geo.wing_params.curve14d[i, 2], lc)
            points14d.append(index)
    
    # Define curves
    curve1e = gmsh.model.geo.addPolyline([p1e] + points1e + [p3e])
    curve2e = gmsh.model.geo.addPolyline([p3e] + points2e + [p4e])
    curve3e = gmsh.model.geo.addPolyline([p4e] + points3e + [p5e] + asarray(points4e)[:geo.wing_params.v1eIndex].tolist() + [v1e])
    curve4e = gmsh.model.geo.addPolyline([v1e] + asarray(points4e)[geo.wing_params.v1eIndex:].tolist() + [p6e])
    curve5e = gmsh.model.geo.addPolyline([p6e] + asarray(points5e)[:geo.wing_params.v2eIndex - 1].tolist() + [v2e])
    curve6e = gmsh.model.geo.addPolyline([v2e] + asarray(points5e)[geo.wing_params.v2eIndex:geo.wing_params.v3eIndex - 1].tolist() + [v3e])
    curve7e = gmsh.model.geo.addBezier([v3e, p7e, v4e]) # gmsh.model.geo.addPolyline([v3e] + asarray(points5e)[geo.wing_params.v3eIndex:].tolist() + [p7e] + asarray(points6e)[:geo.wing_params.v4eIndex - 1].tolist() + [v4e])
    curve8e = gmsh.model.geo.addPolyline([v4e] + asarray(points6e)[geo.wing_params.v4eIndex:].tolist() + [p8e])
    curve9e = gmsh.model.geo.addPolyline([p1e] + points7e + [p8e])
    curve10e = gmsh.model.geo.addPolyline([p1e] + points8e + [p8e])
    curve11e = gmsh.model.geo.addPolyline([p3e] + points9e + [v4e])
    curve12e = gmsh.model.geo.addPolyline([p3e] + points10e + [v4e])
    curve13e = gmsh.model.geo.addPolyline([p4e] + points11e + [v3e])
    curve14e = gmsh.model.geo.addPolyline([p4e] + points12e + [v3e])
    curve15e = gmsh.model.geo.addPolyline([v1e] + points13e + [v2e])
    curve16e = gmsh.model.geo.addPolyline([v1e] + points14e + [v2e])

    curve1d = gmsh.model.geo.addPolyline([p1d] + points1d + [p3d])
    curve2d = gmsh.model.geo.addPolyline([p3d] + points2d + [p4d])
    curve3d = gmsh.model.geo.addPolyline([p4d] + points3d + [p5d] + asarray(points4d)[:geo.wing_params.v1dIndex].tolist() + [v1d])
    curve4d = gmsh.model.geo.addPolyline([v1d] + asarray(points4d)[geo.wing_params.v1dIndex:].tolist() + [p6d])
    curve5d = gmsh.model.geo.addPolyline([p6d] + asarray(points5d)[:geo.wing_params.v2dIndex - 1].tolist() + [v2d])
    curve6d = gmsh.model.geo.addPolyline([v2d] + asarray(points5d)[geo.wing_params.v2dIndex:geo.wing_params.v3eIndex - 1].tolist() + [v3d])
    curve7d = gmsh.model.geo.addBezier([v3d, p7d, v4d]) # gmsh.model.geo.addPolyline([v3d] + asarray(points5d)[geo.wing_params.v3dIndex:].tolist() + [p7d] + asarray(points6d)[:geo.wing_params.v4dIndex - 1].tolist() + [v4d])
    curve8d = gmsh.model.geo.addPolyline([v4d] + asarray(points6d)[geo.wing_params.v4dIndex:].tolist() + [p8d])
    curve9d = gmsh.model.geo.addPolyline([p1d] + points7d + [p8d])
    curve10d = gmsh.model.geo.addPolyline([p1d] + points8d + [p8d])
    curve11d = gmsh.model.geo.addPolyline([p3d] + points9d + [v4d])
    curve12d = gmsh.model.geo.addPolyline([p3d] + points10d + [v4d])
    curve13d = gmsh.model.geo.addPolyline([p4d] + points11d + [v3d])
    curve14d = gmsh.model.geo.addPolyline([p4d] + points12d + [v3d])
    curve15d = gmsh.model.geo.addPolyline([v1d] + points13d + [v2d])
    curve16d = gmsh.model.geo.addPolyline([v1d] + points14d + [v2d])

    # Define curve loops
    curveLoop1e = gmsh.model.geo.addCurveLoop([curve1e, curve11e, curve8e, -curve9e])
    curveLoop2e = gmsh.model.geo.addCurveLoop([curve2e, curve13e, curve7e, -curve11e])
    curveLoop3e = gmsh.model.geo.addCurveLoop([curve3e, curve15e, curve6e, -curve13e])
    curveLoop4e = gmsh.model.geo.addCurveLoop([curve4e, curve5e, -curve15e])
    curveLoop5e = gmsh.model.geo.addCurveLoop([curve1e, curve12e, curve8e, -curve10e])
    curveLoop6e = gmsh.model.geo.addCurveLoop([curve2e, curve14e, curve7e, -curve12e])
    curveLoop7e = gmsh.model.geo.addCurveLoop([curve3e, curve16e, curve6e, -curve14e])
    curveLoop8e = gmsh.model.geo.addCurveLoop([curve4e, curve5e, -curve16e])

    curveLoop1d = gmsh.model.geo.addCurveLoop([curve1d, curve11d, curve8d, -curve9d])
    curveLoop2d = gmsh.model.geo.addCurveLoop([curve2d, curve13d, curve7d, -curve11d])
    curveLoop3d = gmsh.model.geo.addCurveLoop([curve3d, curve15d, curve6d, -curve13d])
    curveLoop4d = gmsh.model.geo.addCurveLoop([curve4d, curve5d, -curve15d])
    curveLoop5d = gmsh.model.geo.addCurveLoop([curve1d, curve12d, curve8d, -curve10d])
    curveLoop6d = gmsh.model.geo.addCurveLoop([curve2d, curve14d, curve7d, -curve12d])
    curveLoop7d = gmsh.model.geo.addCurveLoop([curve3d, curve16d, curve6d, -curve14d])
    curveLoop8d = gmsh.model.geo.addCurveLoop([curve4d, curve5d, -curve16d])

    # Define surfaces
    surface1e = gmsh.model.geo.addSurfaceFilling([curveLoop1e])

    # Refinement
    root_chord = vector.norm(geo.wing_params.p1e - geo.wing_params.p8e)

    gmsh.model.mesh.field.add("Distance", 1); gmsh.model.mesh.field.setNumbers(1, "CurvesList", [curve1e]); gmsh.model.mesh.field.setNumber(1, "Sampling", 100)
    gmsh.model.mesh.field.add("Threshold", 2); gmsh.model.mesh.field.setNumber(2, "InField", 1); gmsh.model.mesh.field.setNumber(2, "SizeMin", lc * refinement_ratio); gmsh.model.mesh.field.setNumber(2, "SizeMax", lc); gmsh.model.mesh.field.setNumber(2, "DistMin", root_chord * 0.1); gmsh.model.mesh.field.setNumber(2, "DistMax", root_chord * 0.2)

    # gmsh.model.mesh.field.add("Distance", 3); gmsh.model.mesh.field.setNumbers(3, "CurvesList", [curve2e]); gmsh.model.mesh.field.setNumber(3, "Sampling", 100)
    # gmsh.model.mesh.field.add("Threshold", 4); gmsh.model.mesh.field.setNumber(4, "InField", 3); gmsh.model.mesh.field.setNumber(4, "SizeMin", lc * refinement_ratio); gmsh.model.mesh.field.setNumber(4, "SizeMax", lc); gmsh.model.mesh.field.setNumber(4, "DistMin", root_chord * 0.1); gmsh.model.mesh.field.setNumber(4, "DistMax", root_chord * 0.2)

    gmsh.model.mesh.field.add("Min", 3)
    gmsh.model.mesh.field.setNumbers(3, "FieldsList", [1, 2])

    gmsh.model.mesh.field.setAsBackgroundMesh(3)

    # gmsh.option.setNumber("Mesh.MeshSizeExtendFromBoundary", 0)
    # gmsh.option.setNumber("Mesh.MeshSizeFromPoints", 0)
    # gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 0)

    gmsh.model.geo.synchronize()
    gmsh.model.mesh.generate(2)

    surface2e = gmsh.model.geo.addSurfaceFilling([curveLoop2e])
    surface3e = gmsh.model.geo.addSurfaceFilling([curveLoop3e])
    surface4e = gmsh.model.geo.addSurfaceFilling([curveLoop4e])
    surface5e = gmsh.model.geo.addSurfaceFilling([curveLoop5e])
    surface6e = gmsh.model.geo.addSurfaceFilling([curveLoop6e])
    surface7e = gmsh.model.geo.addSurfaceFilling([curveLoop7e])
    surface8e = gmsh.model.geo.addSurfaceFilling([curveLoop8e])

    surface1d = gmsh.model.geo.addSurfaceFilling([curveLoop1d])
    surface2d = gmsh.model.geo.addSurfaceFilling([curveLoop2d])
    surface3d = gmsh.model.geo.addSurfaceFilling([curveLoop3d])
    surface4d = gmsh.model.geo.addSurfaceFilling([curveLoop4d])
    surface5d = gmsh.model.geo.addSurfaceFilling([curveLoop5d])
    surface6d = gmsh.model.geo.addSurfaceFilling([curveLoop6d])
    surface7d = gmsh.model.geo.addSurfaceFilling([curveLoop7d])
    surface8d = gmsh.model.geo.addSurfaceFilling([curveLoop8d])

    
    gmsh.model.geo.synchronize()
    gmsh.model.mesh.generate(2)

    #################################################################
    # Body
    #################################################################
    # Define points
    p9e = gmsh.model.geo.addPoint(geo.body_params.p9e[0], geo.body_params.p9e[1], geo.body_params.p9e[2], lc)
    p9d = gmsh.model.geo.addPoint(geo.body_params.p9d[0], geo.body_params.p9d[1], geo.body_params.p9d[2], lc)
    p10e = gmsh.model.geo.addPoint(geo.body_params.p10e[0], geo.body_params.p10e[1], geo.body_params.p10e[2], lc)
    p10d = gmsh.model.geo.addPoint(geo.body_params.p10d[0], geo.body_params.p10d[1], geo.body_params.p10d[2], lc)
    p11 = gmsh.model.geo.addPoint(geo.body_params.p11[0], geo.body_params.p11[1], geo.body_params.p11[2], lc)
    p12 = gmsh.model.geo.addPoint(geo.body_params.p12[0], geo.body_params.p12[1], geo.body_params.p12[2], lc)
    p13 = gmsh.model.geo.addPoint(geo.body_params.p13[0], geo.body_params.p13[1], geo.body_params.p13[2], lc)
    p14 = gmsh.model.geo.addPoint(geo.body_params.p14[0], geo.body_params.p14[1], geo.body_params.p14[2], lc)
    p15 = gmsh.model.geo.addPoint(geo.body_params.p15[0], geo.body_params.p15[1], geo.body_params.p15[2], lc)
    p16 = gmsh.model.geo.addPoint(geo.body_params.p16[0], geo.body_params.p16[1], geo.body_params.p16[2], lc)
    p17 = gmsh.model.geo.addPoint(geo.body_params.p17[0], geo.body_params.p17[1], geo.body_params.p17[2], lc)
    p18 = gmsh.model.geo.addPoint(geo.body_params.p18[0], geo.body_params.p18[1], geo.body_params.p18[2], lc)

    points15e = []
    size = len(geo.body_params.curve15e)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.body_params.curve15e[i, 0], geo.body_params.curve15e[i, 1], geo.body_params.curve15e[i, 2], lc)
            points15e.append(index)
    
    points15d = []
    size = len(geo.body_params.curve15d)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.body_params.curve15d[i, 0], geo.body_params.curve15d[i, 1], geo.body_params.curve15d[i, 2], lc)
            points15d.append(index)
    
    points16e = []
    size = len(geo.body_params.curve16e)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.body_params.curve16e[i, 0], geo.body_params.curve16e[i, 1], geo.body_params.curve16e[i, 2], lc)
            points16e.append(index)
    
    points16d = []
    size = len(geo.body_params.curve16d)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.body_params.curve16d[i, 0], geo.body_params.curve16d[i, 1], geo.body_params.curve16d[i, 2], lc)
            points16d.append(index)
    
    points17 = []
    size = len(geo.body_params.curve17)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.body_params.curve17[i, 0], geo.body_params.curve17[i, 1], geo.body_params.curve17[i, 2], lc)
            points17.append(index)
    
    points18 = []
    size = len(geo.body_params.curve18)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.body_params.curve18[i, 0], geo.body_params.curve18[i, 1], geo.body_params.curve18[i, 2], lc)
            points18.append(index)
    
    points19 = []
    size = len(geo.body_params.curve19)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.body_params.curve19[i, 0], geo.body_params.curve19[i, 1], geo.body_params.curve19[i, 2], lc)
            points19.append(index)
    
    points20 = []
    size = len(geo.body_params.curve20)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.body_params.curve20[i, 0], geo.body_params.curve20[i, 1], geo.body_params.curve20[i, 2], lc)
            points20.append(index)
    
    points21 = []
    size = len(geo.body_params.curve21)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.body_params.curve21[i, 0], geo.body_params.curve21[i, 1], geo.body_params.curve21[i, 2], lc)
            points21.append(index)
    
    points22 = []
    size = len(geo.body_params.curve22)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.body_params.curve22[i, 0], geo.body_params.curve22[i, 1], geo.body_params.curve22[i, 2], lc)
            points22.append(index)
    
    points23e = []
    size = len(geo.body_params.curve23e)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.body_params.curve23e[i, 0], geo.body_params.curve23e[i, 1], geo.body_params.curve23e[i, 2], lc)
            points23e.append(index)
    
    points23d = []
    size = len(geo.body_params.curve23d)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.body_params.curve23d[i, 0], geo.body_params.curve23d[i, 1], geo.body_params.curve23d[i, 2], lc)
            points23d.append(index)
    
    points24e = []
    size = len(geo.body_params.curve24e)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.body_params.curve24e[i, 0], geo.body_params.curve24e[i, 1], geo.body_params.curve24e[i, 2], lc)
            points24e.append(index)
    
    points24d = []
    size = len(geo.body_params.curve24d)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.body_params.curve24d[i, 0], geo.body_params.curve24d[i, 1], geo.body_params.curve24d[i, 2], lc)
            points24d.append(index)
    
    points25e = []
    size = len(geo.body_params.curve25e)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.body_params.curve25e[i, 0], geo.body_params.curve25e[i, 1], geo.body_params.curve25e[i, 2], lc)
            points25e.append(index)
    
    points25d = []
    size = len(geo.body_params.curve25d)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.body_params.curve25d[i, 0], geo.body_params.curve25d[i, 1], geo.body_params.curve25d[i, 2], lc)
            points25d.append(index)
    
    points26e = []
    size = len(geo.body_params.curve26e)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.body_params.curve26e[i, 0], geo.body_params.curve26e[i, 1], geo.body_params.curve26e[i, 2], lc)
            points26e.append(index)
    
    points26d = []
    size = len(geo.body_params.curve26e)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.body_params.curve26d[i, 0], geo.body_params.curve26d[i, 1], geo.body_params.curve26d[i, 2], lc)
            points26d.append(index)
    
    points27 = []
    size = len(geo.body_params.curve27)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.body_params.curve27[i, 0], geo.body_params.curve27[i, 1], geo.body_params.curve27[i, 2], lc)
            points27.append(index)
    
    points28 = []
    size = len(geo.body_params.curve28)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.body_params.curve28[i, 0], geo.body_params.curve28[i, 1], geo.body_params.curve28[i, 2], lc)
            points28.append(index)
    
    points29 = []
    size = len(geo.body_params.curve29)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.body_params.curve29[i, 0], geo.body_params.curve29[i, 1], geo.body_params.curve29[i, 2], lc)
            points29.append(index)
    
    points30 = []
    size = len(geo.body_params.curve30)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.body_params.curve30[i, 0], geo.body_params.curve30[i, 1], geo.body_params.curve30[i, 2], lc)
            points30.append(index)
    
    points31 = []
    size = len(geo.body_params.curve31)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.body_params.curve31[i, 0], geo.body_params.curve31[i, 1], geo.body_params.curve31[i, 2], lc)
            points31.append(index)
    
    points32 = []
    size = len(geo.body_params.curve32)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.body_params.curve32[i, 0], geo.body_params.curve32[i, 1], geo.body_params.curve32[i, 2], lc)
            points32.append(index)
    
    points33 = []
    size = len(geo.body_params.curve33)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.body_params.curve33[i, 0], geo.body_params.curve33[i, 1], geo.body_params.curve33[i, 2], lc)
            points33.append(index)
    
    points34 = []
    size = len(geo.body_params.curve34)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.body_params.curve34[i, 0], geo.body_params.curve34[i, 1], geo.body_params.curve34[i, 2], lc)
            points34.append(index)
    
    # Define curves
    curve15e = gmsh.model.geo.addPolyline([p9e] + points15e + [p1e])
    curve15d = gmsh.model.geo.addPolyline([p9d] + points15d + [p1d])
    curve16e = gmsh.model.geo.addPolyline([p8e] + points16e + [p10e])
    curve16d = gmsh.model.geo.addPolyline([p8d] + points16d + [p10d])
    curve17 = gmsh.model.geo.addPolyline([p11] + points17 + [p12])
    curve18 = gmsh.model.geo.addPolyline([p12] + points18 + [p13])
    curve19 = gmsh.model.geo.addPolyline([p13] + points19 + [p14])
    curve20 = gmsh.model.geo.addPolyline([p15] + points20 + [p16])
    curve21 = gmsh.model.geo.addPolyline([p16] + points21 + [p17])
    curve22 = gmsh.model.geo.addPolyline([p17] + points22 + [p18])
    curve23e = gmsh.model.geo.addPolyline([p12] + points23e + [p1e])
    curve23d = gmsh.model.geo.addPolyline([p12] + points23d + [p1d])
    curve24e = gmsh.model.geo.addPolyline([p1e] + points24e + [p17])
    curve24d = gmsh.model.geo.addPolyline([p1d] + points24d + [p17])
    curve25e = gmsh.model.geo.addPolyline([p13] + points25e + [p8e])
    curve25d = gmsh.model.geo.addPolyline([p13] + points25d + [p8d])
    curve26e = gmsh.model.geo.addPolyline([p8e] + points26e + [p16])
    curve26d = gmsh.model.geo.addPolyline([p8d] + points26d + [p16])
    curve27 = gmsh.model.geo.addPolyline([p11] + points27 + [p9e])
    curve28 = gmsh.model.geo.addPolyline([p9e] + points28 + [p18])
    curve29 = gmsh.model.geo.addPolyline([p18] + points29 + [p9d])
    curve30= gmsh.model.geo.addPolyline([p9d] + points30 + [p11])
    curve31 = gmsh.model.geo.addPolyline([p14] + points31 + [p10e])
    curve32 = gmsh.model.geo.addPolyline([p10e] + points32 + [p15])
    curve33 = gmsh.model.geo.addPolyline([p15] + points33 + [p10d])
    curve34 = gmsh.model.geo.addPolyline([p10d] + points34 + [p14])

    # Define curve loops
    curveLoop9e = gmsh.model.geo.addCurveLoop([curve15e, -curve23e, -curve17, curve27], reorient=True)
    curveLoop10e = gmsh.model.geo.addCurveLoop([curve9e, curve25e, curve18, curve23e], reorient=True)
    curveLoop11e = gmsh.model.geo.addCurveLoop([curve16e, curve31, curve19, curve25e], reorient=True)
    curveLoop12e = gmsh.model.geo.addCurveLoop([curve20, curve26e, curve16e, curve32], reorient=True)
    curveLoop13e = gmsh.model.geo.addCurveLoop([curve21, curve24e, curve10e, curve26e], reorient=True)
    curveLoop14e = gmsh.model.geo.addCurveLoop([curve22, curve28, curve15e, curve24e], reorient=True)

    curveLoop9d = gmsh.model.geo.addCurveLoop([curve15d, -curve23d, -curve17, curve30], reorient=True)
    curveLoop10d = gmsh.model.geo.addCurveLoop([curve9d, curve25d, curve18, curve23d], reorient=True)
    curveLoop11d = gmsh.model.geo.addCurveLoop([curve16d, curve34, curve19, curve25d], reorient=True)
    curveLoop12d = gmsh.model.geo.addCurveLoop([curve20, curve26d, curve16d, curve33], reorient=True)
    curveLoop13d = gmsh.model.geo.addCurveLoop([curve21, curve24d, curve10d, curve26d], reorient=True)
    curveLoop14d = gmsh.model.geo.addCurveLoop([curve22, curve29, curve15d, curve24d], reorient=True)

    # Define surfaces
    surface9e = gmsh.model.geo.addSurfaceFilling([curveLoop9e])
    surface10e = gmsh.model.geo.addSurfaceFilling([curveLoop10e])
    surface11e = gmsh.model.geo.addSurfaceFilling([curveLoop11e])
    surface12e = gmsh.model.geo.addSurfaceFilling([curveLoop12e])
    surface13e = gmsh.model.geo.addSurfaceFilling([curveLoop13e])
    surface14e = gmsh.model.geo.addSurfaceFilling([curveLoop14e])

    surface9d = gmsh.model.geo.addSurfaceFilling([curveLoop9d])
    surface10d = gmsh.model.geo.addSurfaceFilling([curveLoop10d])
    surface11d = gmsh.model.geo.addSurfaceFilling([curveLoop11d])
    surface12d = gmsh.model.geo.addSurfaceFilling([curveLoop12d])
    surface13d = gmsh.model.geo.addSurfaceFilling([curveLoop13d])
    surface14d = gmsh.model.geo.addSurfaceFilling([curveLoop14d])

    #################################################################
    # Tail
    #################################################################
    # Define points
    p19e = gmsh.model.geo.addPoint(geo.tail_params.p19e[0], geo.tail_params.p19e[1], geo.tail_params.p19e[2], lc)
    p19d = gmsh.model.geo.addPoint(geo.tail_params.p19d[0], geo.tail_params.p19d[1], geo.tail_params.p19d[2], lc)
    p20 = gmsh.model.geo.addPoint(geo.tail_params.p20[0], geo.tail_params.p20[1], geo.tail_params.p20[2], lc)
    v5e = gmsh.model.geo.addPoint(geo.tail_params.v5e[0], geo.tail_params.v5e[1], geo.tail_params.v5e[2], lc)
    v6e = gmsh.model.geo.addPoint(geo.tail_params.v6e[0], geo.tail_params.v6e[1], geo.tail_params.v6e[2], lc)
    v7e = gmsh.model.geo.addPoint(geo.tail_params.v7e[0], geo.tail_params.v7e[1], geo.tail_params.v7e[2], lc)
    v5d = gmsh.model.geo.addPoint(geo.tail_params.v5d[0], geo.tail_params.v5d[1], geo.tail_params.v5d[2], lc)
    v6d = gmsh.model.geo.addPoint(geo.tail_params.v6d[0], geo.tail_params.v6d[1], geo.tail_params.v6d[2], lc)
    v7d = gmsh.model.geo.addPoint(geo.tail_params.v7d[0], geo.tail_params.v7d[1], geo.tail_params.v7d[2], lc)

    points35e = []
    size = len(geo.tail_params.curve35e)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.tail_params.curve35e[i, 0], geo.tail_params.curve35e[i, 1], geo.tail_params.curve35e[i, 2], lc)
            points35e.append(index)
    
    points35d = []
    size = len(geo.tail_params.curve35d)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.tail_params.curve35d[i, 0], geo.tail_params.curve35d[i, 1], geo.tail_params.curve35d[i, 2], lc)
            points35d.append(index)
    
    points36e = []
    size = len(geo.tail_params.curve36e)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.tail_params.curve36e[i, 0], geo.tail_params.curve36e[i, 1], geo.tail_params.curve36e[i, 2], lc)
            points36e.append(index)
    
    points36d = []
    size = len(geo.tail_params.curve36d)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.tail_params.curve36d[i, 0], geo.tail_params.curve36d[i, 1], geo.tail_params.curve36d[i, 2], lc)
            points36d.append(index)
    
    points37 = []
    size = len(geo.tail_params.curve37)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.tail_params.curve37[i, 0], geo.tail_params.curve37[i, 1], geo.tail_params.curve37[i, 2], lc)
            points37.append(index)
    
    points38 = []
    size = len(geo.tail_params.curve38)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.tail_params.curve38[i, 0], geo.tail_params.curve38[i, 1], geo.tail_params.curve38[i, 2], lc)
            points38.append(index)
    
    points49e = []
    size = len(geo.tail_params.curve39e)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.tail_params.curve39e[i, 0], geo.tail_params.curve39e[i, 1], geo.tail_params.curve39e[i, 2], lc)
            points49e.append(index)
    
    points50e = []
    size = len(geo.tail_params.curve40e)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.tail_params.curve40e[i, 0], geo.tail_params.curve40e[i, 1], geo.tail_params.curve40e[i, 2], lc)
            points50e.append(index)
    
    points51e = []
    size = len(geo.tail_params.curve41e)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.tail_params.curve41e[i, 0], geo.tail_params.curve41e[i, 1], geo.tail_params.curve41e[i, 2], lc)
            points51e.append(index)
    
    points52e = []
    size = len(geo.tail_params.curve42e)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.tail_params.curve42e[i, 0], geo.tail_params.curve42e[i, 1], geo.tail_params.curve42e[i, 2], lc)
            points52e.append(index)
    
    points49d = []
    size = len(geo.tail_params.curve39d)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.tail_params.curve39d[i, 0], geo.tail_params.curve39d[i, 1], geo.tail_params.curve39d[i, 2], lc)
            points49d.append(index)
    
    points50d = []
    size = len(geo.tail_params.curve40d)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.tail_params.curve40d[i, 0], geo.tail_params.curve40d[i, 1], geo.tail_params.curve40d[i, 2], lc)
            points50d.append(index)
    
    points51d = []
    size = len(geo.tail_params.curve41d)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.tail_params.curve41d[i, 0], geo.tail_params.curve41d[i, 1], geo.tail_params.curve41d[i, 2], lc)
            points51d.append(index)
    
    points52d = []
    size = len(geo.tail_params.curve42d)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.tail_params.curve42d[i, 0], geo.tail_params.curve42d[i, 1], geo.tail_params.curve42d[i, 2], lc)
            points52d.append(index)
    
    # Define curves
    curve35e1 = gmsh.model.geo.addPolyline([p10e] + asarray(points35e)[:geo.tail_params.v7eIndex - 1].tolist() + [v7e])
    curve35e2 = gmsh.model.geo.addPolyline([v7e] + asarray(points35e)[geo.tail_params.v7eIndex:].tolist() + [p19e])
    curve35d1 = gmsh.model.geo.addPolyline([p10d] + asarray(points35d)[:geo.tail_params.v7dIndex - 1].tolist() + [v7d])
    curve35d2 = gmsh.model.geo.addPolyline([v7d] + asarray(points35d)[geo.tail_params.v7dIndex:].tolist() + [p19d])

    curve36e1 = gmsh.model.geo.addPolyline([p19e] + asarray(points36e)[:geo.tail_params.v6eIndex - 1].tolist() + [v6e])
    curve36e2 = gmsh.model.geo.addPolyline([v6e] + asarray(points36e)[geo.tail_params.v6eIndex:geo.tail_params.v5eIndex - 1].tolist() + [v5e])
    curve36e3 = gmsh.model.geo.addPolyline([v5e] + asarray(points36e)[geo.tail_params.v5eIndex:].tolist() + [p20])
    curve36d1 = gmsh.model.geo.addPolyline([p19d] + asarray(points36d)[:geo.tail_params.v6dIndex - 1].tolist() + [v6d])
    curve36d2 = gmsh.model.geo.addPolyline([v6d] + asarray(points36d)[geo.tail_params.v6dIndex:geo.tail_params.v5dIndex - 1].tolist() + [v5d])
    curve36d3 = gmsh.model.geo.addPolyline([v5d] + asarray(points36d)[geo.tail_params.v5dIndex:].tolist() + [p20])

    curve37 = gmsh.model.geo.addPolyline([p14] + points37 + [p20])
    curve38 = gmsh.model.geo.addPolyline([p15] + points38 + [p20])

    curve49e = gmsh.model.geo.addPolyline([p10e] + points49e + [v5e])
    curve50e = gmsh.model.geo.addPolyline([p10e] + points50e + [v5e])
    curve51e= gmsh.model.geo.addPolyline([v7e] + points51e + [v6e])
    curve52e = gmsh.model.geo.addPolyline([v7e] + points52e + [v6e])
    curve49d = gmsh.model.geo.addPolyline([p10d] + points49d + [v5d])
    curve50d= gmsh.model.geo.addPolyline([p10d] + points50d + [v5d])
    curve51d = gmsh.model.geo.addPolyline([v7d] + points51d + [v6d])
    curve52d = gmsh.model.geo.addPolyline([v7d] + points52d + [v6d])

    # Define curve loops
    curveLoop15e1 = gmsh.model.geo.addCurveLoop([curve31, curve49e, curve36e3, curve37], reorient=True)
    curveLoop15e2 = gmsh.model.geo.addCurveLoop([curve35e1, curve51e, curve36e2, curve49e], reorient=True)
    curveLoop15e3 = gmsh.model.geo.addCurveLoop([curve35e2, curve36e1, curve51e], reorient=True)

    curveLoop16e1 = gmsh.model.geo.addCurveLoop([curve32, curve50e, curve36e3, curve38], reorient=True)
    curveLoop16e2 = gmsh.model.geo.addCurveLoop([curve35e1, curve52e, curve36e2, curve50e], reorient=True)
    curveLoop16e3 = gmsh.model.geo.addCurveLoop([curve35e2, curve36e1, curve52e], reorient=True)

    curveLoop15d1 = gmsh.model.geo.addCurveLoop([curve34, curve49d, curve36d3, curve37], reorient=True)
    curveLoop15d2 = gmsh.model.geo.addCurveLoop([curve35d1, curve51d, curve36d2, curve49d], reorient=True)
    curveLoop15d3 = gmsh.model.geo.addCurveLoop([curve35d2, curve36d1, curve51d], reorient=True)

    curveLoop16d1 = gmsh.model.geo.addCurveLoop([curve33, curve50d, curve36d3, curve38], reorient=True)
    curveLoop16d2 = gmsh.model.geo.addCurveLoop([curve35d1, curve52d, curve36d2, curve50d], reorient=True)
    curveLoop16d3 = gmsh.model.geo.addCurveLoop([curve35d2, curve36d1, curve52d], reorient=True)


    # # Define surfaces
    surface15e1 = gmsh.model.geo.addSurfaceFilling([curveLoop15e1])
    surface15e2 = gmsh.model.geo.addSurfaceFilling([curveLoop15e2])
    surface15e3 = gmsh.model.geo.addSurfaceFilling([curveLoop15e3])
    surface16e1 = gmsh.model.geo.addSurfaceFilling([curveLoop16e1])
    surface16e2 = gmsh.model.geo.addSurfaceFilling([curveLoop16e2])
    surface16e3 = gmsh.model.geo.addSurfaceFilling([curveLoop16e3])

    surface15d1 = gmsh.model.geo.addSurfaceFilling([curveLoop15d1])
    surface15d2 = gmsh.model.geo.addSurfaceFilling([curveLoop15d2])
    surface15d3 = gmsh.model.geo.addSurfaceFilling([curveLoop15d3])
    surface16d1 = gmsh.model.geo.addSurfaceFilling([curveLoop16d1])
    surface16d2 = gmsh.model.geo.addSurfaceFilling([curveLoop16d2])
    surface16d3 = gmsh.model.geo.addSurfaceFilling([curveLoop16d3])

    #################################################################
    # Head
    #################################################################
    # Define points
    p21e = gmsh.model.geo.addPoint(geo.head_params.p21e[0], geo.head_params.p21e[1], geo.head_params.p21e[2], lc)
    p21d = gmsh.model.geo.addPoint(geo.head_params.p21d[0], geo.head_params.p21d[1], geo.head_params.p21d[2], lc)
    p22 = gmsh.model.geo.addPoint(geo.head_params.p22[0], geo.head_params.p22[1], geo.head_params.p22[2], lc)
    p23 = gmsh.model.geo.addPoint(geo.head_params.p23[0], geo.head_params.p23[1], geo.head_params.p23[2], lc)
    p24 = gmsh.model.geo.addPoint(geo.head_params.p24[0], geo.head_params.p24[1], geo.head_params.p24[2], lc)
    
    points39e = []
    size = len(geo.head_params.curve39e)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.head_params.curve39e[i, 0], geo.head_params.curve39e[i, 1], geo.head_params.curve39e[i, 2], lc)
            points39e.append(index)
    
    points39d = []
    size = len(geo.head_params.curve39d)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.head_params.curve39d[i, 0], geo.head_params.curve39d[i, 1], geo.head_params.curve39d[i, 2], lc)
            points39d.append(index)
    
    points40e = []
    size = len(geo.head_params.curve40e)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.head_params.curve40e[i, 0], geo.head_params.curve40e[i, 1], geo.head_params.curve40e[i, 2], lc)
            points40e.append(index)
    
    points40d = []
    size = len(geo.head_params.curve40d)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.head_params.curve40d[i, 0], geo.head_params.curve40d[i, 1], geo.head_params.curve40d[i, 2], lc)
            points40d.append(index)
    
    points41 = []
    size = len(geo.head_params.curve41)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.head_params.curve41[i, 0], geo.head_params.curve41[i, 1], geo.head_params.curve41[i, 2], lc)
            points41.append(index)
    
    points42 = []
    size = len(geo.head_params.curve42)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.head_params.curve42[i, 0], geo.head_params.curve42[i, 1], geo.head_params.curve42[i, 2], lc)
            points42.append(index)
    
    points43 = []
    size = len(geo.head_params.curve43)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.head_params.curve43[i, 0], geo.head_params.curve43[i, 1], geo.head_params.curve43[i, 2], lc)
            points43.append(index)
    
    points44 = []
    size = len(geo.head_params.curve44)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.head_params.curve44[i, 0], geo.head_params.curve44[i, 1], geo.head_params.curve44[i, 2], lc)
            points44.append(index)
    
    points45 = []
    size = len(geo.head_params.curve45)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.head_params.curve45[i, 0], geo.head_params.curve45[i, 1], geo.head_params.curve45[i, 2], lc)
            points45.append(index)
    
    points46 = []
    size = len(geo.head_params.curve46)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.head_params.curve46[i, 0], geo.head_params.curve46[i, 1], geo.head_params.curve46[i, 2], lc)
            points46.append(index)
    
    points47 = []
    size = len(geo.head_params.curve47)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.head_params.curve47[i, 0], geo.head_params.curve47[i, 1], geo.head_params.curve47[i, 2], lc)
            points47.append(index)
    
    points48 = []
    size = len(geo.head_params.curve48)
    for i in range(size):
        if i != 0 and i != size - 1:
            index = gmsh.model.geo.addPoint(geo.head_params.curve48[i, 0], geo.head_params.curve48[i, 1], geo.head_params.curve48[i, 2], lc)
            points48.append(index)
    
    # Define curves
    curve39e = gmsh.model.geo.addPolyline([p9e] + points39e + [p21e])
    curve39d = gmsh.model.geo.addPolyline([p9d] + points39d + [p21d])
    curve40e = gmsh.model.geo.addPolyline([p21e] + points40e + [p22])
    curve40d = gmsh.model.geo.addPolyline([p21d] + points40d + [p22])
    curve41 = gmsh.model.geo.addPolyline([p11] + points41 + [p23])
    curve42 = gmsh.model.geo.addPolyline([p18] + points42 + [p24])
    curve43 = gmsh.model.geo.addPolyline([p23] + points43 + [p22])
    curve44 = gmsh.model.geo.addPolyline([p24] + points44 + [p22])
    curve45 = gmsh.model.geo.addPolyline([p23] + points45 + [p21e])
    curve46 = gmsh.model.geo.addPolyline([p21e] + points46 + [p24])
    curve47 = gmsh.model.geo.addPolyline([p24] + points47 + [p21d])
    curve48 = gmsh.model.geo.addPolyline([p21d] + points48 + [p23])

    # Define curve loops
    curveLoop17e = gmsh.model.geo.addCurveLoop([curve39e, curve45, curve41, curve27], reorient=True)
    curveLoop18e = gmsh.model.geo.addCurveLoop([curve40e, curve43, curve45], reorient=True)
    curveLoop19e = gmsh.model.geo.addCurveLoop([curve39e, curve46, curve42, curve28], reorient=True)
    curveLoop20e = gmsh.model.geo.addCurveLoop([curve40e, curve44, curve46], reorient=True)
    curveLoop17d = gmsh.model.geo.addCurveLoop([curve39d, curve48, curve41, curve30], reorient=True)
    curveLoop18d = gmsh.model.geo.addCurveLoop([curve40d, curve43, curve48], reorient=True)
    curveLoop19d = gmsh.model.geo.addCurveLoop([curve39d, curve47, curve42, curve29], reorient=True)
    curveLoop20d = gmsh.model.geo.addCurveLoop([curve40d, curve44, curve47], reorient=True)

    # Define surfaces
    surface17e = gmsh.model.geo.addSurfaceFilling([curveLoop17e])
    surface18e = gmsh.model.geo.addSurfaceFilling([curveLoop18e])
    surface19e = gmsh.model.geo.addSurfaceFilling([curveLoop19e])
    surface20e = gmsh.model.geo.addSurfaceFilling([curveLoop20e])
    surface17d = gmsh.model.geo.addSurfaceFilling([curveLoop17d])
    surface18d = gmsh.model.geo.addSurfaceFilling([curveLoop18d])
    surface19d = gmsh.model.geo.addSurfaceFilling([curveLoop19d])
    surface20d = gmsh.model.geo.addSurfaceFilling([curveLoop20d])

    # Build mesh
    # gmsh.option.setNumber("Mesh.Algorithm", 5)
    # gmsh.model.geo.synchronize()
    # gmsh.model.mesh.generate(2)

    if '-nopopup' not in sys.argv:
        gmsh.fltk.run()
    
    gmsh.finalize()