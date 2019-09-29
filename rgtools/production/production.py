from rgtools.save import RealmGrinderSave
import json
# Given a save, try to calculate production
# We start with a very simple save in R0

if __name__ == '__main__':
    fname = 'saves/json/r1_brandnew.json'
    save = json.loads(open(fname, 'r').read())
    save = RealmGrinderSave(save=save)
    print(save)