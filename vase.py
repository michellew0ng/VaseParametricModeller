# Michelle Wong PRA1817277 on 24th April
# This program generates an ASCII STL file for a simple vase ith several user given parameters for height and radius

import math
import numpy as np 

def write_stl(filename):
    # Name of file is vase
    header = 'solid vase\n'

    # Define the normal and vertices for one triangle
    normal = (0.0, 0.0, 1.0)
    vertex1 = (0.0, 0.0, 0.0)
    vertex2 = (1.0, 0.0, 0.0)
    vertex3 = (0.0, 1.0, 0.0)

    # Create the facet
    facet = f'''
    facet normal {normal[0]} {normal[1]} {normal[2]}
        outer loop
            vertex {vertex1[0]} {vertex1[1]} {vertex1[2]}
            vertex {vertex2[0]} {vertex2[1]} {vertex2[2]}
            vertex {vertex3[0]} {vertex3[1]} {vertex3[2]}
        endloop
    endfacet
    '''

    # Footer to end the solid
    footer = 'endsolid'

    # Combine all parts into one STL string
    stl_string = f"{header}{facet}{footer}"

    # Write the STL string to file
    with open(filename, 'w') as file:
        file.write(stl_string)

    print(f"Your finished vase is written in STL file '{filename}'.")

# Generates points in a radius given additional parameters the height from base and number of sides
def generate_points(radius, height, sides):

    pass

def main():
    print("Welcome to the Parametric Vase Generator!")
    print("To generate your perfect vase, we will need to take 6 parameters -- 4 radii, and 3 heights.")
    
    # All parameters are labelled from base to mouth
    h1 = float(input("Enter the height of the bottom plane of the belly (h1): "))
    h2 = float(input("Enter the height of the top plane of the belly (h2): "))
    h1 = float(input("Enter the height of the neck (h3): "))
    
    r1 = float(input("Enter the radius of the base (r1): "))
    r2 = float(input("Enter the radius of the belly (r2): "))
    r2 = float(input("Enter the radius of the neck (r3): "))
    r3 = float(input("Enter the radius of the mouth (r4): "))

    num_sides = None
    while num_sides is None or (num_sides is not None and (num_sides < 8 or num_sides > 64)):
        num_sides = float(input("Choose a number of sides for the base of the vase between 8 and 64: "))

    angle = np.radians(360/num_sides) # The angle of difference between each vertice 

    # circular points around the 4 radii
    mouth_pts = 
    neck_pts = 
    belly_pts = 
    base_pts = 

    filename = "vase.stl"
    write_stl(filename)

if __name__ == "__main__":
    main()