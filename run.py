from helper import make_panels, parsecoords, define_panels
from profile_new import AirfoilProfile
from make_cylinder import cylinder, circle
from joukowski import make_joukowski, make_karman_trefftz, joukowski_ca
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scenario.errorcylindertheoretical import errorcylindertheoretical
from scenario.eightsidedcylindererror import eightsidedcylindererror
from scenario.eightsidedcylinderpanelparameters import eightsidedcylinderpanelparameters
from scenario.writecylinderintocircle import writecylinderintocircle
from scenario.novortexsystemmatrix import novortexsystemmatrix
from scenario.analyticalcylinder import analyticalcylinder
from scenario.cylinderqvc import cylinderqvc
from scenario.rotatingcylinder import rotatingcylinder
from scenario.completeprofile import completeprofile
from scenario.completeprofile2d import completeprofile2d
from scenario.joukowskiplots import joukowskiplots
from scenario.joukowskierror import joukowskierror
from scenario.karmanerror import karmanerror
from scenario.definitionfigures import definitionfigures
from scenario.definitionpanel import definitionpanel
from scenario.loadandplot import loadandplot
from scenario.custom import custom
from scenario.makeprofileplot import makeprofileplot
from scenario.lineplotprofiles import lineplotprofiles
from scenario.caformulafind import caformulafind

#custom()

#get paneldefinitionsbild
#definitionpanel()

#get zaehlrichtungsbild
#definitionfigures()

#karman trefftz error plot and error analysis
#karmanerror()

#joukowski error plot and error analysis
#joukowskierror()

#joukowski und karman-trefftz graphen generieren
#joukowskiplots()

#formel für ca bestimmen für profile
caformulafind()

#bessere lineplots
#lineplotprofiles()

#komplette Graphen für vx, vy, q und cp
#completeprofile()

#funkionierende komplette Graphen in 2d
#loadandplot()

#8-seitiger Zylinder zwischen -15 und 15 grad
#rotatingcylinder()

#q, vt, cp für 8-seitigen Zylinder
#cylinderqvc()

#Analytische Lösung 8-seitgier Zylinder
#analyticalcylinder()

#Systemmatrix 8-seitiger Zylinder
#novortexsystemmatrix()

#Zylinder in Kreis einschreiben
#writecylinderintocircle()

#BigGraphs
#besser: über scenario-Folder starten
#makeprofilegraphs()
#makeprofileplot()

# Panelparameter 8-seitig
#eightsidedcylinderpanelparameters()

# Grafik Abweichung Berechnung Theorie
#eightsidedcylindererror()

# error kreiszylinder theoretischer wert
#errorcylindertheoretical()
