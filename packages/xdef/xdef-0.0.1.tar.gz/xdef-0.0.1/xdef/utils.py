import random
import pandas as pd
import os.path as osp
import re
import os
import json
import numpy as np
from glob import glob
import collections
import math
from functools import partial

zh_re = re.compile('[\u4e00-\u9fa5]')


def read_json(file):
    with open(file, 'r', encoding='rb') as f:
        return json.load(f)


def write_json(file, path):
    with open(path, 'wb') as f:
        json.dump(file, f)


def read_json_lines(file, lazy=False):
    if lazy:
        return (json.loads(line) for line in open(file, 'r', encoding='utf-8'))
    return [json.loads(x) for x in open(file, encoding='utf-8')]


def write_json_line(line, f):
    line = json.dumps(line, ensure_ascii=False) + '\n'
    f.write(line)


def write_json_lines(lines, path, mode='w+'):
    with open(path, mode, encoding='utf-8') as f:
        for line in lines:
            line = json.dumps(line, ensure_ascii=False) + '\n'
            f.write(line)


def random_split_list(data, frac=0.8, random_state=None):
    if random_state is None:
        random.seed(random_state)
    random.shuffle(data)
    return data[:int(len(data) * frac)], data[int(len(data) * frac):]


def kfold_split_json_lines(lines, folds, output_dir, key=None, use_value=False, pre_key=None, overwrite=True):
    check_dir(output_dir, overwrite)

    new_lines = []
    for line in lines:
        tmp = line if pre_key is None else line[pre_key]
        if key is not None:
            gp_key = tmp[key]
        else:
            gp_key = list(tmp.keys())[0]
        new_lines.append({'gp_key': gp_key, 'data': line})
    df = pd.DataFrame(new_lines)
    for _, df_gp in df.groupby('gp_key'):
        fold_idx = list(range(folds)) * (len(df_gp) // folds + 1)
        df_gp['fold'] = fold_idx[:len(df_gp)]
        for i in range(folds):
            train = df_gp[df_gp.fold != i]
            dev = df_gp[df_gp.fold == i]
            train_lines = train.data
            dev_lines = dev.data
            write_json_lines(train_lines, osp.join(output_dir, 'train{}.json', ).format(i), 'a+')
            write_json_lines(dev_lines, osp.join(output_dir, 'dev{}.json').format(i), 'a+')


def stratified_sampling(df, by, test_frac=None, test_num=None, random_state=None):
    df.index = range(len(df))
    test_idx = []
    if test_num:
        test_frac = test_num / df.shape[0]
    for by, df_gp in df.groupby(by):
        test_idx += list(df_gp.sample(frac=test_frac, random_state=random_state).index)
    test = df[df.index.isin(test_idx)]
    train = df[~df.index.isin(test_idx)]
    return train, test


def sequence_padding(inputs, length=None, value=0, seq_dims=1, mode='post', dtype='int64'):
    if length is None:
        length = np.max([np.shape(x)[:seq_dims] for x in inputs], axis=0)
    elif not hasattr(length, '__getitem__'):
        length = [length]

    slices = [np.s_[:length[i]] for i in range(seq_dims)]
    slices = tuple(slices) if len(slices) > 1 else slices[0]
    pad_width = [(0, 0) for _ in np.shape(inputs[0])]

    outputs = []
    for x in inputs:
        x = x[slices]
        for i in range(seq_dims):
            if mode == 'post':
                pad_width[i] = (0, length[i] - np.shape(x)[i])
            elif mode == 'pre':
                pad_width[i] = (length[i] - np.shape(x)[i], 0)
            else:
                raise ValueError('"mode" argument must be "post" or "pre".')
        x = np.pad(x, pad_width, 'constant', constant_values=value)
        outputs.append(x)
    return np.array(outputs, dtype=dtype)


class AverageMeter:
    def __init__(self):
        self.total = 0
        self.n = 0

    def update(self, item):
        self.total += item
        self.n += 1

    def accumulate(self):
        return self.total / self.n

    def reset(self):
        self.total = 0
        self.n = 0


def print_item(alist):
    for i in alist:
        print(i)


def label2id(alist):
    alist = sorted(set(alist))
    return dict(zip(alist, range(len(alist))))


def has_zh(s):
    return zh_re.search(s)


def check_dir(out_dir, overwrite=False):
    if osp.exists(out_dir) and overwrite:
        import shutil
        shutil.rmtree(out_dir)
    if not osp.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)


if __name__ == '__main__':
    x1 = np.random.randn(3, 3)
    x2 = np.random.randn(4, 4)
    x3 = sequence_padding([x1, x2], seq_dims=2)
    print(x3.shape)
