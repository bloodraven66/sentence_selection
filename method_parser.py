import os
from config_parser import read_yaml
import random_select
import random_group
import entropy_criteria
import triphone_priority
import numpy as np
import librosa
from tqdm import tqdm
from handle_files import load_pickle, store_pickle

def run(dct, args, audio_files, audio_dur_dct):
    method = args.method
    available_methods = [
                        'random_group',
                        'entropy_criteria',
                        'low_triphone_count_priority',
                        'random',
                        ]
    assert method in available_methods, \
        f'Please provide a valid method to use! Choices: {available_methods}'
    if method != 'random':
        args = read_yaml(args)
    selector = get_func(method)
    if audio_dur_dct is None:
        if method == 'random':
            print('Computing duration with Librosa')
        else:
            audio_dur_dct = cache_audio_dur(args, audio_files)
    collected_data = selector(dct, args, audio_files, audio_dur_dct)
    save(collected_data, args)


def get_func(method):

    if method == 'random_group':
        fn = random_group.start

    elif method == 'entropy_criteria':
        fn = entropy_criteria.start

    elif method == 'low_triphone_count_priority':
        fn = triphone_priority.start

    elif method == 'random':
        fn = random_select.start

    return fn

def cache_audio_dur(args, audio_files):

    if args.cache_audio_dur is None:
        raise Exception('Provide a path to cache durations in <cache-audio-dur>')
    aud_dur_path = os.path.join(args.cache_audio_dur, args.dataset_identifier, 'dur.pkl')
    if  os.path.exists(aud_dur_path) and args.override_caching == False:
        print(f'Loading durations cached at {aud_dur_path}')
        dct = load_pickle(aud_dur_path)
    else:
        print('Computing duration with Librosa')
        dct = {}
        for path in tqdm(audio_files):
            y, sr = librosa.load(audio_files[path])
            dct[path] = len(y)/sr
        if not os.path.exists(os.path.join(args.cache_audio_dur, args.dataset_identifier)):
            os.mkdir(os.path.join(args.cache_audio_dur, args.dataset_identifier))
        store_pickle(dct, aud_dur_path)
        print(f'Durations stored at {aud_dur_path}')
    return dct

def save(collected_data, args):
    print('-'*80)
    assert isinstance(collected_data, dict) and len(collected_data) == 3
    for key in collected_data:
        if not os.path.exists(os.path.join(args.save_path, args.dataset_identifier, args.method)):
            os.makedirs(os.path.join(args.save_path,args. dataset_identifier, args.method))
        if args.method == 'random':
            name = os.path.join(args.save_path, args.dataset_identifier, args.method, "_".join([key, str(args.dur_in_hours), 'hr.npy']))
        else:
            pass
            if not os.path.exists(os.path.join(args.save_path, args.dataset_identifier, args.method, args.mode)):
                os.makedirs(os.path.join(args.save_path, args.dataset_identifier, args.method, args.mode))
            name = os.path.join(args.save_path, args.dataset_identifier, args.method, args.mode, "_".join([key, str(args.dur_in_hours), 'hr.npy']))
        with open(name, 'wb') as f:
            np.save(f, np.array(collected_data[key], dtype=object))
        print(f'Results saved at {name}')
