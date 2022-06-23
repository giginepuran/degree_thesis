from lib.MyLumerical.LumAPI import *
import lumapi
import matplotlib.pyplot as plt
import time
import math


fiberTOL_path = 'D:/final/fiber_TOL'
fdtd = lumapi.FDTD()
ce = []
wl = [w for w in range(1530, 1570+1, 5)]
colors = {"-6":"-r", "-4":"-y", "-2":"-g", "0":"-b", "2":"-m", "4":"-c", "6":"-k"}

for dt in range(-6, 6+1, 2):
    ce_ = []
    for w in wl:
        fdtd.load(f'{fiberTOL_path}/dtheta{dt}_lambda{w}.fsp')
        run_lsf_in_fdtd(fdtd, "E:/degree_thesis/script/lsf/PDL_Analysis.lsf")
        ce_.append(10 * math.log10(get_value_from_fdtd(fdtd, "CE2")))
        time.sleep(5)
    ce.append(ce_)
    plt.plot(wl, ce_, colors[f"{dt}"], label=f"{dt} deg.")

plt.title("CE of fiber with error tilt angle")
plt.xlabel("wavelength (nm)")
plt.ylabel("CE (dB)")
plt.show()
plt.clf()

print(wl)
print(ce)