from lib.MyLumerical.LumAPI import *
import lumapi
import matplotlib.pyplot as plt
import time
import math


indent_path = 'D:/0419_oriSet/0419_TFAPO_0.465/indent'
fdtd = lumapi.FDTD()
indent_step = 20
file_num = 35
indent = []
CE = []
mode_factor = []
T = []

for n in range(1, file_num+1):
    ind = n * indent_step
    indent.append(ind)
    fdtd.load(f'{indent_path}/indent_{ind}.fsp')
    run_lsf_in_fdtd(fdtd, "E:/degree_thesis/script/lsf/t_expansion_P_wg2.lsf")

    T.append(get_value_from_fdtd(fdtd, "T2"))
    mode_factor.append(get_value_from_fdtd(fdtd, "M"))
    CE.append(10 * math.log10(get_value_from_fdtd(fdtd, "FOM")))

    fdtd.eval("newproject;")
    time.sleep(2)

plt.plot(indent, T, "-b", label="transmission")
plt.plot(indent, mode_factor, "-r", label="mode_factor")
plt.legend(loc="upper right")
plt.xlim(indent[0], indent[-1])
plt.ylim(0.3, 0.6)
plt.xlabel("indent (nm)")
plt.ylabel("fraction")
plt.show()
plt.clf()

plt.plot(indent, CE, "-b", label="transmission")
plt.legend(loc="upper right")
plt.xlim(indent[0], indent[-1])
plt.ylim(-10, 0)
plt.xlabel("indent (nm)")
plt.ylabel("coupling efficiency (dB)")
plt.show()
plt.clf()
