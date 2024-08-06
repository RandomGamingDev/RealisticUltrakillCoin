import bpy

# Function to create a line with a given thickness and color
def create_line(start, end):
    # Create a new mesh
    mesh = bpy.data.meshes.new("LineMesh")
    obj = bpy.data.objects.new("Line", mesh)
    
    # Set mesh vertices and edges
    vertices = [start, end]
    edges = [(0, 1)]
    mesh.from_pydata(vertices, edges, [])

    bpy.context.collection.objects.link(obj)
    mesh.update()

# Create the line
create_line((0, 0, 0), (2, 2, 2))