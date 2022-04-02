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


parameter_num = 3
dimension = parameter_num * 5
gbest_path = 'D:/saving_path_0402_0.44/Gen40/gbest'

paras = []
for para_no in range(1, dimension+1):
    paras.append(float(open(f'{gbest_path}/para{para_no}.txt', 'r').read()))
paras = np.array(paras)

after_interpolation = []
num_of_point_in_a_set = dimension // parameter_num
for para_no in range(1, parameter_num+1):
    x = np.linspace(1, 20, num=num_of_point_in_a_set, endpoint=True)
    y = paras[(para_no-1)*num_of_point_in_a_set:para_no*num_of_point_in_a_set]
    f = interp1d(x, y.reshape(num_of_point_in_a_set,), kind='cubic')
    x_new = np.linspace(1, 20, num=20, endpoint=True)
    after_interpolation.append(f(x_new))

lsf_para = 'ln = [para__1, para__2, para__3, para__4, para__5,\n' + \
           '      para__6, para__7, para__8, para__9, para__10,\n' + \
           '      para__11,para__12,para__13,para__14,para__15,\n' + \
           '      para__16,para__17,para__18,para__19,para__20]*1e-9;\n'
for para_no in range(1, parameter_num+1):
    script = lsf_para
    script = script.replace('ln', f'l{para_no}')
    for i in range(1, 21):
        script = script.replace(f'para__{i}', f'{round(after_interpolation[para_no-1][i-1], 2)}')
    print(script)
print(paras)
print(after_interpolation)
