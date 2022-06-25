from lib.MyLumerical.LumAPI import *
import lumapi
import matplotlib.pyplot as plt
import time
import math


PDL_path = 'D:/final/0619_APOUNI_0.44/fixed/maxPDL'
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
#plt.ylim(-10, 0)
plt.xlabel("wavelength (nm)")
plt.ylabel("coupling efficiency (dB)")
plt.show()
plt.clf()

plt.plot(wl, PDL, "-r", label="max_PDL")
plt.legend(loc="upper right")
plt.xlim(head, tail)
plt.ylim(0, 3)
#plt.title(f"max_PDL")
plt.xlabel("wavelength (nm)")
plt.ylabel("PDL (dB)")
plt.show()
plt.clf()

print(PDL)
print(ce_0)
print(ce_90)
"""
E:\degree_thesis\venv\Scripts\python.exe E:/degree_thesis/script/py/analysis/MAX_PDL.py
[2.5817499325841737, 2.447630293693811, 2.1658868464733487, 1.863365403154578, 1.605116935308394, 1.5107424387857353, 1.4507947622204869, 1.147013014470439, 1.0088714400547043, 0.8473197231813607, 0.5637595315279889, 0.3325235115147005, 0.05608302142038246, 0.2898122560619818, 0.6966850444689738, 1.0109083768520772, 0.8421733295643801, 0.4866597953560792, 0.4979982060785062, 0.42061535522555893, 0.49325479115980997]
[-14.148380587277995, -11.72579120333114, -9.859434114669686, -8.28408019982007, -6.878531942238456, -5.952993724091399, -4.9633761093357895, -3.8484318247910987, -3.4354105090012914, -3.1528331314082854, -3.1639957448542715, -3.4381937366349664, -3.8851453765729915, -4.489119578688891, -5.47747281383062, -6.8290276267244945, -8.40577779666136, -10.45710617156027, -13.106030811803581, -16.089693006587517, -19.522176478469618]
[-16.73013051986217, -14.17342149702495, -12.025320961143034, -10.147445602974647, -8.48364887754685, -7.463736162877134, -6.414170871556276, -4.995444839261538, -4.444281949055996, -4.000152854589646, -3.7277552763822603, -3.770717248149667, -3.941228397993374, -4.199307322626909, -4.7807877693616465, -5.818119249872417, -7.5636044670969795, -9.97044637620419, -12.608032605725075, -15.669077651361958, -19.028921687309808]
"""
