# We will need a tree datastructure
# so i will first make a node class
class Node(object):
    # init the node
    def __init__(self, nodeName=None, parentNode=None) -> None:
        self.nodeName = nodeName
        self.parentNode = parentNode
        self.subNodes = []
        self.content = []
    
    def get_size(self):
        self.size = 0
        for item in self.content:
            self.size += item['size']
        
        # add size of subNodes
        for subNode in self.subNodes:
            self.size += subNode.get_size()
        
        return self.size


# ------------------------------------------------------------
# import input and put queries and responses into nicer format
# ------------------------------------------------------------

with open("input.dat", "r") as file:
    lines = [line.strip() for line in file.readlines()]

commands = []
query = None
response = []
for line in lines:
    # if new command save previous and make new command
    if line[0] == "$":

        # for initial iteration
        if query != None:
            commands.append({'query': query, 'response':response})

        # split query to command and args ('$ cd a' -> ['cd', 'a'])
        query = line.strip("$ ").split(" ")
        response = []
        continue

    # if not new query then must be response
    response.append(line.split(" "))
commands.append({'query': query, 'response':response})



# ---------------------------------------
# Build the tree structure from the input
# ---------------------------------------

# define root node
root = Node("/")
list_of_folders = [root]
current_folder = root

# loop over all commands
for command in commands[1:]:
    # if query is "ls"
    if command['query'][0] == 'ls':
        sub_folders = []
        files = []
        for response in command['response']:
            # if dir, then definitely a new directory (input does not show same ls response twice)
            if response[0] == 'dir':
                new_folder = Node(nodeName=response[1], parentNode=current_folder)
                sub_folders.append(new_folder)
                list_of_folders.append(new_folder)
                continue

            # else just files. Save in dict with name and size
            files.append({'filename':response[1], 'size':int(response[0])})

        # save subfolders and files into node
        current_folder.subNodes = sub_folders
        current_folder.content = files
        continue

    # else if query is "cd .."
    if command['query'][1] == '..':
        current_folder = current_folder.parentNode
        continue

    # else if query is "cd *"
    # search subnodes till the one with the right name is found
    for sub_folder in current_folder.subNodes:
        if sub_folder.nodeName == command['query'][1]:
            current_folder = sub_folder

# run get_size() on root folder to initialise self.size for all folder
root.get_size()

# ------
# PART 1
# ------
part1 = 0
for f in list_of_folders:
    size = f.size
    if size <= 100000:
        part1 += size

print(part1)

# ------
# PART 2
# ------
total_space = 70000000
needed_space = 30000000
occupied_space = root.size

list_of_possible_delete_sizes = []
for f in list_of_folders:
    if total_space - occupied_space + f.size >= needed_space:
        list_of_possible_delete_sizes.append(f.get_size())

print(sorted(list_of_possible_delete_sizes)[0])