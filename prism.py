import numpy as np

class Vertex:
    def __init__(self, label, coordinates):
        self.label = label # number, 0 indexed
        self.coordinates = coordinates

class Edge:
    def __init__(self, start_vertex, end_vertex):
        self.start_vertex = start_vertex
        self.end_vertex = end_vertex


# Generates points in a radius given additional parameters the height from base and number of sides
# The first point will appear at the start and the end in a circular fashion, ie. [pt1, pt2, pt3, .... pt1]
def generate_pts(radius, height, num_sides, is_top):
    points = []

    angle = np.radians(360/num_sides) # The angle of difference between each vertice 

    # Define the transformation matrix to rotate angle_of_diff around the z axis
    # Note that this is anti clockwise rotation
    rotation_matrix = np.array([[np.cos(angle), -1 * np.sin(angle), 0],
                [np.sin(angle), np.cos(angle), 0],
                [0, 0, 1]])
    
    # Start on the x axis (potentially elevated)
    start_pt = Vertex(0 if not is_top else num_sides, np.array([0, radius, height]))
    curr_pt = start_pt
    points.append(start_pt)

    for i in range(1, num_sides):
        label = i if not is_top else num_sides + i

        rotated_point = np.dot(rotation_matrix, curr_pt.coordinates)
        new_vertex = Vertex(label, rotated_point)
        points.append(new_vertex)
        curr_pt = new_vertex

    points.append(start_pt)

    return points

def generate_vertical_edges(base_pts, top_pts, num_sides):
    vert_edges = []
    for i in range(num_sides):
        new_edge = Edge(base_pts[i], top_pts[i])
        vert_edges.append(new_edge)
    return vert_edges

def generate_horizontal_edges(pts, num_sides):
    horz_edges = []
    for i in range(num_sides):
        new_edge = Edge(pts[i], pts[i+1])
        horz_edges.append(new_edge)
    return horz_edges


def main():
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

    base_pts = generate_pts(r, 0, n, False)
    top_pts = generate_pts(r, h, n, True)
    vertexes = base_pts[:-1] + top_pts[:-1]

    horz_edges_base = generate_horizontal_edges(base_pts, n)
    horz_edges_top = generate_horizontal_edges(top_pts, n)
    vert_edges = generate_vertical_edges(base_pts, top_pts, n)

    edges = horz_edges_base + horz_edges_top + vert_edges

    print('')
    print('VERTEX LIST')
    print_index = 1
    for vertex in vertexes:
        coords = " ".join(f"{coord:.2f}" for coord in vertex.coordinates)
        print(f"{vertex.label} = [{coords}]") 
        print_index += 1

    print('')
    print('EDGE LIST')
    print_index = 1
    for edge in edges:
        print(f"Edge {print_index:2} = {(edge.start_vertex.label, edge.end_vertex.label)}") 
        print_index += 1

if __name__ == "__main__":
    main()