from common import *
import random
from tqdm import tqdm

def start(dct, cfg, audio_files=None, aud_dur_dct=None):
    required_duration = cfg.dur_in_hours
    mode = cfg.mode
    keys = list(dct.keys())
    values = list(dct.values())
    collected_duration, collected_sentences, collected_keys  = [], [], []
    reject_steps, reject_step_keys = [], []
    print(f'Starting {required_duration} hr selection with {cfg.method} selection')
    print('-'*80)
    required_duration = required_duration*60*60

    print('Total Data Entropy:', entropy(dct.values()))
    with tqdm(total=int(required_duration)) as pbar:
        while sum(collected_duration) < required_duration:
            randn_key = random.choice(keys)
            triphones = dct[randn_key]
            sent = collected_sentences + [randn_key]
            if mode == 'uniform':
                old_ent = entropy(collected_sentences)
                ent = entropy(sent)
            elif mode == 'skewed':
                old_ent = entropy(sent)
                ent = entropy(collected_sentences)
            criterion = ent - old_ent
            formula = criterion > 0
            if formula:
                keys.remove(randn_key)
                collected_keys.append(randn_key)
                collected_sentences.append(triphones)
                collected_duration.append(aud_dur_dct[randn_key])
                pbar.set_description(f'ent:{str(round(entropy(collected_sentences), 2))}, num:{len(collected_sentences)}, reject:{len(reject_steps)}')
                reject_steps, reject_step_keys = [], []
                pbar.update(collected_duration[-1])
            else:
                reject_steps.append(criterion)
                reject_step_keys.append(randn_key)
                if len(reject_steps)>cfg.num_reject_skip:
                    idx = reject_steps.index(max(reject_steps))
                    some_key = reject_step_keys[idx]
                    reject_steps, reject_step_keys = [], []
                    keys.remove(some_key)
                    collected_keys.append(some_key)
                    collected_sentences.append(dct[some_key])
                    collected_duration.append(aud_dur_dct[some_key])
                    pbar.update(collected_duration[-1])
                pbar.set_description(f'ent:{str(round(entropy(collected_sentences), 2))}, num:{len(collected_sentences)}, reject:{len(reject_steps)}')

    return {
            'sentences':collected_sentences,
            'keys':collected_keys,
            'durations':collected_duration
            }
