# Michelle Wong PRA1817277 on 24th April
# This program generates an ASCII STL file for a simple vase ith several user given parameters for height and radius

import math

def write_stl(filename):
    # Define the header for the STL file
    header = 'solid ascii\n'

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

    print(f"STL file '{filename}' has been written.")

# Usage
filename = "example.stl"
write_stl(filename)

def main():
    print("Welcome to the Parametric Vase Generator!")
    print("To generate your perfect vase, we will need to take 6 parameters -- 3 radii, and 3 heights.")
    h1 = float(input("Enter the height of the neck (h1): "))
    h2 = float(input("Enter the height of the top plane of the belly (h2): "))
    h3 = float(input("Enter the height of the bottom plane of the belly (h3): "))
    r1 = float(input("Enter the radius of the mouth (r1): "))
    r2 = float(input("Enter the radius of the belly (r2): "))
    r3 = float(input("Enter the radius of the base (r3): "))

    filename = "vase.stl"
    write_stl(filename)
    print("Your finished vase is in vase.stl!")

if __name__ == "__main__":
    main()