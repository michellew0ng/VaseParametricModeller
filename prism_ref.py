import numpy as np

class Vertex:
    def __init__(self, label, coordinates):
        self.label = label
        self.coordinates = coordinates

class Edge:
    def __init__(self, start_vertex, end_vertex):
        self.start_vertex = start_vertex
        self.end_vertex = end_vertex


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
    start_pt = np.array([0, radius, height]) 
    curr_pt = start_pt
    points.append(start_pt)
    # Note: -1 because the start point has already been appended
    for i in range(num_sides):
        rotated_point = np.dot(rotation_matrix, curr_pt.pt)
        points.append(rotated_point)
        curr_pt.pt = rotated_point.pt 

    points.append(start_pt)

    return points

def main():
    vertexes = []
    edges = []

    x_in, y_in, z_in = input("Enter point of reference p, in form (x,y,z): ").split()
    x_in = int(x_in)
    y_in = int(y_in)
    z_in = int(z_in)

    print('Enter the radius of your prism, r:')
    r = int(input())

    print('Enter the height of your prism, h:')
    h = int(input())

    print('Enter the number of sides of your prism, n:')
    n = int(input())

    base_pts = generate_pts(r, 0, n)
    top_pts = generate_pts(r, h, n)

    while count < (n - 1) * 2:
        # Generating the vertex for the base
        vector = np.dot(M, vector)
        coordinates = tuple(vector.ravel())
        vertex_base = Vertex(f"Vertex {count + 3}", coordinates)
        vertexes.append(vertex_base)

        if first_vertex_base is None:
            first_vertex_base = vertex_base
  
        # create an edge between base vertexes
        edge = Edge(vertex_base, prev_vertex_base)
        edges.append(edge)
        prev_vertex_base = vertex_base

        # Generate the vertex for the top
        upper = (coordinates[0], coordinates[1], coordinates[2]+h)
        vertex_upper = Vertex(f"Vertex {count + 4}", upper)
        vertexes.append(vertex_upper)

        # create an edge between upper vertexes
        edge = Edge(vertex_upper, prev_vertex_upper)
        edges.append(edge)
        prev_vertex_upper = vertex_upper

        if first_vertex_upper is None:
            first_vertex_upper = vertex_upper

        # Create an edge from lower to the upper
        vertical_edge = Edge(vertex_base, vertex_upper)
        edges.append(vertical_edge)
        

        count += 2

    # Finish the 'circle'
    edges.append(Edge(first_vertex_base, vertex_base))
    edges.append(Edge(first_vertex_upper, vertex_upper))


    print('')
    print('VERTEX LIST')
    print_index = 1
    for vertex in vertexes:
        print(f"{vertex.label} = {vertex.coordinates}") 
        print_index += 1

    print('')
    print('EDGE LIST')
    print_index = 1
    for edge in edges:
        print(f"Edge {print_index:2} = {(edge.start_vertex.label, edge.end_vertex.label)}") 
        print_index += 1

if __name__ == "__main__":
    main()