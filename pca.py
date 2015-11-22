import configparser
config = configparser.ConfigParser()

config.read('data/Alligator_Hatchling_1_.pca')

def ConfigSectionMap(section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


averaging = ConfigSectionMap('CalibValue')['averaging']
skip = ConfigSectionMap('CalibValue')['skip']
timingVal = ConfigSectionMap('Detector')['timingval']
current = ConfigSectionMap('Xray')['current']
voxX = ConfigSectionMap('Geometry')['voxelsizex']
voxY = ConfigSectionMap('Geometry')['voxelsizey']

d = dict(averaging = averaging, skip = skip, timingVal = timingVal, current = current, voxX = voxX, voxY = voxY)
print(d)