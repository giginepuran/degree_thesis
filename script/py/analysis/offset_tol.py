from lib.MyLumerical.LumAPI import *
import lumapi
import matplotlib.pyplot as plt
import time


offset_path = 'D:/final/tolerance'
fdtd = lumapi.FDTD()
ce = [] #(y,x)
x = np.arange(-60, 60+1, 20)
y = np.arange(-60, 60+1, 20)
X, Y = np.meshgrid(x, y)

for dy in range(-60, 60+1, 20):
    yy = []
    for dx in range(-60, 60+1, 20):
        fdtd.load(f'{offset_path}/dx{dx}_dy{dy}.fsp')
        run_lsf_in_fdtd(fdtd, "E:/degree_thesis/script/lsf/PDL_Analysis.lsf")
        yy.append(get_value_from_fdtd(fdtd, "CE2"))
        time.sleep(5)
    ce.append(yy)

Z = np.array(ce)


fig, (ax0, ax1) = plt.subplots(nrows=2)
im = ax0.pcolormesh(X, Y, Z, vmin=Z.min(), vmax=Z.max())
fig.colorbar(im, ax=ax0)
ax0.set_title('CE of shallow etch with offset')
# contours are *point* based plots, so convert our bound into point
# centers
cf = ax1.contourf(X, Y, Z, vmin=Z.min(), vmax=Z.max())
fig.colorbar(cf, ax=ax1)
ax1.set_title('CE of shallow etch with offset')
# adjust spacing between subplots so `ax1` title and `ax0` tick labels
# don't overlap
fig.colorbar(im)
fig.tight_layout()
plt.show()
plt.clf()

