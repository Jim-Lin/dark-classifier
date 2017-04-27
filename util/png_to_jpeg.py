#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
from PIL import Image
from multiprocessing import Pool
from functools import partial

def convert(dir_from_sub, dir_to_sub, file):
    file_from = os.path.join(dir_from_sub, file)
    filename = os.path.splitext(file)[0]
    file_to = os.path.join(dir_to_sub, filename + ".jpg")
    if not os.path.exists(file_to):
        im = Image.open(file_from)
        im.convert('RGB').save(file_to, 'JPEG')
        print file_to

def main(args):
    dir_from = args.dir_from
    dir_to = args.dir_to
    if not os.path.exists(dir_to):
        os.makedirs(dir_to)

    ids = [f for f in os.listdir(dir_from) if not f.startswith('.') and f.find('.t7') == -1]
    for actress_id in ids:
        dir_from_sub = os.path.join(dir_from, actress_id)
        files = [f for f in os.listdir(dir_from_sub) if not f.startswith('.')]
        if len(files) >= 20:
            dir_to_sub = os.path.join(dir_to, actress_id)
            if not os.path.exists(dir_to_sub):
                os.makedirs(dir_to_sub)

            func = partial(convert, dir_from_sub, dir_to_sub)
            pool = Pool()
            pool.map(func, files)
            pool.close()
            pool.join()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dir_from',
        type=str,
        help='png dir',
        required=True
    )
    parser.add_argument(
        '--dir_to',
        type=str,
        help='jpeg dir',
        required=True
    )

    args = parser.parse_args()
    main(args)
