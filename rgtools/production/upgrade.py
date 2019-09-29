
class Upgrade():

    # Class for saving and retrieving building information
    # The end goal is to calculate building production

    def __init__(self, inputs, outputs, func, type, id=None, name=None):
        '''
        Create a representation for an upgrade
        :param inputs: String, or list of strings that represent the inputs for the upgrade
        :param outputs: String, or list of strings that represent the outputs of the upgrade
        :param func: Function that, given the inputs, calculates the outputs
        :param type: Type of the upgrade. Either 'additive' or 'percent'
        :param id: Optionally, the id of the upgrade in the save file
        :param name: Optionally, the name of the upgrade
        '''

        self.inputs = inputs
        self.outputs = outputs
        self.func = func
        self.type = type
        self.id = id
        self.name = name

        