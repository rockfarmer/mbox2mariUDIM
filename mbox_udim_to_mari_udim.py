# -*- coding:UTF-8 -*-
__author__ = 'zhaoxu'

import os
import sys
import re
import subprocess
import logging

MBOX_UDIM_COMP = re.compile('u\d_v\d')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def mbox2mari(dir_path):
    if not os.path.isdir(dir_path):
        logging.error('can\'t find {0}'.format(dir_path))
    mbox_tex_list = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and MBOX_UDIM_COMP.search(f)]

    for mbox_tex in mbox_tex_list:
        mbox_re = MBOX_UDIM_COMP.search(mbox_tex)
        mbox_part = mbox_tex[mbox_re.start(): mbox_re.end()]
        u = mbox_part.split('_')[0][1:]
        v = mbox_part.split('_')[1][1:]
        mari_part = '10{0}{1}'.format(u, v)
        mari_tex = mbox_tex.replace(mbox_part, mari_part)
        copy_file(os.path.join(dir_path, mbox_tex), os.path.join(dir_path, mari_tex))


def copy_file(source_file, target_file):
    diff_sep = '/' if os.sep == '\\' else '\\'
    source_file = source_file.replace(diff_sep, os.sep)
    target_file = target_file.replace(diff_sep, os.sep)

    logging.info('copy "{0}" to "{1}"'.format(source_file, target_file))

    if sys.platform == 'win32':
        subprocess.call('copy /y "{0}" "{1}"'.format(source_file, target_file), shell=True)
    else:
        subprocess.call('cp -f "{0}" "{1}"'.format(source_file, target_file), shell=True)


if __name__ == '__main__':
    try:
        input_path = sys.argv[1]
    except:
        input_path = '.'
    
    mbox2mari(input_path)
