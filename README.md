# pybird

## Modules

### Geometry

The geometry module components is shown in the Figure below. There are 5 methods available in the geo class:

- load('file.geo'): file.geo contains a dict saved as a json file with all intermediate variables necessary to define the geometry.
- save('file.geo'): save the _data into a file.
- ui(): shows a ui to facilitate the intermediate variables definition.
- addRotation('x1', 45, 'left'): add a rotation to the wing with the parameters axis, angle (degrees) and wing side.
- removeRotations(): remove all rotations.
- updateValue('l1', 1.0): update an intermediate value.

The parameter _data is a dict that contains the information loaded from the method load and params is a class that calculate all the control points based on the _data values.

![geo_components](/doc/geo_components.png "Geoemtry module components")