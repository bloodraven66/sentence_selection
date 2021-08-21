import os
import yaml
from attrdict import AttrDict

def read_yaml(args):

    config_file = os.path.join(args.config_folder, args.method+'.yaml')

    assert os.path.exists(config_file), \
        f'Config file {config_file} does not exist'

    with open(config_file) as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
        
    return AttrDict({**config, **vars(args)})
