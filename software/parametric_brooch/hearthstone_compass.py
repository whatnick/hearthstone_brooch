import cadquery as cq
from cqmore import Workplane
import math

# Define the tetrahedral parameters
edge_length = 10  # Length of the shortest edge
longest_edge_length = 30  # Length of the longest edge
scaling_factor = 1.4

# Create a tetrahedron
def create_tetrahedron(edge_length, longest_edge_length, scaling_factor ):
    # Calculate the scaled length of the longest edge
    scaled_longest_edge_length = longest_edge_length * scaling_factor

    # Calculate the intermediate edge length
    intermediate_edge_length = (scaled_longest_edge_length + edge_length) / 2

    # Define the tetrahedron vertices
    vertices = [
        (0, 0, 0),
        (longest_edge_length, intermediate_edge_length/2, 0),
        (longest_edge_length, -intermediate_edge_length/2, 0),
        (edge_length, 0, edge_length),
    ]

    # Create the CadQuery tetrahedron
    # Define the tetrahedron faces
    faces = [
        [0, 1, 2],
        [0, 2, 3],
        [0, 3, 1],
        [1, 3, 2],
    ]

    # Create the CadQuery tetrahedron
    tetrahedron = Workplane().polyhedron(vertices, faces)

    return tetrahedron

# Create array of tetrahedrons in circle
def tetrahedron_circle(in_tetrahedron,linear_offset, angular_offset = 0):
    offset_distance = linear_offset * edge_length

    # Offset the tetrahedron
    offset_tetrahedron = in_tetrahedron.translate((-offset_distance, 0, 0))

    # Create 4 copies of the tetrahedron rotated at 4 points of the compass
    tetrahedrons = cq.Assembly()
    for i in range(4):
        angle = i * 90 + angular_offset
        rotated_copy = offset_tetrahedron.rotate((0, 0, 0), (0, 0, 1), angle)
        tetrahedrons.add(rotated_copy)
    
    return tetrahedrons

def tri_ring(radius, base_width, height):
    path = cq.Workplane().circle(5)

    rv = (
        cq.Workplane("YZ")
        .polyline([(radius,0),(radius+base_width,0),(radius + base_width/2, height),(radius,0)])
        .close()
        .sweep(path, transition="round")
    )
    return rv

def create_cabochon_profile(radius, height):
    # Define the radius and height of the cabochon
    cabochon_radius = radius
    cabochon_height = height
    path = cq.Workplane().circle(5)
    # Define the center point of the arc
    cabochon = (cq.Workplane("YZ")
        .lineTo(radius, 0)
        .threePointArc((0.0, height), (-radius, 0.0))
        .close()
        .sweep(path, transition="round"))

    return cabochon

# Create the tetrahedron object
tetrahedron_obj = create_tetrahedron(edge_length, longest_edge_length, scaling_factor)

# Create 4 copies of the tetrahedron rotated at 4 points of the compass
tetrahedrons_outer = tetrahedron_circle(tetrahedron_obj, 6)
tetrahedrons_inner = tetrahedron_circle(tetrahedron_obj, 5, 45)


# Display the model
show_object(tetrahedrons_outer)
show_object(tetrahedrons_inner)

rv = tri_ring(25, 15, 6)
cabochon = create_cabochon_profile(25, 10)

show_object(rv)
show_object(cabochon)
