from common import *
import random
from tqdm import tqdm

def limitter(
            cfg,
            sorted_tri,
            tri_key_save,
            collected_keys,
            collected_sentences,
            all_keys,
            all_collected_sentences,
            dct, collected_duration,
            collected_duration_lim,
            limit,
            aud_dur_dct,
            parse_mode='current'
            ):

    thsiLimkeys = []
    for (c, cc) in sorted_tri:
        if cc <= limit:
            if tri_key_save[c][0] not in all_keys+collected_keys:
                thsiLimkeys.append(tri_key_save[c][0])
                all_keys.append(tri_key_save[c][0])
                all_collected_sentences.append(dct[tri_key_save[c][0]])

    if len(all_keys+collected_keys) != len(set(all_keys+collected_keys)):
        print('Duplicates')
        exit()
    reject = 0
    if parse_mode=='current':
        if len(thsiLimkeys) == 0:
            return all_keys, all_collected_sentences, collected_keys, collected_sentences, collected_duration

    # with tqdm(total=int(collected_duration_lim)) as pbar:
    while sum(collected_duration) < collected_duration_lim:
            if parse_mode == 'all':
                randNkey = random.choice(all_keys)
            elif parse_mode == 'current':
                if len(thsiLimkeys)==0:
                    break
                randNkey = random.choice(thsiLimkeys)

            else:
                raise NotImplementedError
            triphones = dct[randNkey]
            sent = collected_sentences + [triphones]
            criterion = entropy(sent)-entropy(collected_sentences)
            if criterion>0:
                reject = 0
                all_keys.remove(randNkey)
                if parse_mode == 'current':
                    thsiLimkeys.remove(randNkey)
                collected_keys.append(randNkey)
                collected_sentences.append(triphones)
                collected_duration.append(aud_dur_dct[randNkey])
            else:
                reject += 1
            if reject>cfg.num_reject_skip_low:
                break
    return all_keys, all_collected_sentences, collected_keys, collected_sentences, collected_duration


def Diff(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))

def start(dct, cfg, audio_files=None, aud_dur_dct=None):
    required_duration = cfg.dur_in_hours
    mode = cfg.mode
    print(f'Starting {required_duration} hr selection with {cfg.method} selection method')
    print('-'*80)
    keys = list(dct.keys())
    values = list(dct.values())
    count_dct = {}
    tri_key_save = {}
    all_keys = set()
    required_duration = required_duration*60*60
    for i in range(len(values)):
        for tri in values[i]:
            if tri in count_dct:
                count_dct[tri] +=1
                tri_key_save[tri].append(keys[i])
            else:
                count_dct[tri] = 1
                tri_key_save[tri] = [keys[i]]
    sorted_tri = sorted(count_dct.items(), key=lambda x: x[1])

    collected_duration, collected_sentences, collected_keys  = [], [], []
    all_sentences, all_keys = [], []
    print(f'Starting with sentences with 1, 2, ... , {cfg.low_limit} triphone counts')
    for limit in range(1, cfg.low_limit):
        (
        all_keys,
        all_sentences,
        collected_keys,
        collected_sentences,
        collected_duration
        ) = limitter(
                    cfg,
                    sorted_tri,
                    tri_key_save,
                    collected_keys,
                    collected_sentences,
                    all_keys,
                    all_sentences,
                    dct,
                    collected_duration,
                    required_duration,
                    limit,
                    aud_dur_dct
                    )
        if sum(collected_duration)>required_duration:
            print(f'Entropy: {entropy(collected_sentences)}')
            break
        if limit % cfg.low_mix_intervel == 0:
            (
            all_keys,
            all_sentences,
            collected_keys,
            collected_sentences,
            dur
            )= limitter(
                        cfg,
                        sorted_tri,
                        tri_key_save,
                        collected_keys,
                        collected_sentences,
                        all_keys,
                        all_sentences,
                        dct,
                        collected_duration,
                        required_duration,
                        limit,
                        aud_dur_dct,
                        parse_mode='all'
                        )

        print(f'{limit}= Num_sentences: {len(collected_sentences)}, Duration: {sum(collected_duration)/(60*60):.2f}, Entropy: {entropy(collected_sentences):.2f}')
    remaining_keys = Diff(keys, collected_keys)
    reject_list, reject_list_key = [], []
    if sum(collected_duration)<required_duration:
        print('-'*80)
        print(f'Low triphone based selection ended. Starting entropy criteria on remaining {(required_duration-sum(collected_duration))/(60*60):.2f} hours')
    with tqdm(total=int(required_duration)) as pbar:
        pbar.update(sum(collected_duration))
        while sum(collected_duration) < required_duration:
            randn_key = random.choice(remaining_keys)
            triphones = dct[randn_key]
            sent = collected_sentences + [triphones]
            criterion = entropy(sent)-entropy(collected_sentences)
            if criterion>0:
                reject_list, reject_list_key = [], []
                remaining_keys.remove(randn_key)
                collected_keys.append(randn_key)
                collected_sentences.append(triphones)
                collected_duration.append(aud_dur_dct[randn_key])
                pbar.set_description(f'ent:{str(round(entropy(collected_sentences), 2))}, num:{len(collected_sentences)}')
                pbar.update(collected_duration[-1])
            else:
                reject_list.append(criterion)
                reject_list_key.append(randn_key)

                if len(reject_list)>cfg.num_reject_skip:
                    idx = reject_list.index(max(reject_list))
                    some_key = reject_list_key[idx]
                    eject_list, reject_list_key = [], []
                    remaining_keys.remove(some_key)
                    collected_keys.append(some_key)
                    collected_sentences.append(dct[some_key])
                    collected_duration.append(aud_dur_dct[some_key])
                    pbar.update(collected_duration[-1])
    print(f'Entropy: {entropy(collected_sentences)}')

    return {
            'collected_sentences':collected_sentences,
            'keys':collected_keys,
            'collected_durationations':collected_duration
            }
