from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
from lib.pyDriveLib import Get
from lib.pyDriveLib import Put
from lib.CommWithTaiwania import Taiwania
from lib.CommWithTaiwania import BuildHost
from lib.CommWithTaiwania import BuildHost_interpolation
from lib.CommWithTaiwania import Transfer
import os
import time
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

colors = ['b', 'g', 'r', 'c']
legends = ['l1', 'l2', 'l3', 'l5']

start_para_no = 1
end_para_no = 4
parameter_num = end_para_no - start_para_no + 1
dimension = parameter_num * 5
uniform = True
title_template = 'TFAPO uniform spline Gen__GEN__'
gbest_path_template = 'D:/final/0619_APOUNI_0.44/fixed/gbest'
# 'D:/0427~0429set//Gen50/gbest'
# 'E:/degree_thesis/local/saving_path/Gen10/gbest'
for gen in range(17, 17+1):
    title = title_template.replace('__GEN__', f'{gen}')
    gbest_path = gbest_path_template.replace('__GEN__', f'{gen}')
    paras = []
    for para_no in range(1, dimension+1):
        paras.append(float(open(f'{gbest_path}/para{para_no}.txt', 'r').read()))
    paras = np.array(paras)

    after_interpolation = []
    num_of_point_in_a_set = dimension // parameter_num

    if uniform:
        for para_no in range(1, parameter_num+1):
            x = np.linspace(1, 20, num=num_of_point_in_a_set, endpoint=True)
            y = paras[(para_no-1)*num_of_point_in_a_set:para_no*num_of_point_in_a_set]
            f = interp1d(x, y.reshape(num_of_point_in_a_set,), kind='cubic')
            x_new = np.linspace(1, 20, num=20, endpoint=True)
            y_new = f(x_new)
            after_interpolation.append(y_new)
            plt.plot(x_new, y_new, colors[para_no+start_para_no-2], label=legends[para_no+start_para_no-2])
            plt.scatter(x, y, color=colors[para_no+start_para_no-2], marker='D')
    else:
        x_new = np.array([xx for xx in range(1, 21)])
        x = np.array([1, 3, 7, 12, 17])
        for para_no in range(1, parameter_num+1):
            y = paras[(para_no-1)*num_of_point_in_a_set:para_no*num_of_point_in_a_set]
            f = interp1d(x, y.reshape(num_of_point_in_a_set, ), kind='cubic', fill_value='extrapolate')
            y_new = f(x_new)
            after_interpolation.append(y_new)
            plt.plot(x_new, y_new, colors[para_no+start_para_no-2], label=legends[para_no+start_para_no-2])
            plt.scatter(x, y, color=colors[para_no+start_para_no-2], marker='D')

    lsf_para = 'ln = [para__1__, para__2__, para__3__, para__4__, para__5__,\n' + \
               '      para__6__, para__7__, para__8__, para__9__, para__10__,\n' + \
               '      para__11__,para__12__,para__13__,para__14__,para__15__,\n' + \
               '      para__16__,para__17__,para__18__,para__19__,para__20__]*1e-9;\n'
    for para_no in range(1, parameter_num+1):
        script = lsf_para
        script = script.replace('ln', legends[para_no-1])
        for i in range(1, 21):
            script = script.replace(f'para__{i}__', f'{round(after_interpolation[para_no-1][i-1], 0)}')
        print(script)

    plt.legend(loc="upper right")
    plt.xlim(1, 20)
    plt.xticks(np.arange(1, 21))
    plt.xlabel("Period")
    plt.ylabel("(nm)")
    # plt.title(title)
    plt.savefig(f"{gen}.png")
    plt.show()

