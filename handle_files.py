import pickle
import numpy as np
import os
from pathlib import Path

def load_file(args):
    filename = args.triphone_file
    if not os.path.exists(filename):
        raise Exception(f'path for {filename} does not exist')

    if filename.endswith('.pkl'):
        dct = load_pickle(filename)

    else:
        raise Exception(f'extension for {filename} not supported.')

    if args.save_path is None:
        raise Exception(f'Specify folder to store results in <save-path>')

    if not os.path.exists(args.save_path):
        raise Exception(f'path for <{args.save_path}> does not exist')

    if args.method != 'random':
        assert args.mode in ['uniform', 'skewed'], \
            f'Please provide a valid method to use! Choices: [uniform, skewed]'

    selected_audio_files = validate_audio(dct, args)
    audio_dur_dct = None
    if args.audio_dur_file is not None:

        raise NotImplementedError #load audiodict
    return dct, selected_audio_files, audio_dur_dct


def load_pickle(filename):
    try:
        with open(filename, 'rb') as handle:
             dct = pickle.load(handle)
    except:
        raise Exception(f'Unable to load pickle file {filename}')
    return dct

def store_pickle(data, filename):
    try:
        with open(filename, 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    except:
        raise Exception(f'Unable to store pickle file {filename}')

def validate_audio(dct, args):
    if not os.path.exists(args.audio_path):
        raise Exception(f'Audio path, {args.audio_path} does not exist')

    if isinstance(args.audio_extn, list):
        raise Exception(f'Multiple audio extensions in {args.audio_extn} not supported')

    audio_files = get_file_paths(args.audio_path, args.audio_extn)
    accepted_count = [1 if file_.stem in dct.keys() else 0 for file_ in audio_files]
    print('')
    if sum(accepted_count) == len(dct):
        print('Triphones for all audio files present')
    else:
        print(f'{sum(accepted_count)} sentence-audio pair found in {len(dct)} sentences & {len(audio_files)} audio files')

    if args.audio_dur_file is None:
        selected_audio_files = {}
        for i in range(len(audio_files)):
            if accepted_count[i] == 1:
                selected_audio_files[audio_files[i].stem] = audio_files[i]
    else:
        selected_audio_files = None
    return selected_audio_files

def get_file_paths(path, extension):
    path = Path(path).expanduser().resolve()
    return list(path.rglob(f'*{extension}'))
