#! /usr/bin/env python3

import os
import os.path
import shutil
import subprocess

script_dir=os.path.dirname(os.path.abspath(__file__))+'/'
brick_dir=script_dir+'bricks/'
dev_dir=script_dir+'dev_configs/'

def get_available_bricks():
    """Return all available bricks with clear assigned numbers (dict/list)"""

    ls_process = subprocess.Popen('ls -1 {}'.format(brick_dir)\
                               .split(), stdout=subprocess.PIPE)
    sed_process = subprocess.Popen('sed /default/d'.split(), stdout=subprocess.PIPE,\
                                   stdin=ls_process.stdout)
    ls_process.stdout.close()
    nl_process = subprocess.Popen('nl -n ln'.split(), stdout=subprocess.PIPE,\
                                  stdin=sed_process.stdout)
    sed_process.stdout.close()
    output, error = nl_process.communicate()

    available_bricks = {}
    for line in output.decode().splitlines():
        n, b = line.split()
        available_bricks[n] = b

    return available_bricks


def parse_bricks(user_input, available_bricks):
    bricks = []
    for e in user_input.split():
        if (e.isupper() or e.islower()) and (e in available_bricks.values()):
            bricks.append(e)
        elif e.isdigit() and int(e) <= len(available_bricks.values()):
            bricks.append(available_bricks[e])
        else:
            return False
    return bricks


def get_available_devices():
    """Return all available devices with clear assigned numbers (dict/list)"""

    find_process = subprocess.Popen('find {} -mindepth 1 -maxdepth 1 -type f -printf %f\\n'\
                                  .format(dev_dir).split(),\
                                    stdout=subprocess.PIPE)
    nl_process = subprocess.Popen('nl -n ln'.split(), stdout=subprocess.PIPE,\
                                  stdin=find_process.stdout)
    find_process.stdout.close()
    output, error = nl_process.communicate()

    available_devices = {}
    for line in output.decode().splitlines():
        n, b = line.split()
        available_devices[n] = b

    return available_devices



def parse_device(user_input, available_devices):
    if ' ' in user_input:
        return False
    elif (user_input.isupper() or user_input.islower()) and (user_input in available_devices.values()):
        return user_input
    elif user_input.isdigit() and int(user_input) <= len(available_devices.values()):
        return available_devices[user_input]
    else:
        return False


def copytree(src, dst):
    # According to https://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth#12514470
    # Deprecated in python 3.8+
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d)
        else:
            shutil.copy2(s, d)



def init_git(path):
    git_process = subprocess.Popen('git -C {} init'.format(path).split(),\
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return git_process.communicate()


def add_git(path):
    git_process = subprocess.Popen('git -C {} add -A'.format(path).split(),\
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return git_process.communicate()


def commit_git(path, message):
    git_process = subprocess.Popen('git -C {} commit -m {}'.format(path, message).split(),\
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return git_process.communicate()


def push_git(path):
    git_process = subprocess.Popen('git -C {} push'.format(path).split(),\
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return git_process.communicate()


# From here on the methods are for workspace rather than help methods

def choose_bricks():
    """Present the user with a selection interface for the bricks
    and return selected bricks in given order
    """
    bricks = []
    available_bricks = get_available_bricks()

    for k in available_bricks.keys():
        print("{}\t{}".format(k, available_bricks[k]))

    print("Select multiple bricks (number/name) in the order you would like to have them applied")
    user_selection = input('> ')
    bricks = parse_bricks(user_selection, available_bricks)

    if not bricks:
        print()
        print("That is not a valid input!")
        print("Please correct your selection...")
        print()
        return choose_bricks()
    else:
        return bricks


def choose_device():
    """Present the user with a selection interface for the devices
    and return selected target device
    """
    available_devices = get_available_devices()

    for k in available_devices.keys():
        print("{}\t{}".format(k, available_devices[k]))

    print("Select your target device (number/name) from the list")
    user_selection = input('> ')
    device = parse_device(user_selection, available_devices)

    if not device:
        print()
        print("That is not a valid input!")
        print("Please correct your selection...")
        print()
        return choose_device()
    else:
        return device
    pass


def save_config(bricks, device, options):
    """Save bricks, device and maybe even options to file for reuse"""
    pass


def build_to_dir(bricks, device, target_dir=os.environ['HOME'], git=False, push=False):
    """Actually build the configuraion"""
    tempdir='/tmp/build_cfg/'
    if os.path.exists(tempdir):
        shutil.rmtree(tempdir)
    os.makedirs(tempdir)

    try:
        shutil.copytree(os.path.join(brick_dir, 'default'), target_dir, dirs_exist_ok=True)
    except TypeError:
        # < python 3.8
        copytree(os.path.join(brick_dir, 'default'), target_dir)


    for b in bricks:
        try:
            shutil.copytree(os.path.join(brick_dir, b), target_dir, dirs_exist_ok=True)
        except TypeError:
            # < python 3.8
            copytree(os.path.join(brick_dir, b), target_dir)

    # Cleaning up
    shutil.rmtree(tempdir)

    pass


if __name__ == "__main__":
    bricks = choose_bricks()
    dev = choose_device()
    build_to_dir(bricks, dev, '/home/jzbor/test')


