import os
import shutil
import sys
import lumapi
from past.builtins import execfile
import time
from os.path import exists
from PSO import swarm

print("API setting complete.")

workPath = '/home/u6097335/OptGratingCoupler'
filePath = '/home/u6097335/result'
setBase = open(f'{workPath}/lsf/setBase1.lsf', 'r').read()
getData = open(f'{workPath}/lsf/getData.lsf', 'r').read()
qsubTemplate = open(f'{workPath}/jobTemplate.sh', 'r').read()
afterEvolution = open(f'{workPath}/afterEvolution.sh', 'r').read()

# env
maxGen = 70
population = 20
execfile('buildOptPath.py')

# jobScript for qsub
for generation in range(1, maxGen + 1):
    with open(f'{filePath}/optPath/Gen{generation}/job_gen{generation}.sh', "w") as txt:
        script = qsubTemplate
        script = script.replace('{generation}', f'{generation}')
        script = script.replace('{population}', f'{population}')
        txt.write(script)
    with open(f'{filePath}/optPath/Gen{generation}/afterEvolution.sh', "w") as txt:
        script = afterEvolution
        script = script.replace('{generation}', f'{generation}')
        script = script.replace('{population}', f'{population}')
        txt.write(script)

floor = [100, 100, 100, 50, 10]
ceiling = [300, 300, 300, 200, 90]
dimension = 5
mySwarm = swarm.Swarm(dimension, population, floor, ceiling)
fdtd = lumapi.FDTD(hide=True)
for generation in range(1, maxGen + 1):
    # build fsp & simulate & get fom
    print(f"Building all individuals in Gen{generation}")
    for p in range(population):
        para = mySwarm.particles[p].get_x()
        build = setBase
        for i in range(1, dimension + 1, 1):
            build = build.replace(f'para{i}__', f'{para[i - 1][0]}')
        fdtd.eval(build)
        fdtd.save(f'{filePath}/optPath/Gen{generation}/p{p + 1}/ind.fsp')

    print(f"Waiting for qsub simulation complete")
    qsub_success = False
    while not qsub_success:
        job_id = os.popen(f'qsub {filePath}/optPath/Gen{generation}/job_gen{generation}.sh').read()
        if ".srvc1" in job_id:
            print(f"job id : {job_id}")
            qsub_success = True
        else:
            print(f"qsub failed at Gen{generation}\nError message:{job_id}")
        time.sleep(5)

    lastTime = 0
    finish = False
    while not finish:
        if exists(f"{filePath}/optPath/Gen{generation}/finish.txt"):
            finish = True
        else:
            print(f"Gen{generation} haven't finished yet, Past Time:{lastTime}")
            time.sleep(5 * population)
            lastTime = lastTime + population * 5

    print(f"Gen{generation} simulation completed")
    fom = []
    for p in range(population):
        fdtd.load(f'{filePath}/optPath/Gen{generation}/p{p + 1}/ind.fsp')
        fdtd.eval(getData)
        result = fdtd.getv('FOM')
        fom.append(result)

    pbest_changed = mySwarm.update_fom(fom)

    print("recording parameters of each individual")
    # save parameters&fsp of each particle
    for p in range(population):
        with open(f'{filePath}/optPath/Gen{generation}/p{p + 1}/fom.txt', "w") as txt:
            txt.write(f'{fom[p]}')
        with open(f'{filePath}/optPath/Gen{generation}/p{p + 1}/pbest/fom.txt', "w") as txt:
            txt.write(f'{mySwarm.p_foms[p]}')
        for d in range(dimension):
            with open(f'{filePath}/optPath/Gen{generation}/p{p + 1}/para{d + 1}.txt', "w") as txt:
                txt.write(f'{mySwarm.xs[p][d][0]}')
            with open(f'{filePath}/optPath/Gen{generation}/p{p + 1}/pbest/para{d + 1}.txt', "w") as txt:
                txt.write(f'{mySwarm.p_xs[p][d][0]}')
        if pbest_changed[p]:
            shutil.copy(f'{filePath}/optPath/Gen{generation}/p{p + 1}/ind.fsp',
                        f'{filePath}/optPath/Gen{generation}/p{p + 1}/pbest/ind.fsp')
        else:
            shutil.copy(f'{filePath}/optPath/Gen{generation - 1}/p{p + 1}/pbest/ind.fsp',
                        f'{filePath}/optPath/Gen{generation}/p{p + 1}/pbest/ind.fsp')

    print("assigning/recording the global best individual")
    # save parameters&fsp of gbest
    for d in range(dimension):
        with open(f'{filePath}/optPath/Gen{generation}/gbest/para{d + 1}.txt', "w") as txt:
            txt.write(f'{mySwarm.p_xs[mySwarm.gbest_index][d][0]}')
    with open(f'{filePath}/optPath/Gen{generation}/gbest/fom.txt', "w") as txt:
        txt.write(f'{mySwarm.p_foms[mySwarm.gbest_index]}')
    shutil.copy(f'{filePath}/optPath/Gen{generation}/p{mySwarm.gbest_index + 1}/pbest/ind.fsp',
                f'{filePath}/optPath/Gen{generation}/gbest/ind.fsp')

    print(f"Gen{generation} finished, doing evolution to each individual\n\n")
    # evolute all particle to new position (x)
    mySwarm.evolution()

    print("\n\n")
    if generation >= 3:
        print(f"removing fsp files...")  # only ind.fsp of gbest remain
        os.system(f'sh {filePath}/optPath/Gen{generation-2}/afterEvolution.sh')
