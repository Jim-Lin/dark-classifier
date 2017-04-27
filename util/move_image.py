#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import os
import shutil

root = "/home/shuai/face/"
today = datetime.date.today().strftime('%Y-%m-%d')

root_training_images_today = root + today + "-training-images/"
root_training_images = root + "training-images/"

root_aligned_images_today = root + today + "-aligned-images/"
root_aligned_images = root + "aligned-images/"

def main(args):
    ids = [f for f in os.listdir(args[0]) if not f.startswith('.')]
    for actress_id in ids:
        dir_from = os.path.join(args[0], actress_id)
        dir_to = os.path.join(args[1], actress_id)

        files = [f for f in os.listdir(dir_from) if not f.startswith('.')]
        for file in files:
            file_from = os.path.join(dir_from, file)
            file_to = os.path.join(dir_to, file)
            shutil.move(file_from, file_to)
            print file_from
            print file_to

if __name__ == '__main__':
    if os.path.exists(root_training_images_today):
        main([root_training_images_today, root_training_images])
        shutil.rmtree(root_training_images_today)

    if os.path.exists(root_aligned_images_today):
        main([root_aligned_images_today, root_aligned_images])
        shutil.rmtree(root_aligned_images_today)
