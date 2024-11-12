import open3d
import numpy as np

def reconstruct_mesh(pcd):
    mesh = open3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=10, n_threads=1)[0]
    rotation = mesh.get_rotation_matrix_from_xyz((np.pi, 0, 0))
    mesh.rotate(rotation, center=(0, 0, 0))
    return mesh

def export_mesh(mesh, output_path):
    open3d.io.write_triangle_mesh(output_path + ".obj", mesh, write_vertex_normals=True, 
                                  write_vertex_colors=True, write_triangle_uvs=True)
