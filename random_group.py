from common import *
import librosa
import random
from tqdm import tqdm

def get_sents_from_group(group, dct, aud_dur_dct):
    return [dct[key] for key in group], [aud_dur_dct[key] for key in group]

def start(dct, cfg, audio_files=None, aud_dur_dct=None):
    required_duration = cfg.dur_in_hours
    num_groups = cfg.num_groups
    mode = cfg.mode

    print(f'Starting {required_duration} hr selection with {cfg.method} selection with {num_groups} groups')
    print('-'*80)
    required_duration = required_duration*60*60
    keys = list(dct.keys())
    random.shuffle(keys)
    grouped_keys = [keys[i::num_groups] for i in range(num_groups)]
    group_entropy = [entropy(get_sents_from_group(grouped_keys[i], dct, aud_dur_dct)[0]) for i in range(len(grouped_keys))]

    if mode == 'uniform':
        entropy_key = group_entropy.index(max(group_entropy))
        entropy_check = 0
    elif mode == 'skewed':
        entropy_key = group_entropy.index(min(group_entropy))
        entropy_check = 50
    collected_sentences, collected_duration = get_sents_from_group(grouped_keys[entropy_key], dct, aud_dur_dct)
    remove_list = [entropy_key]
    group_ids = [i for i in range(0, len(grouped_keys))]
    collected_keys = grouped_keys[entropy_key]

    print('Total Data Entropy:', entropy(dct.values()))
    with tqdm(total=int(required_duration)) as pbar:
        pbar.update(sum(collected_duration))
        while sum(collected_duration) < required_duration:

            group_entropy = [entropy(collected_sentences+get_sents_from_group(grouped_keys[i], dct, aud_dur_dct)[0]) if i not in remove_list else entropy_check for i in group_ids]

            if mode == 'uniform':
                entropy_key = group_entropy.index(max(group_entropy))
            elif mode == 'skewed':
                entropy_key = group_entropy.index(min(group_entropy))
            remove_list.append(entropy_key)
            new_sent, add_dur = get_sents_from_group(grouped_keys[entropy_key],dct, aud_dur_dct)
            collected_duration += add_dur
            collected_sentences += new_sent
            collected_keys += grouped_keys[entropy_key]
            pbar.set_description(f'ent:{str(round(group_entropy[entropy_key], 2))}, num:{len(collected_sentences)}')
            pbar.update(sum(add_dur))

    return {
            'sentences':collected_sentences,
            'keys':collected_keys,
            'durations':collected_duration
            }
