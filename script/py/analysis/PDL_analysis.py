from lib.MyLumerical.LumAPI import *
import lumapi
import matplotlib.pyplot as plt
import time


wavelength = [1.55]
ceiling = [0.5]
PDL_path = 'D:/final/0619_APOUNI_0.44/fixed/PDL'
fdtd = lumapi.FDTD()
angle = []
CE1 = []
CE2 = []
CE_tot = []
n = 1
for wl_index in range(n):
    CE1.append([])
    CE2.append([])
    CE_tot.append([])

for pol in range(0, 180+1, 5):
    fdtd.load(f'{PDL_path}/pol{pol}.fsp')
    run_lsf_in_fdtd(fdtd, "E:/degree_thesis/script/lsf/PDL_Analysis.lsf")
    ce1 = get_value_from_fdtd(fdtd, "CE1")
    ce2 = get_value_from_fdtd(fdtd, "CE2")
    ce_tot = get_value_from_fdtd(fdtd, "CE_tot")
    angle.append(pol)
    for wl_index in range(n):
        #T1[wl_index].append(t1[wl_index])
        #T2[wl_index].append(t2[wl_index])
        #T_tot[wl_index].append(t_tot[wl_index])
        CE1[wl_index].append(ce1)
        CE2[wl_index].append(ce2)
        CE_tot[wl_index].append(ce_tot)
    fdtd.eval("newproject;")
    time.sleep(2)

for wl_index in range(n):
    plt.plot(angle, CE1[wl_index], "-b", label="CE(+y)")
    plt.plot(angle, CE2[wl_index], "-r", label="CE(+x)")
    plt.plot(angle, CE_tot[wl_index], "-g", label="CE(+y)+CE(+x)")
    plt.legend(loc="upper right")
    plt.xlim(0, 180)
    plt.ylim(0, ceiling[wl_index])
    plt.title(f"wavelength = {wavelength[wl_index]} um")
    plt.xlabel("polarization (degree)")
    plt.ylabel("coupling efficiency")
    plt.show()
    plt.clf()

print(CE1[0])
print(CE2[0])
print(CE_tot[0])
"""
E:\degree_thesis\venv\Scripts\python.exe E:/degree_thesis/script/py/analysis/PDL_analysis.py
[0.2413071728830444, 0.2020624128387784, 0.16356812122285108, 0.12698932222164616, 0.09343738938541503, 0.06393349557756685, 0.03937054558041183, 0.020498386007618483, 0.007886359244381979, 0.0019203128227296747, 0.0027803768856971053, 0.01044109049746534, 0.024671414343986547, 0.04503861785239659, 0.07092320078273544, 0.10153983279795747, 0.13595765514680946, 0.1731308590823155, 0.2119298911177762, 0.2511757885686379, 0.2896760133927495, 0.32626068562021143, 0.3598181503735199, 0.38932707485315515, 0.4138919644733821, 0.4327687229599355, 0.44536978078973893, 0.451333290642503, 0.45045599504410366, 0.4427917363347977, 0.42854791301964507, 0.40818281833825476, 0.3822950856092424, 0.35168024394797626, 0.31726552732775853, 0.28009655392143035, 0.2413071719677526]
[0.24130739575515056, 0.2800970809593201, 0.31726636879625564, 0.35168142164971433, 0.3822965875568285, 0.4081846490022542, 0.4285500525834587, 0.4427941578131342, 0.450458658146156, 0.4513361529599876, 0.4453727922801677, 0.432771823196107, 0.41389510081220315, 0.3893301840750741, 0.3598211795625177, 0.32626357849072546, 0.2896787232316516, 0.2511782660354794, 0.2119320990046765, 0.17313276891194923, 0.13595924726108713, 0.10154109330689341, 0.07092413077560458, 0.04503922713816883, 0.024671720632249653, 0.010441122039119023, 0.002780170625045449, 0.001919911631019013, 0.007885811491534476, 0.02049774530856198, 0.03936986779568668, 0.06393283644495334, 0.09343680500187729, 0.1269888699558062, 0.16356785294715143, 0.20206237036765773, 0.2413073952223441]
[0.48261456863819496, 0.4821594937980985, 0.4808344900191067, 0.4786707438713605, 0.4757339769422435, 0.47211814457982104, 0.4679205981638705, 0.4632925438207527, 0.45834501739053796, 0.4532564657827173, 0.4481531691658648, 0.44321291369357235, 0.4385665151561897, 0.4343688019274707, 0.43074438034525314, 0.42780341128868293, 0.4256363783784611, 0.4243091251177949, 0.4238619901224527, 0.42430855748058716, 0.4256352606538366, 0.42780177892710486, 0.4307422811491245, 0.434366301991324, 0.43856368510563176, 0.4432098449990545, 0.44814995141478436, 0.453253202273522, 0.45834180653563816, 0.46328948164335965, 0.46791778081533175, 0.4721156547832081, 0.4757318906111197, 0.4786691139037824, 0.48083338027490996, 0.4821589242890881, 0.48261456719009665]
"""
