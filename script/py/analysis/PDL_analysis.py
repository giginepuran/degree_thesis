from lib.MyLumerical.LumAPI import *
import lumapi
import matplotlib.pyplot as plt
import time


wavelength = [1.55, 1.600, 1.574, 1.548, 1.524, 1.500]
ceiling = [0.5, 0.2, 0.5, 0.5, 0.15, 0.05]
PDL_path = 'D:/0419_oriSet/0419_TFUNI_0.425/PDL/1550'
fdtd = lumapi.FDTD()
angle = []
T1 = []
T2 = []
T_tot = []
n = 1
for wl_index in range(n):
    T1.append([])
    T2.append([])
    T_tot.append([])

for pol in range(0, 180+1, 5):
    fdtd.load(f'{PDL_path}/pol{pol}.fsp')
    run_lsf_in_fdtd(fdtd, "E:/degree_thesis/script/lsf/PDL_Analysis.lsf")
    t1 = get_value_from_fdtd(fdtd, "T1")
    t2 = get_value_from_fdtd(fdtd, "T2")
    t_tot = get_value_from_fdtd(fdtd, "T_tot")
    angle.append(pol)
    for wl_index in range(n):
        #T1[wl_index].append(t1[wl_index])
        #T2[wl_index].append(t2[wl_index])
        #T_tot[wl_index].append(t_tot[wl_index])
        T1[wl_index].append(t1)
        T2[wl_index].append(t2)
        T_tot[wl_index].append(t_tot)
    fdtd.eval("newproject;")
    time.sleep(2)

for wl_index in range(n):
    plt.plot(angle, T1[wl_index], "-b", label="T1")
    plt.plot(angle, T2[wl_index], "-r", label="T2")
    plt.plot(angle, T_tot[wl_index], "-g", label="T1+T2")
    plt.legend(loc="upper right")
    plt.xlim(0, 180)
    plt.ylim(0, ceiling[wl_index])
    plt.title(f"wavelength = {wavelength[wl_index]} um")
    plt.xlabel("polarization (degree)")
    plt.ylabel("Coupling efficiency")
    plt.show()
    plt.clf()
