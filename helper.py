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
    return [coords[i][0] for i in range(len(coords))], \
           [coords[i][1] for i in range(len(coords))]


def preprocess_list(filename: str) -> None:
    with open("data/rawdata/" + filename) as file:
        with open("data/skinneddata/" + filename, "w+") as write:
            for line in file:
                if any(char.isalpha() for char in line):
                    continue
                else:
                    s = line.strip().split(".")
                    try:
                        if int(s[0]) > 1:
                            continue
                    except:
                        pass
                    write.write(line)


def check_selig_format(filename: str) -> bool:
    with open("data/skinneddata/" + filename) as file:
        for line in file:
            s = line.strip().split(".")
            try:
                if int(s[0]) == 1:
                    return True
                elif int(s[0]) == 0:
                    return False
            except:
                pass
            break


def split_data(filename: str) -> None:
    # splits data in first half of loop and other half (which needs to be reversed)
    with open("data/skinneddata/" + filename) as file:
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


def merge_and_reverse_lists(filename: str, rev1=True, rev2=False) -> str:
    # merge two lists and reverse the second one
    with open("data/loopdata/" + filename, "w+") as write:
        with open("data/splitdata/" + filename[:-4] + "_1.dat", "r") as file:
            lines1 = []
            for line in file:
                lines1.append(line)
            if rev1:
                lines1.reverse()
            for line in lines1:
                write.write(line)
        with open("data/splitdata/" + filename[:-4] + "_2.dat", "r") as file:
            lines2 = []
            for line in file:
                lines2.append(line)
            if rev2:
                lines2.reverse()
            for line in lines2:
                write.write(line)


def finish_data(filename: str, path: str) -> None:
    with open("data/processeddata/" + filename, "w+") as write:
        with open(path + filename) as file:
            for line in file:
                write.write(line)


def make_continuuous_loop(filename: str, rev1: bool = True, rev2: bool = False) -> None:
    preprocess_list(filename)
    # preprocess_list_n(filename)
    selig = check_selig_format(filename)
    if not selig:
        split_data(filename)
        merge_and_reverse_lists(filename, rev1, rev2)
        finish_data(filename, "data/loopdata/")
    else:
        finish_data(filename, "data/skinneddata/")
