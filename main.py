from rgtools.save import read_save


def read_write(fname):
    outname = 'saves/json/' + fname + '.json'
    fname = 'saves/txt/' + fname + '.txt'
    save = read_save(fname)
    save.write(outname, pretty=True)
    return save


save = read_write('r133_recent')

#print([x['u2'] for x in save['trophies']])
print(save.get('stats/15/stats'))
print(save.get('trophies/_len'))
print(len(save['trophies']))