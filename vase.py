# Michelle Wong PRA1817277 on 24th April
# This program generates an ASCII STL file for a simple vase with 7 user given parameters for height and radius

import math
import numpy as np 
import os
import time

################################################
################## CLASSES #####################
################################################

class Point:
    def __init__(self, pt):
        self.pt = pt # np array

class Facet:
    def __init__(self, v1, v2, v3, normal):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.normal = normal

class Vase:
    def __init__(self, base_fcts, low_fcts, mid_fcts, top_fcts):
        self.base_fcts = base_fcts
        self.low_fcts = low_fcts
        self.mid_fcts  = mid_fcts
        self.top_fcts  = top_fcts

################################################
########### FILE MODIFICATION HELPERS ##########
################################################

def write_line_to_file(file_path, line):
    with open(file_path, 'a') as file:
        file.write(line)

def clear_file(file_path):
    """Clear the contents of a file."""
    with open(file_path, 'w') as file:
        file.truncate(0)  # Truncate the file to 0 bytes

def create_output_directory(directory_name):
    """Create the output directory if it doesn't exist."""
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

def generate_unique_filename():
    """Generate a unique filename using the current timestamp."""
    timestamp = int(time.time())
    return f"vase_{timestamp}.stl"  
    # Example filename format: vase_<timestamp>.stl

################################################
########### VASE GENERATION HELPERS ############
################################################

# Given the 3 vertexes and normal vector for a facet, 
# Returns a facet string properly formatted for an ASCII STL file
def format_facet(facet):
    # Create a template string for the facet
    facet_template = """
    facet normal {0} {1} {2}
        outer loop
            vertex {3} {4} {5}
            vertex {6} {7} {8}
            vertex {9} {10} {11}
        endloop
    endfacet
    """
    n = facet.normal.tolist()
    v1 = facet.v1.tolist()
    v2 = facet.v2.tolist()
    v3 = facet.v3.tolist()

    
    # Format all floats in scientific notation and fill in the template
    # Vertexes should be in anticlockwise format
    facet_str = facet_template.format(
        format(n[0], ".6e"), format(n[1], ".6e"), format(n[2], ".6e"),
        format(v1[0], ".6e"), format(v1[1], ".6e"), format(v1[2], ".6e"),
        format(v2[0], ".6e"), format(v2[1], ".6e"), format(v2[2], ".6e"),
        format(v3[0], ".6e"), format(v3[1], ".6e"), format(v3[2], ".6e")
    )
    return facet_str

# Writes a complete set of facets to file
def write_facet_set(filename, set_of_fcts):
    for facet in set_of_fcts:
        write_line_to_file(filename, format_facet(facet))

# Writes the ASCII STL file from start to finish
def write_stl(vase):
    dir_name = "output"
    create_output_directory(dir_name)
    filename = os.path.join(dir_name, generate_unique_filename())

    clear_file(filename) # In case it already exists

    write_line_to_file(filename, "solid vase\n")

    write_facet_set(filename, vase.base_fcts)
    write_facet_set(filename, vase.low_fcts)
    write_facet_set(filename, vase.mid_fcts)
    write_facet_set(filename, vase.top_fcts)

    write_line_to_file(filename, "endsolid\n")

    print(f"Your finished vase is written in STL file '{filename}'.")

# Generates points in a radius given additional parameters the height from base and number of sides
# The first point will appear at the start and the end in a circular fashion, ie. [pt1, pt2, pt3, .... pt1]
def generate_pts(radius, height, num_sides):
    points = []

    angle = np.radians(360/num_sides) # The angle of difference between each vertice 

    # Define the transformation matrix to rotate angle_of_diff around the z axis
    # Note that this is anti clockwise rotation
    rotation_matrix = np.array([[np.cos(angle), -1 * np.sin(angle), 0],
                [np.sin(angle), np.cos(angle), 0],
                [0, 0, 1]])
    
    # Start on the x axis (potentially elevated)
    start_pt = Point(np.array([0, radius, height])) 
    curr_pt = start_pt
    points.append(start_pt)
    # Note: -1 because the start point has already been appended
    for i in range(num_sides - 1):
        rotated_point = Point(np.dot(rotation_matrix, curr_pt.pt))
        points.append(rotated_point)
        curr_pt.pt = rotated_point.pt 

    points.append(start_pt)

    return points

# Given 3 non-collinear points on a plane, generates a normal vector for the plane 
def normal_vector(pt1, pt2, pt3):
    # Generate 2 vectors on the plane
    v1 = pt3 - pt1
    v2 = pt2 - pt1

    normal = np.cross(v1, v2)

    return normal

# Given a bottom and top ring of points, returns a list of facets for the planes created by 
# Drawing straight between corresponding points in both rings
def generate_fcts(bottom_ring, top_ring, num_sides):
    facets = []
    
    for i in range(num_sides):
        top_left = top_ring[i].pt
        top_right = top_ring[i + 1].pt
        btm_left = bottom_ring[i].pt
        btm_right = bottom_ring[i + 1].pt

        # Calculate normal
        normal = normal_vector(top_left, top_right, btm_left)

        facet1 = Facet(btm_right, top_right, top_left, normal)
        facet2 = Facet(top_left, btm_left, btm_right, normal)
        facets.append(facet1)
        facets.append(facet2)

    return facets

# Generates the 'pizza' facets that form the base
def generate_base_fcts(bottom_ring, num_sides):
    base_fcts = []
    
    left_pt = None
    right_pt = None
    null_pt = np.array([0, 0, 0]) # All facets here will include zero point
    normal = np.array([0, 0, 1]) # Normal vector to base x/y plane
    for i in range(num_sides):
        left_pt = bottom_ring[i].pt
        right_pt = bottom_ring[i + 1].pt
        facet = Facet(null_pt, right_pt, left_pt, normal)
        base_fcts.append(facet)

    return base_fcts

def main():
    print("Welcome to the Parametric Vase Generator!")
    print("To generate your perfect vase, we will need to take 7 parameters -- 4 radii, and 3 heights.")
    
    # All parameters are labelled from base to mouth
    h1 = None
    h2 = None
    h3 = None

    h1 = float(input("Enter the height of the bottom plane of the belly (h1): "))
    while h1 <= 0:
        print("Please input a valid height over 0.")
        h1 = float(input("Enter the height of the bottom plane of the belly (h1): "))

    h2 = float(input("Enter the height of the top plane of the belly (h2): "))
    while h2 <= 0:
        print("Please input a valid height over 0.")
        h2 = float(input("Enter the height of the top plane of the belly (h2): "))
    h2 = h2 + h1

    h3 = float(input("Enter the height of the neck (h3): "))
    while h3 <= 0:
        print("Please input a valid height over 0.")
        h3 = float(input("Enter the height of the neck (h3): "))
    h3 = h3 + h2
    
    base_r  = float(input("Enter the radius of the base (r1): "))
    belly_r = float(input("Enter the radius of the belly (r2): "))
    neck_r  = float(input("Enter the radius of the neck (r3): "))
    mouth_r = float(input("Enter the radius of the mouth (r4): "))

    while (neck_r >= belly_r) and (neck_r >= mouth_r):
        print("To preserve the 'S' shape, please ensure the neck and base radii are both LESS THAN the belly AND neck. ")
        base_r  = float(input("Enter the radius of the base (r1): "))
        belly_r = float(input("Enter the radius of the belly (r2): "))
        neck_r  = float(input("Enter the radius of the neck (r3): "))
        mouth_r = float(input("Enter the radius of the mouth (r4): "))

    num_sides = None
    while num_sides is None or (num_sides is not None and (num_sides < 8 or num_sides > 128)):
        num_sides = int(input("Please choose a number of sides for the base of the vase between 8 and 128: "))

    # Generate the circular points
    base_pts = generate_pts(base_r, 0, num_sides)
    belly_pts = generate_pts(belly_r, h1, num_sides)
    neck_pts = generate_pts(neck_r, h2, num_sides)
    mouth_pts = generate_pts(mouth_r, h3, num_sides)
    
    base_fcts = generate_base_fcts(base_pts, num_sides)
    low_fcts = generate_fcts(base_pts, belly_pts, num_sides)
    mid_fcts = generate_fcts(belly_pts, neck_pts, num_sides)
    top_fcts = generate_fcts(neck_pts, mouth_pts, num_sides)

    vase = Vase(base_fcts, low_fcts, mid_fcts, top_fcts)

    write_stl(vase)

if __name__ == "__main__":
    main()