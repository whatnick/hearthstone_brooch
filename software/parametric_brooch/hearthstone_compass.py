import cadquery as cq
from cqmore import Workplane
from cqmore.curve import logarithmicSpiral
import math
import numpy as np

# Define the compass parameters

# Tetrahedral
edge_length = 10  # Length of the shortest edge
longest_edge_length = 30  # Length of the longest edge
scaling_factor = 1.4

# Circle sweeps
cabochon_radius = 25 # Width of the central section
cabochon_height = 10 # Thickness of the central section
height_ratio = 0.6 # Centre to edge ring ratio
ring_base = 15

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

def create_spiral_extrude(iterations = 5, width = cabochon_radius, height = cabochon_height):
    # https://github.com/CadQuery/cadquery/pull/110
    # Use parametric curve for spiral
    # Offset by certain amount or buffer with angular edges
    spiral_pts = np.array(
        [logarithmicSpiral(t / 14) for t in range(14 * iterations)])/(cabochon_radius*30)
    fib_spiral = (Workplane()
            .polyline(spiral_pts)
         )
    
    spiral_extrude = (
        cq.Workplane("YZ")
        .rect(5, height * 2)
        .sweep(fib_spiral, transition="round" )
    )
    
    spiral_extrude = spiral_extrude.translate((-width/8, width/4,0))
    spiral_extrude = spiral_extrude.mirror(mirrorPlane="XZ")

    return spiral_extrude

# Create the tetrahedron object
tetrahedron_obj = create_tetrahedron(edge_length, longest_edge_length, scaling_factor)

# Create 4 copies of the tetrahedron rotated at 4 points of the compass
tetrahedrons_outer = tetrahedron_circle(tetrahedron_obj, 6)
tetrahedrons_inner = tetrahedron_circle(tetrahedron_obj, 5, 45)

# Create circular swept ring and cabochon
rv = tri_ring(cabochon_radius, ring_base, cabochon_height * height_ratio)
cabochon = create_cabochon_profile(cabochon_radius , cabochon_height)

# Add Spiral and subtract from Cabochon
central_spiral = create_spiral_extrude()

# Display the model
show_object(tetrahedrons_outer)
show_object(tetrahedrons_inner)
show_object(rv)
show_object(cabochon)
show_object(central_spiral)
