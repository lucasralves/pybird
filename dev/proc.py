from py.create_mesh import create_mesh
from py.correct_vertices_ids import correct_vertices_ids
from py.solve import solve
from py.create_vtp_file import create_vtp_file

# Create mesh
vertices, faces3, faces4, trailing_edge_list = create_mesh(foilname='./data/NACA0009.dat', span=5.0, n_span=5, n_chord_1=20, n_chord_2=4, n_chord_3=10, coef_le=10.0, coef_te=1.1)

# Correct ids
vertices_out, faces_out, trailing_edge_out = correct_vertices_ids(vertices, faces3, faces4, trailing_edge_list)

# Solve
freestream = 1.0
alpha = 0.0
beta = 0.0
delta_t = 1.0
wake_length = 5.0
data = solve(vertices_out, faces_out, trailing_edge_out, freestream, alpha, beta, delta_t, wake_length)

# Create vtp file
create_vtp_file(vertices_out, faces_out, data)