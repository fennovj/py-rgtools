from rgtools.rgsave import _apply_rule, RealmGrinderByteArray, RealmGrinderSave
from rgtools.resources import get_formats, decode_save

import json

with open('save.txt', 'r') as file:
    save = file.read()

rgdata = RealmGrinderByteArray(decode_save(save))
rgsave = RealmGrinderSave()

for rule in get_formats():
    # print("Now applying rule {}".format(rule))
    _apply_rule(rule, rgsave, rgdata)
    with open('save.json', 'w') as file:
        file.write(json.dumps(rgsave.save,
                              sort_keys=True,
                              indent=4,
                              separators=(',', ': ')))
