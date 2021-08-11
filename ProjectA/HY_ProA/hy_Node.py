def get_plane_num(line):
    pl_num =  line.split(':')[0:1]
    pl_num = pl_num[0].split('_')[2:3][0]
    pl_num = pl_num.replace(" ","")
    return pl_num

# represent a line in the STN data table
class hy_Node:
    def __init__(self, action, pl_num, time):
        self.action = action
        self.pl_num = pl_num
        self.id = action + pl_num
        self.time = time
        self.parents = {}
        self.childs = {}
        
    def __str__(self):
        return self.action +" " + self.pl_num
    
    def add_parent(self, parent_id, parent):
        self.parents[parent_id] = parent
        
    def add_child(self, child_id, child):
        self.childs[child_id] = child
    
    def get_parents(self):
        return self.parents.values()
    
    def get_childs(self):
        return self.childs.values()
    
    def get_id(self):
        return self.id

# represent the data structure of an STN as a graph   
class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vert = 0
       
        log = open('log_output.txt', 'r')
        
        # read the stn table line by line and create a new node with the corrospandin data
        for line in log:
        # get the action + plane number + start time from log file
           action = line.split('_')[1:2][0] 
           pl_num = get_plane_num(line)
           id = action + pl_num
           s_time = line.split(':')[1:2][0].strip()
           
        # create a new node and add it to the dict
        # key = action+pl_num   value = class hy_node object
           self.num_vert +=1
           new_vertex = hy_Node(action, pl_num, s_time)
           self.vert_dict[id] = new_vertex
           
        log.close()   
    
        log = open('log_output.txt', 'r')
        
        # convert the parent list to a dict and insert it to the relavent node
        for line in log:
        # get the current node id
           action = line.split('_')[1:2][0] 
           pl_num = get_plane_num(line)
           id = action + pl_num
        
        # get the parent list from the stn
           parents = line.split(':')[3:4][0].replace(" ","")
           parents_list = list(parents.replace("[","").replace("]","").split(","))
           parents = [p[3:-1].replace("_","") for p in parents_list]
        
        # set the node parent dict with key = parent_id, value = parent node for each of the parents in the parntes list    
           for pr in parents:
               if pr == "":
                   continue
               self.vert_dict[id].add_parent(pr, self.vert_dict[pr])
           
        log.close()
        
        log = open('log_output.txt', 'r')
        
        # convert the child list to a dict and insert it to the relavent node
        for line in log:
        # get the current node id
           action = line.split('_')[1:2][0] 
           pl_num = get_plane_num(line)
           id = action + pl_num
        
        # get the childs list
           childs =  line.split(':')[5:6][0].replace("\n","").replace(" ","")
           childs_list = list(childs.replace("[","").replace("]","").split(","))
           childs = [p[3:-1].replace("_","") for p in childs_list]
           
        # set the node childs dict with key = child_id, value = child node for each of the child in the parntes list    
           for ch in childs:
               if ch == "":
                   continue
               self.vert_dict[id].add_child(ch, self.vert_dict[ch])
           
        log.close()
        
    def __iter__(self):
        return iter(self.vert_dict.values()) 
    
    def get_vertices(self):
        return self.vert_dict.keys()
    
          
g = Graph()

for v in g:
    print("node {} -".format(v.get_id()))
    print("parents: ", end ="")
    for w in v.get_parents():
        print ("{},".format(w.get_id()), end ="")
    print("")
    print("childs: ", end ="")
    for w in v.get_childs():
        print ("{},".format(w.get_id()), end ="")
    print("")
    print("")
