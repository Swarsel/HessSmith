import numpy as np
from panel import Panel


def index(list: list, element: int) -> float:
    # allows to use normal list as a closed loop, connecting the last and first elements
    return list[element % len(list)]

def check_ccw(x, y):
    edge = np.zeros(len(x) - 1)
    for i in range(len(x) - 1):  # Loop over all panels
        edge[i] = (x[i + 1] - x[i]) * (y[i + 1] + y[i])
    if np.sum(edge) <0:
        return True
    else:
        return False


def make_panels_old(x, y):
    panels = np.empty(len(x), dtype=object)
    for i in range(len(x)):
        panels[i] = Panel(index(x, i), index(y, i), index(x, i + 1), index(y, i + 1))
    return panels

def make_panels(x, y):
    panels = np.empty(len(x), dtype=object)
    for i in range(len(x)):
        panels[i] = Panel(x[i], y[i], x[i+1], y[i+1])
    #if (panels[0].xa, panels[0].ya) == (panels[0].xb, panels[0].yb):
    #    panels = panels[1:]
    return panels

def make_panels_ant(x, y):
    panels = np.empty(len(x)-1, dtype=object)
    for i in range(len(x)-1):
        panels[i] = Panel(x[-i-2], y[-i-2], x[-i-1], y[-i-1])
    #if (panels[0].xa, panels[0].ya) == (panels[0].xb, panels[0].yb):
    #    panels = panels[1:]
    return panels


def parsecoords(filename: str):
    # reads coordinates from file
    x, y = np.loadtxt(filename, dtype=float, unpack=True)

    return x, y

def write_coords(x,y, filename):
    with open("data/writtendata/" + filename, "w+") as write:
        for x, y in zip(x,y):
            write.write(f"{x} {y}\n")

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
            first = ""
            for line in file:
                if not first:
                    first = line
                last = line
                write.write(line)
            #if str(first) != str(last)+"\n" and str(first) != str(last):
            #    write.write(first)


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
