from lib.MyLumerical.LumAPI import *
import lumapi
import matplotlib.pyplot as plt
import time
import math


PDL_path = 'D:/final/0619_APOUNI_0.44/maxPDL'
fdtd = lumapi.FDTD()
ce_0 = []
ce_90 = []
PDL = []
wl = []
head = 1500
tail = 1600
step = 5

for wavelength in range(head, tail+1, step):
    wl.append(wavelength)

    fdtd.load(f'{PDL_path}/{wavelength}_pol0.fsp')
    run_lsf_in_fdtd(fdtd, "E:/degree_thesis/script/lsf/PDL_Analysis.lsf")
    ce0 = 10*math.log10(get_value_from_fdtd(fdtd, "CE_tot"))
    fdtd.eval("newproject;")
    time.sleep(2)

    fdtd.load(f'{PDL_path}/{wavelength}_pol90.fsp')
    run_lsf_in_fdtd(fdtd, "E:/degree_thesis/script/lsf/PDL_Analysis.lsf")
    ce90 = 10*math.log10(get_value_from_fdtd(fdtd, "CE_tot"))
    fdtd.eval("newproject;")
    time.sleep(2)

    pdl = ce0-ce90
    PDL.append(pdl if pdl > 0 else -pdl)
    ce_0.append(ce0)
    ce_90.append(ce90)

plt.plot(wl, ce_0, "-b", label="pol-0")
plt.plot(wl, ce_90, "-r", label="pol-90")
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

print(PDL)
print(ce_0)
print(ce_90)