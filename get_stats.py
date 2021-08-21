import numpy as np

def execute(dct, status):
    if status is not True:
        return None
    if not isinstance(dct, dict):
        print('computing stats not implemented for <dict>. Skipped.')
        return None
    print('-'*80)
    print('Number of keys (sentences): ', len(dct))
    triphones = list(dct.values())
    lengths = [len(i) for i in triphones]
    sum_ = sum(lengths)
    avg_ = np.mean(lengths)
    std_ = np.std(lengths)

    count = {}
    for sent in triphones:
        for id in sent:
            count[id] = count.get(id, 0) + 1

    print(f'Total triphones: {sum_: ,}')
    print(f'Average triphones per sentence: {avg_:.2f}({std_:.2f})')
    print(f'Number of unique triphones: {len(count): ,}')
    print('-'*80)
