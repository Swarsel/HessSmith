from make_cylinder import cylinder
from helper import make_panels
from profile import Profile

for npanels in range(8, 9):
    for a in range(0, 1):
        x, y = cylinder(n=npanels)
        panels = make_panels(x, y)
        profile = Profile(panels, f"{npanels}-Sided Cylinder", vortex=False)

        profile.solve()
        profile.plot()
        print(f"Panels: {panels}, Angle: {a}\n"
              f"Tangential velocity:\n"
              f"{[panel.vt for panel in panels]}\n"
              f"Constituent Pressure:\n"
              f"{[panel.cp for panel in panels]}\n"
              f"Source vector:\n"
              f"{[panel.q for panel in panels]}\n"
              f"Gamma:\n"
              f"{profile.gamma}\n"
              f"Constituent updrift:\n"
              f"{profile.ca}\n"
              f"Accuracy:\n"
              f"{profile.accuracy}\n\n")