from ast import literal_eval

maps = ["test_line", "test_cross", "test_loop", "test_loop_fork", "main_maze"]
# maps = ["test_line"]

# create first part of HTML document
def make_html_header(map):

    html = '<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    html += '    <title>' + map + '</title>\n'
    html += '    <link rel="stylesheet" href="maze.css" />\n'
    html += '</head>\n<body>\n'
    html += '    <h1>' + map + '</h1>\n    <table>\n'

    return html

# create final part of HTML document
def make_html_footer():

    html = '    </table>\n</body>\n</html>'

    return html

# create HTML version of map
for map in maps:
    map_file = "maps/" + map + ".txt"

    # evaluate contents of text file as a Python dictionary of rooms
    room_graph = literal_eval(open(map_file, "r").read())

    # determine dimensions of grid
    largest_row = 0
    largest_col = 0

    for room_ID in room_graph:
        room_data = room_graph[room_ID]

        # tuple represents (x, y) coordinates
        room_col, room_row = room_data[0]

        if room_row > largest_row:
            largest_row = room_row
        
        if room_col > largest_col:
            largest_col = room_col

    # create an array to hold the map
    maze = []
    
    for row_ID in range(0, largest_row + 1):
        
        row = [[]] * (largest_col + 1)
        maze.append(row)
        
    # add all relevant room data to maze
    # each entry in the grid will contain the ID and exits of the room
    for room_ID in room_graph:
        room_data = room_graph[room_ID]

        # tuple represents (x, y) coordinates
        room_col, room_row = room_data[0]

        exits = []

        if "n" in room_data[1]:
            exits.append("n")
        if "s" in room_data[1]:
            exits.append("s")
        if "e" in room_data[1]:
            exits.append("e")
        if "w" in room_data[1]:
            exits.append("w")

        maze[room_row][room_col] = {"id": room_ID, "exits": exits}

    with open("maps/" + map + ".html", "w") as html:

        html.write(make_html_header(map))

        # add data for each room
        for row_ID in range(len(maze) - 1, -1, -1):
            
            row = maze[row_ID]

            html.write('        <tr>\n            <th>' + str(row_ID) +'</th>\n')

            for col_ID in range(len(maze[0])):

                room_data = row[col_ID]

                # if there is data in the room, add it
                if len(room_data) > 0:

                    room_ID = room_data["id"]
                    exits = " ".join(room_data["exits"])

                    html.write('            <td class="room ' + exits + '">')
                    html.write(str(room_ID))
                    html.write("</td>\n")

                else:
                    html.write("            <td></td>\n")

            html.write('        </tr>\n')
        
        # add a bottom row for column IDs
        html.write('        <tr>\n            <td></td>\n')
        
        for col_ID in range(len(maze[0])):
            html.write('            <th>' + str(col_ID) +'</th>\n')
        
        html.write('        </tr>\n')

        html.write(make_html_footer())
        
        print("Created " + map + ".html")