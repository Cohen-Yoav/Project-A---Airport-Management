class config_line():
    def __init__(self, cfg_line):
        self.lst = cfg_line
        # single digit id plane number - TODO H&Y fix it
        self.id = cfg_line[0][-1]
        self.start_day_min = cfg_line[1]
        self.start_day_max = cfg_line[2]
        self.mission_duration = cfg_line[3]
        self.max_fuel = cfg_line[4]
        self.end_day = cfg_line[5]
        self.status = cfg_line[6]
        
        
class config_file():
    def __init__(self, path, permission):
        self.file = open(path, permission)
        self.num_of_planes = 0
        self.num_of_lanes = 0
        self.max_run_time = 0
        self.config_line_lst = []
        
        if permission == 'r':
            self.set_config_file(path, permission)
        else:
            pass
        
        self.file.close()
    
    def set_config_file(self, path, permission):
        config_lines = {}
        count = 0
        for line in self.file:
            # each line in the config file is:
            # 1. striped from all extra white spaces 
            # 2. stripped from all commenets
            # 3. striped from endofline space
            # 4. split into a list
            
            config_lines[count] = " ".join(line.split()).split('#')[0].strip().split(" ")[:7]
            count += 1
        
        self.num_of_planes = config_lines[0][2]
        self.num_of_lanes = config_lines[1][2]
        self.max_run_time = config_lines[2][2]
        
        for i in range (3, count):
            self.config_line_lst.append(config_line(config_lines[i]))

if __name__ == "__main__":
    config = config_file('ProjectA/BT_ProA/configs/config0.txt', 'r')
    new_config = config_file('ProjectA/BT_ProA/configs/config1.txt', 'w')