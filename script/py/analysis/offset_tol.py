from lib.MyLumerical.LumAPI import *
import lumapi
import matplotlib.pyplot as plt
import time


plt.rc('font',family='Times New Roman')
offset_path = 'D:/final/0619_APOUNI_0.44/analysis/offset_TOL'
ce = [] #(y,x)
x = np.arange(-60, 60+1, 20)
y = np.arange(-60, 60+1, 20)
X, Y = np.meshgrid(x, y)
"""
fdtd = lumapi.FDTD()
for dy in range(-60, 60+1, 20):
    yy = []
    for dx in range(-60, 60+1, 20):
        fdtd.load(f'{offset_path}/dx{dx}_dy{dy}.fsp')
        run_lsf_in_fdtd(fdtd, "E:/degree_thesis/script/lsf/PDL_Analysis.lsf")
        yy.append(get_value_from_fdtd(fdtd, "CE2"))
        time.sleep(5)
    ce.append(yy)

Z = np.array(ce)
"""

X = [[-60, -40, -20, 0, 20, 40, 60],
 [-60, -40, -20, 0, 20, 40, 60],
 [-60, -40, -20, 0, 20, 40, 60],
 [-60, -40, -20, 0, 20, 40, 60],
 [-60, -40, -20, 0, 20, 40, 60],
 [-60, -40, -20, 0, 20, 40, 60],
 [-60, -40, -20, 0, 20, 40, 60]]
Y = [[-60, -60, -60, -60, -60, -60, -60],
 [-40, -40, -40, -40, -40, -40, -40],
 [-20, -20, -20, -20, -20, -20, -20],
 [  0,   0,   0,  0,  0,   0,   0],
 [ 20,  20,  20,  20,  20,  20,  20],
 [ 40,  40,  40,  40,  40,  40,  40],
 [ 60,  60,  60,  60,  60,  60,  60]]
Z = [[0.35680124, 0.39299225, 0.41344678, 0.41085734, 0.38498154, 0.34247118, 0.2956847 ],
 [0.34936994, 0.39883679, 0.43196375, 0.44180814, 0.42352395, 0.38185327, 0.33100354],
 [0.33449742, 0.39372566, 0.43477571, 0.45351911, 0.44293565, 0.40563356, 0.35484009],
 [0.31558196, 0.37944414, 0.42558059, 0.45133615, 0.44891233, 0.41908409, 0.37250902],
 [0.29649905, 0.36195801, 0.41114349, 0.44197856, 0.44706521, 0.4258647, 0.38627638],
 [0.27990245, 0.34468048, 0.39520824, 0.42912727, 0.4404387,  0.42795374, 0.39677356],
 [0.26781157, 0.33013152, 0.38021235, 0.41542286, 0.43103814, 0.42594205, 0.40275939]]

Z = np.array(Z)
im = plt.pcolormesh(X, Y, Z, vmin=Z.min(), vmax=Z.max())
plt.xlabel("$\it{dx}$ (nm)")
plt.ylabel("$\it{dy}$ (nm)")
plt.title("Coupling Efficiency under shallow etching with offset")
plt.colorbar(im)
plt.show()
plt.clf()

cf = plt.contourf(X, Y, Z, vmin=Z.min(), vmax=Z.max())
plt.xlabel("$\it{dx}$ (nm)")
plt.ylabel("$\it{dy}$ (nm)")
plt.title("Coupling Efficiency under shallow etching with offset")
plt.colorbar(cf)
plt.show()
plt.clf()

print(X)
print(Y)
print(Z)
"""
[[-60 -40 -20   0  20  40  60]
 [-60 -40 -20   0  20  40  60]
 [-60 -40 -20   0  20  40  60]
 [-60 -40 -20   0  20  40  60]
 [-60 -40 -20   0  20  40  60]
 [-60 -40 -20   0  20  40  60]
 [-60 -40 -20   0  20  40  60]]
[[-60 -60 -60 -60 -60 -60 -60]
 [-40 -40 -40 -40 -40 -40 -40]
 [-20 -20 -20 -20 -20 -20 -20]
 [  0   0   0   0   0   0   0]
 [ 20  20  20  20  20  20  20]
 [ 40  40  40  40  40  40  40]
 [ 60  60  60  60  60  60  60]]
[[0.35680124 0.39299225 0.41344678 0.41085734 0.38498154 0.34247118
  0.2956847 ]
 [0.34936994 0.39883679 0.43196375 0.44180814 0.42352395 0.38185327
  0.33100354]
 [0.33449742 0.39372566 0.43477571 0.45351911 0.44293565 0.40563356
  0.35484009]
 [0.31558196 0.37944414 0.42558059 0.45133615 0.44891233 0.41908409
  0.37250902]
 [0.29649905 0.36195801 0.41114349 0.44197856 0.44706521 0.4258647
  0.38627638]
 [0.27990245 0.34468048 0.39520824 0.42912727 0.4404387  0.42795374
  0.39677356]
 [0.26781157 0.33013152 0.38021235 0.41542286 0.43103814 0.42594205
  0.40275939]]
"""