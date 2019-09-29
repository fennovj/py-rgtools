from rgtools.save import read_save


def read_write(fname):
    outname = 'saves/json/' + fname + '.json'
    fname = 'saves/txt/' + fname + '.txt'
    save = read_save(fname)
    save.write(outname)
    return save


save = read_write('r133_recent')

for i in range(35, 41):
    print(i)
    print(save['stats'][i])
