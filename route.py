#!/usr/local/bin/python3
# route.py : Road Trip!
#
# Code by: [Sri Harsha Manjunath - srmanj; Vijaylakshmi Maigur - vbmaigur; Disha talreja - dtalreja]
#
#
#
# put your routing program here!

import numpy as np
from queue import PriorityQueue

#Dealing with new keys in a dictionary
def new_key(default_type):
    class NewKey(dict):
        def __getitem__(self, key):
            if key not in self:
                dict.__setitem__(self, key, default_type())
            return dict.__getitem__(self, key)
    return NewKey()

def create_map():
    #Create a new dict to store all paths
    roads = new_key(list)
    for line in road_segments:
        everything = line.split(" ")

        city_a = everything[0].strip(); city_a.replace("\"","")
        city_b = everything[1].strip(); city_b.replace("\"","")
        dist = everything[2].strip()
        speed = everything[3].strip()
        time = int(dist)/int(speed)
        mpg = 400*(int(speed)/150) * (1-(int(speed)/150))**4 #QC Please
        h_name = everything[4].strip()

        #Creating the dictionary
        roads[city_a].append(city_b+"~"+dist+"~"+speed+"~"+h_name+"~"+str(np.round(time,3))+"~"+str(np.round(mpg,3)))
        roads[city_b].append(city_a+"~"+dist+"~"+speed+"~"+h_name+"~"+str(np.round(time,3))+"~"+str(np.round(mpg,3)))
        #This ensures that all streets are entered as a 2 way streets

def successor(city):
    ret_list = []
    for c in roads[city]:
        c = c.split("~")
        ret_list.append((1,c[1],c[4],np.round(float(c[1])/float(c[5]),2),c[5],c[0]))
    return ret_list

def solve(start_city,end_city,metric):
    visited = []
    fringe = PriorityQueue()
    fringe.put((0,0,0,0,0,0,"",start_city)) #[Priority][total-segments][total-miles][total-hours][total-gas-gallons][cities][cur-city]

    if metric == 'distance': #Return the least distant neighbor
        while not fringe.empty():
            (priority, tot_seg, tot_mil, tot_hor, tot_gal,tot_mpg, all_cit, cur_cit) = fringe.get()
            tmp = 0 #The priority variable

            for (seg, mil, hor, gal, mpg, city) in successor(cur_cit):
                #Check 1: If Successor is the goal
                if cur_cit == end_city:
                    return(tot_seg,tot_mil,tot_hor,tot_gal,str(all_cit)+str('[')+str(cur_cit)+str(']'))
                if city not in visited:
                    tmp = float(tot_mil) + float(mil)
                    fringe.put((tmp,float(tot_seg) + float(seg), float(tot_mil) + float(mil), float(tot_hor) + float(hor),\
                            float(tot_gal) + float(gal), float(tot_mpg) + float(mpg), str(all_cit)+str('[')+str(cur_cit)+str(']'), city))
                    visited.append(city)

    elif metric == 'time': #Return the least time consuming neighbor
        while not fringe.empty():
            (priority, tot_seg, tot_mil, tot_hor, tot_gal,tot_mpg, all_cit, cur_cit) = fringe.get()
            tmp = 0 #The priority variable

            for (seg, mil, hor, gal, mpg, city) in successor(cur_cit):
                #Check 1: If Successor is the goal
                if cur_cit == end_city:
                    return(tot_seg,tot_mil,tot_hor,tot_gal,str(all_cit)+str('[')+str(cur_cit)+str(']'))
                if city not in visited:
                    tmp = float(tot_hor) + float(hor)
                    fringe.put((tmp,float(tot_seg) + float(seg), float(tot_mil) + float(mil), float(tot_hor) + float(hor),\
                            float(tot_gal) + float(gal), float(tot_mpg) + float(mpg), str(all_cit)+str('[')+str(cur_cit)+str(']'), city))
                    visited.append(city)

    elif metric == 'mpg': #Return the cheapest neighbor in terms of mpg
        while not fringe.empty():
            (priority, tot_seg, tot_mil, tot_hor, tot_gal,tot_mpg, all_cit, cur_cit) = fringe.get()
            tmp = 0 #The priority variable

            for (seg, mil, hor, gal, mpg, city) in successor(cur_cit):
                #Check 1: If Successor is the goal
                if cur_cit == end_city:
                    return(tot_seg,tot_mil,tot_hor,tot_gal,str(all_cit)+str('[')+str(cur_cit)+str(']'))
                if city not in visited:
                    tmp = float(tot_mpg) + float(mpg)
                    fringe.put((tmp,float(tot_seg) + float(seg), float(tot_mil) + float(mil), float(tot_hor) + float(hor),\
                        float(tot_gal) + float(gal), float(tot_mpg) + float(mpg), str(all_cit)+str('[')+str(cur_cit)+str(']'), city))
                    visited.append(city)

    else:#Return the least distant neighbor in terms of segments
        while not fringe.empty():
            (priority, tot_seg, tot_mil, tot_hor, tot_gal,tot_mpg, all_cit, cur_cit) = fringe.get()
            tmp = 0 #The priority variable

            for (seg, mil, hor, gal, mpg, city) in successor(cur_cit):
                #Check 1: If Successor is the goal
                if cur_cit == end_city:
                    return(tot_seg,tot_mil,tot_hor,tot_gal,str(all_cit)+str('[')+str(cur_cit)+str(']'))

                if city not in visited:
                    tmp = float(tot_seg) + float(seg)
                    fringe.put((tmp,float(tot_seg) + float(seg), float(tot_mil) + float(mil), float(tot_hor) + float(hor),\
                            float(tot_gal) + float(gal), float(tot_mpg) + float(mpg), str(all_cit)+str('[')+str(cur_cit)+str(']'), city))
                    visited.append(city)
    return False

result = solve(start_city,end_city,'mpg')
print(int(result[0]), int(result[1]), result[2], result[3],result[4].replace('[','').replace(']',' '))


if __name__ == "__main__":

    if(len(sys.argv) != 4):
        raise Exception('Error: expected 3 command line arguments')
        #Data Preprocessing -
        filename = 'road-segments.txt'
        road_segments = open(filename,"r")

        result = solve(sys.argv[1],sys.argv[2],sys.argv[3])
        print(int(result[0]), int(result[1]), result[2], result[3],result[4].replace('[','').replace(']',' '))
