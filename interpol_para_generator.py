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


parameter_num = 7
dimension = parameter_num * 5
gbest_path = 'E:/degree_thesis/local/0417_TCAPO_0.359/Gen50/gbest'

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

lsf_para = 'ln = [para__1__, para__2__, para__3__, para__4__, para__5__,\n' + \
           '      para__6__, para__7__, para__8__, para__9__, para__10__,\n' + \
           '      para__11__,para__12__,para__13__,para__14__,para__15__,\n' + \
           '      para__16__,para__17__,para__18__,para__19__,para__20__]*1e-9;\n'
for para_no in range(1, parameter_num+1):
    script = lsf_para
    script = script.replace('ln', f'l{para_no}')
    for i in range(1, 21):
        script = script.replace(f'para__{i}__', f'{round(after_interpolation[para_no-1][i-1], 2)}')
    print(script)
