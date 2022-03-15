import sys, os

# optimization environment initializing
# 1 genration 1 directory,
# there are N particles(directory) in one generation

if not os.path.isdir(f'{filePath}/optPath'):
    os.mkdir(f'{filePath}/optPath')
for gen in range(1, maxGen+1):
    if not os.path.isdir(f'{filePath}/optPath/Gen{gen}'):
        os.mkdir(f'{filePath}/optPath/Gen{gen}')
    if not os.path.isdir(f'{filePath}/optPath/Gen{gen}/gbest'):
        os.mkdir(f'{filePath}/optPath/Gen{gen}/gbest')
    for particle in range(1, population + 1):
        if not os.path.isdir(f'{filePath}/optPath/Gen{gen}/p{particle}'):
            os.mkdir(f'{filePath}/optPath/Gen{gen}/p{particle}')
        if not os.path.isdir(f'{filePath}/optPath/Gen{gen}/p{particle}/pbest'):
            os.mkdir(f'{filePath}/optPath/Gen{gen}/p{particle}/pbest')

print("Optimization Path setting complete.")