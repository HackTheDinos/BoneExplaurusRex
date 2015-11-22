import configparser
config = configparser.ConfigParser()

config.read('data/Alligator_Hatchling_1_.pca')


def parse_config(config, section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


averaging = parse_config('CalibValue')['averaging']
skip = parse_config('CalibValue')['skip']
timingVal = parse_config('Detector')['timingval']
current = parse_config('Xray')['current']
voxX = parse_config('Geometry')['voxelsizex']
voxY = parse_config('Geometry')['voxelsizey']
