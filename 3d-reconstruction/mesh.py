import open3d
import numpy as np


# Reconstructs a 3D mesh from a point cloud using Poisson surface reconstruction
def reconstruct_mesh(point_cloud):

    # Perform Poisson surface reconstruction with a specified octree depth (higher values improve resolution but require more resources)
    mesh = open3d.geometry.TriangleMesh.create_from_point_cloud_poisson(point_cloud, depth=10, n_threads=1)[0]

    # Rotate the mesh by 180 degrees around the X-axis to align it properly
    rotation = mesh.get_rotation_matrix_from_xyz((np.pi, 0, 0))
    mesh.rotate(rotation, center=(0, 0, 0))

    return mesh

# Exports the reconstructed 3D mesh to a file in OBJ format with vertex normals, colors, and UVs
def export_mesh(mesh, output_path):
    open3d.io.write_triangle_mesh(output_path + ".obj", mesh, write_vertex_normals=True, 
                                  write_vertex_colors=True, write_triangle_uvs=True)
