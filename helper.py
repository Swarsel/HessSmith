import numpy as np

def index(list: list, element: int) -> float:
    # allows to use normal list as a closed loop, connecting the last and first elements
    return list[element % len(list)]

def parsecoords(filename: str) -> list:
    # reads coordinates from file
    parsed = np.loadtxt(filename, unpack=True)
    return [(parsed[0][i], parsed[1][i]) for i in range(len(parsed[0]))]

def split_xy(coords: list) -> (list, list):
    # splits a list of coordinates into x & y
    return [coords[i][0] for i in range(len(coords))],\
           [coords[i][1] for i in range(len(coords))]

def preprocess_list_header(filename):
    with open("data/rawestdata/" + filename) as file:
        with open ("data/rawedata/" + filename, "w+") as write:
            for line in file:
                if any(char.isalpha() for char in line):
                    continue
                else:
                    write.write(line)

def preprocess_list_n(filename):
    with open("data/rawedata/" + filename) as file:
        with open("data/rawdata/" + filename, "w+") as write:
            for line in file:
                s = line.strip().split(".")
                try:
                    if int(s[0]) > 1:
                        continue
                except:
                    pass
                write.write(line)

def split_data(filename):
    # splits data in first half of loop and other half (which needs to be reversed)
    with open("data/rawdata/" + filename) as file:
        with open("data/splitdata/" + filename[:-4] + "_1.dat", "w+") as write1:
            with open("data/splitdata/" + filename[:-4] + "_2.dat", "w+") as write2:
                flag = False
                count = 0
                for line in file:
                    if any(char.isdigit() for char in line) and not flag:
                        write1.write(line)
                    elif any(char.isdigit() for char in line) and flag:
                        write2.write(line)
                    elif count != 0:
                        flag = True
                    count += 1

def merge_and_reverse_lists (filename):
    # merge two lists and reverse the second one
    with open("data/loopdata/" + filename[:-4] + "_loop.dat", "w+") as write:
        with open("data/splitdata/" + filename[:-4] + "_1.dat", "r") as file:
            for line in file:
                write.write(line)
        with open("data/splitdata/" + filename[:-4] + "_2.dat", "r") as file:
            lines = []
            for line in file:
                lines.append(line)
            lines.reverse()
            for line in lines:
                write.write(line)

def make_continuuous_loop(filename):
    preprocess_list_header(filename)
    preprocess_list_n(filename)
    split_data(filename)
    merge_and_reverse_lists(filename)
