class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

class Graph:

    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):

        # create a new entry only if it doesn't exist yet
        if vertex_id not in self.vertices:

            self.vertices[vertex_id] = dict()
            self.vertices[vertex_id]["n"] = None
            self.vertices[vertex_id]["s"] = None
            self.vertices[vertex_id]["e"] = None
            self.vertices[vertex_id]["w"] = None

    def add_edge(self, vertex1_id, vertex2_id, direction):

        # add v2 if it doesn't exist yet
        if vertex2_id not in self.vertices:
            self.add_vertex(vertex2_id)

        # create an edge going from vertex1_id to vertex2_id
        self.vertices[vertex1_id][direction] = vertex2_id

        # store the edge going from vertex2_id to vertex1_id using the opposite direction
        reverse_direction = opposite_directions[direction]
        self.vertices[vertex2_id][reverse_direction] = vertex1_id
        
    def get_neighbors(self, vertex_id):
        return self.vertices[vertex_id]

    # use breadth-first search to return a list of nodes to traverse to travel between two vertices
    # starting_vertex and destination_vertex are purposely left out of the list
    def find_shortest_sequence_of_nodes_between(self, starting_vertex, destination_vertex):

        # create a queue to hold vertices to traverse
        vertices_to_visit = Queue()

        # initialize queue with starting vertex
        vertices_to_visit.enqueue(starting_vertex)

        # use a dictionary to keep track of visited vertices and their path from the starting node
        paths_to_vertices = dict()
        paths_to_vertices[starting_vertex] = []

        # use a set to keep track of visited vertices
        vertices_already_visited = set()

        while vertices_to_visit.size() > 0:

            # get next vertex in line
            current_vertex = vertices_to_visit.dequeue()

            # process current vertex if it hasn't been visited yet
            if current_vertex not in vertices_already_visited:

                # mark current vertex as visited and store its path at the same time
                vertices_already_visited.add(current_vertex)

                # inspect all the neighbors of the current vertex
                # neighbor_data = [neighbor for neighbor in self.get_neighbors(current_vertex) if neighbor is not None]
                neighbor_data = self.get_neighbors(current_vertex)

                for direction in neighbor_data:

                    neighbor = neighbor_data[direction]

                    # there are entries for all four directions, even if the neighbor doesn't exist
                    # skip those neighbors if they don't exist
                    if neighbor is not None:

                        # if the target vertex is one of the neighbors, the search is done
                        # right now paths_to_vertices[current_vertex] only contains all the vertices up to and including the parent vertex
                        # to return the full path, add both the current vertex and the target vertex first.
                        if neighbor == destination_vertex:
                            final_path = paths_to_vertices[current_vertex][:]
                            final_path.append(current_vertex)
                            final_path.append(neighbor)
                            return final_path[1:-1]

                        # add all the other neighbors to the queue
                        vertices_to_visit.enqueue(neighbor)

                        # store a copy of the current path for each of the neighbors
                        # take the path leading to current_vertex and add current_vertex to it
                        # make a copy in order to not modify the original
                        copy_of_path_to_parent = paths_to_vertices[current_vertex][:]
                        copy_of_path_to_parent.append(current_vertex)

                        # store path in dictionary
                        paths_to_vertices[neighbor] = copy_of_path_to_parent
        
        # target not found
        print("Vertex", destination_vertex, "was not found.")
        return

# use a dictionary to look up opposite directions (used for backtracking)
opposite_directions = dict()
opposite_directions["n"] = "s"
opposite_directions["s"] = "n"
opposite_directions["e"] = "w"
opposite_directions["w"] = "e"

def traverse_maze(player):
    
    # use a graph to store visited rooms and their neighbors
    maze = Graph()

    # keep track of room numbers at each step
    # this will later be converted to a sequence of movements
    traversal_path = []

    # keep track of rooms already visited
    # each entry in rooms_to_visit will be a Room object
    visited_rooms = dict()
    rooms_to_visit = Stack()

    # add current room to rooms to visit
    new_room = player.current_room
    rooms_to_visit.push(new_room)

    # keep track of previous room in order to know when to backtrack
    previous_room = None

    while rooms_to_visit.size() > 0:

        # visit next room in stack
        new_room = rooms_to_visit.pop()

        # visit room only if this room has not been visited before
        if new_room.id not in visited_rooms:

            # check to see if the new room is directly accessible from the previous room
            # only do so if this is not the starting room
            if previous_room is not None:

                is_valid_direct_connection = False
                exit_to_use = None

                # examine all exits from the previous room for one that will lead to the new room
                for exit_direction in previous_room.get_exits():

                    adjoining_room = previous_room.get_room_in_direction(exit_direction)

                    if adjoining_room.id == new_room.id:
                        is_valid_direct_connection = True
                        exit_to_use = exit_direction
                
                # the new room is not directly reachable; need to search for a path to the target room
                if not is_valid_direct_connection:

                    # use breadth-first search to find a route (which may involve backtracking if at a dead end, or moving forward at the end of a loop)
                    path_between_rooms = maze.find_shortest_sequence_of_nodes_between(previous_room.id, new_room.id)
                    
                    # add that route to traversal_path
                    traversal_path = traversal_path + path_between_rooms                      

            # add room to dictionary
            visited_rooms[new_room.id] = new_room

            # add room to graph
            maze.add_vertex(new_room.id)

            # add room to traversal path
            traversal_path.append(new_room.id)

            # get any neighbors to the room to add them to the graph
            for exit_direction in new_room.get_exits():

                # get neighboring room
                adjoining_room = new_room.get_room_in_direction(exit_direction)

                # add a vertex from the current room to the neighboring room
                maze.add_edge(new_room.id, adjoining_room.id, exit_direction)
                
                # push all neighbors onto the stack to visit later
                rooms_to_visit.push(adjoining_room)

            # update previous room
            previous_room = new_room
    
    # convert traversal_path to a sequence of directions
    traversal_directions = []

    for i in range(0, len(traversal_path) - 1):

        previous_room = traversal_path[i]
        current_room = traversal_path[i + 1]

        neighbor_data = maze.get_neighbors(previous_room)

        for direction in neighbor_data:

            if neighbor_data[direction] == current_room:
                traversal_directions.append(direction)
        
    print(traversal_path)
    print(traversal_directions)
    print("done")

    # refine solution now that all rooms have been traversed and had their data recorded

    # store each room that has a branch into a dead end
    # value will be a list of lists representing paths to traverse each dead end entirely, beginning with the square after the square in the key
    dead_ends = dict()

    # store the reverse relationship: dead end rooms to start rooms
    # key will be any room that belongs to a dead end
    # value will be the starting room that each room in a dead end belongs to
    dead_end_start_rooms = dict()

    # find rooms with only a single neighbor (end of a dead-end passage)
    for room in visited_rooms:

        # count the neighbors in this room
        neighbor_data = maze.get_neighbors(room)
        actual_neighbors = []

        for direction in neighbor_data:
            neighbor = neighbor_data[direction]

            # skip neighbors that do not exist
            if neighbor is not None:
                actual_neighbors.append(neighbor)
        
        path_from_dead_end = []

        # keep track of rooms in this dead end
        while len(actual_neighbors) == 1:
            # print(prev_room, "has only one neighbor,", actual_neighbors)

            prev_room = room
            # set the current room to the only exit out of this room
            # (or only other exit out of this room)
            room = actual_neighbors[0]

            # count the neighbors in this room
            neighbor_data = maze.get_neighbors(room)
            actual_neighbors = []

            for direction in neighbor_data:
                neighbor = neighbor_data[direction]

                # skip neighbors that do not exist
                if neighbor is not None and neighbor != prev_room:
                    actual_neighbors.append(neighbor)
            
            path_from_dead_end.append(prev_room)

        # associate each room in the dead end with the start of the dead end
        # this will be used later to consolidate multiple dead end passages
        # "room" is the room right before the dead end

        for dead_end_room in path_from_dead_end:
            dead_end_start_rooms[dead_end_room] = room

        # store the sequence of rooms needed to traverse the dead end
        if len(path_from_dead_end) > 0:
            
            # calculate the path back to the fork. Exclude the dead-end room
            path_to_dead_end = path_from_dead_end[1:]
            path_to_dead_end.reverse()
            
            # store in the dictionary with the key as the room that forks (that leads to the dead end)
            # there is a possibility that a room will fork to multiple dead ends. Resolve this later.
            if room in dead_ends:
                dead_ends[room].append(path_to_dead_end + path_from_dead_end)
            else:
                dead_ends[room] = [path_to_dead_end + path_from_dead_end]
        
    # print("Total dead ends:", len(dead_ends))
    # for starting_room in dead_ends:
    #     print(starting_room, dead_ends[starting_room])

    # consolidate dead ends that branch off of other dead ends
    for starting_room in dead_ends:

        passages = dead_ends[starting_room]

        # only dead ends longer than a single room can branch
        if len(passages) > 1:

            print(starting_room, dead_ends[starting_room])

    print(len(dead_end_start_rooms), "rooms belong to a dead end passage.")
    print(dead_end_start_rooms)

    return (traversal_path, traversal_directions)
