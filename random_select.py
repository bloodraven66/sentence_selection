from common import *
import librosa
import random
from tqdm import tqdm

def start(dct, cfg, audio_files=None, aud_dur_dct=None):
    if audio_files is None and aud_dur_dct is None:
        raise Exception('Audio duration not accessible. Exiting..')
    required_duration = cfg.dur_in_hours
    print(f'Starting {required_duration} hr selection with {cfg.method} selection method')
    print('-'*80)
    required_duration = required_duration*60*60
    keys = list(dct.keys())
    values = list(dct.values())
    collected_duration, collected_sentences, collected_keys  = [], [], []
    print('Total Data Entropy:', entropy(values))
    with tqdm(total=int(required_duration)) as pbar:
        while sum(collected_duration) < required_duration:
            randNkey = random.choice(keys)
            triphones = dct[randNkey]
            collected_sentences.append(triphones)
            keys.remove(randNkey)
            collected_keys.append(randNkey)
            if aud_dur_dct is None:
                y, sr = librosa.load(audio_files[randNkey])
                dur = len(y)/sr
            else:
                dur = aud_dur_dct[randNkey]
            collected_duration.append(dur)
            pbar.set_description(f'ent:{str(round(entropy(collected_sentences), 2))}, num:{len(collected_sentences)}')
            pbar.update(collected_duration[-1])

    return {
            'sentences':collected_sentences,
            'keys':collected_keys,
            'durations':collected_duration
            }
