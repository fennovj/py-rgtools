from rgtools.raw.buildings import get_buildings


class Buildings():

    # Class for saving and retrieving building information
    # The end goal is to calculate building production

    def __init__(self, save):
        self.quantities = {}
        self.production = {}
        self.buildings_raw = get_buildings()

        for building in save['buildings']:
            self.quantities[building['id']] = building['q']

        # Before applying upgrades, set the production to the base production
        for key in self.buildings_raw:
            self.production[key] = self.buildings_raw[key]['base_production']

    def building_production(self):
        production = 0
        for key in self.quantities:
            production += self.quantities[key] * self.production[key]
        return production


if __name__ == '__main__':
    from rgtools.save import read_json, read_save
    #save = read_json('saves/json/r1_brandnew.json')
    save = read_save('saves/txt/tmp.txt')
    buildings = Buildings(save)
    print(buildings.building_production())