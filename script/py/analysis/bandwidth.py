from lib.MyLumerical.LumAPI import *
import lumapi
import matplotlib.pyplot as plt
import time
import math


band_path = 'D:/final/0619_APOUNI_0.44/fixed/band'
fdtd = lumapi.FDTD()
ce = []
ct = []
wl = []
head = 1500
tail = 1600
step = 5

for wavelength in range(head, tail+1, step):
    wl.append(wavelength)

    fdtd.load(f'{band_path}/{wavelength}.fsp')
    run_lsf_in_fdtd(fdtd, "E:/degree_thesis/script/lsf/PDL_Analysis.lsf")
    ce.append(10*math.log10(get_value_from_fdtd(fdtd, "CE2")))
    ct.append(10 * math.log10(get_value_from_fdtd(fdtd, "CE1")/get_value_from_fdtd(fdtd, "CE2")))
    fdtd.eval("newproject;")
    time.sleep(2)

plt.plot(wl, ce, "-b", label="CE2")
# plt.legend(loc="upper right")
plt.xlim(head, tail)
# plt.ylim(-20, 0)
plt.xlabel("wavelength (nm)")
plt.ylabel("coupling efficiency (dB)")
plt.show()
plt.clf()

plt.plot(wl, ct, "-r", label="CE1 (crosstalk)")
# plt.legend(loc="upper right")
plt.xlim(head, tail)
# plt.ylim(-20, 0)
plt.xlabel("wavelength (nm)")
plt.ylabel("cross talk (dB)")
plt.show()
plt.clf()

print(wl)
print(ce)
print(ct)
"""
E:\degree_thesis\venv\Scripts\python.exe E:/degree_thesis/script/py/analysis/bandwidth.py
[1500, 1505, 1510, 1515, 1520, 1525, 1530, 1535, 1540, 1545, 1550, 1555, 1560, 1565, 1570, 1575, 1580, 1585, 1590, 1595, 1600]
[-15.357471373728469, -12.877327805660823, -10.888677616459994, -9.17790357162923, -7.651787388742982, -6.681285129106548, -5.664254275341381, -4.411525292746084, -3.9338033432191377, -3.5784021853751655, -3.45499878707661, -3.6175647269631828, -3.9283539739421696, -4.357885220378724, -5.132882293995282, -6.311457211537786, -7.974677460173959, -10.210548421936936, -12.853381848675012, -15.876903816200889, -19.27841709061297]
[-16.033674250876174, -16.41555263102063, -17.297826583333975, -18.474729573726705, -19.86269278291583, -20.5199289796035, -20.821437534200143, -22.003425284990044, -22.7268867450815, -22.827455620646937, -23.711281303078128, -24.30226636419556, -24.45999551617585, -24.42129363773799, -23.780398638187492, -24.054403648034967, -26.21726825882362, -30.843504352056293, -30.828592349459363, -32.21253547855059, -26.495134701142852]
"""