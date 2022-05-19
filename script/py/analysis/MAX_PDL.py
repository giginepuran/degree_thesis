from lib.MyLumerical.LumAPI import *
import lumapi
import matplotlib.pyplot as plt
import time
import math


PDL_path = 'D:/0419_oriSet/0419_TFAPO_0.465/MAX_PDL'
fdtd = lumapi.FDTD()
t_0 = []
t_90 = []
PDL = []
wl = []
head = 1475
tail = 1625
step = 10

for wavelength in range(head, tail+1, step):
    wl.append(wavelength)

    fdtd.load(f'{PDL_path}/{wavelength}_pol0.fsp')
    run_lsf_in_fdtd(fdtd, "E:/degree_thesis/script/lsf/PDL_Analysis.lsf")
    T0 = 10*math.log10(get_value_from_fdtd(fdtd, "T_tot"))
    fdtd.eval("newproject;")
    time.sleep(2)

    fdtd.load(f'{PDL_path}/{wavelength}_pol90.fsp')
    run_lsf_in_fdtd(fdtd, "E:/degree_thesis/script/lsf/PDL_Analysis.lsf")
    T90 = 10*math.log10(get_value_from_fdtd(fdtd, "T_tot"))
    fdtd.eval("newproject;")
    time.sleep(2)

    pdl = T0-T90
    PDL.append(pdl if pdl > 0 else -pdl)
    t_0.append(T0)
    t_90.append(T90)

plt.plot(wl, t_0, "-b", label="pol-0")
plt.plot(wl, t_90, "-r", label="pol-90")
plt.legend(loc="upper right")
plt.xlim(head, tail)
plt.ylim(-10, 0)
plt.xlabel("wavelength (nm)")
plt.ylabel("Coupling efficiency")
plt.show()
plt.clf()

plt.plot(wl, PDL, "-r", label="max_PDL")
plt.legend(loc="upper right")
plt.xlim(head, tail)
#plt.ylim(0, 3)
#plt.title(f"max_PDL")
plt.xlabel("wavelength (nm)")
plt.ylabel("PDL (dB)")
plt.show()
plt.clf()
