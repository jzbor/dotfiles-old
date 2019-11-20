#! /usr/bin/env python3

import argparse
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


def load_config(name):
    attr = {}
    file = open(os.path.join(dev_dir, name))
    for l in file.readlines():
        if l[0] == '#':
            try:
                k, v = l.split()
                attr[k] = v
            except ValueError:
                # If a line does not contain enough arguments
                pass
    return attr


def replace_in_dir(target, k, v):
    # !!! DANGER ZONE !!!
    # find $dotfiledir -type f | xargs sed -i "s/$conf_value_def/$conf_value/g"
    find_process = subprocess.Popen('find {} -type f'.format(target)\
                               .split(), stdout=subprocess.PIPE)
    sed_process = subprocess.Popen('xargs sed -i "s/{}/{}/g"'.format(k, v).split(),\
                                   stdout=subprocess.PIPE, stdin=find_process.stdout)
    find_process.stdout.close()
    output, error = sed_process.communicate()



def apply_devconf(name):
    default_config = load_config('default')
    target_config = load_config(name)

    for k in default_config.keys():
        replace_in_dir(default_config[k], target_config[k])



def git_init(path):
    git_process = subprocess.Popen('git -C {} init'.format(path).split(),\
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return git_process.communicate()


def git_add(path):
    git_process = subprocess.Popen('git -C {} add -A'.format(path).split(),\
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return git_process.communicate()


def git_commit(path, message):
    git_process = subprocess.Popen('git -C {} commit -m {}'.format(path, message).split(),\
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return git_process.communicate()


def git_push(path):
    git_process = subprocess.Popen('git -C {} push'.format(path).split(),\
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return git_process.communicate()


def git_pull(path):
    git_process = subprocess.Popen('git -C {} pull'.format(path).split(),\
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
    print()
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
    print()
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

    print('Loading bricks')
    # @TODO tempdir necessary?
    print('\tCreating tempdir')
    tempdir='/tmp/build_cfg/'
    if os.path.exists(tempdir):
        shutil.rmtree(tempdir)
    os.makedirs(tempdir)

    print('\tCopying \'default\' brick to destination')
    try:
        shutil.copytree(os.path.join(brick_dir, 'default'), target_dir, dirs_exist_ok=True)
    except TypeError:
        # < python 3.8
        copytree(os.path.join(brick_dir, 'default'), target_dir)

    for b in bricks:
        print('Copying \'{}\' brick to destination'.format(b))
        try:
            shutil.copytree(os.path.join(brick_dir, b), target_dir, dirs_exist_ok=True)
        except TypeError:
            # < python 3.8
            copytree(os.path.join(brick_dir, b), target_dir)

    print('Loading device config: {}'.format(device))
    apply_devconf(device)

    # Cleaning up
    shutil.rmtree(tempdir)


def parse_args():
    parser = argparse.ArgumentParser(description='Building and loading configs from the repo')
    parser.add_argument('-H', help='takes the users home as target directory',\
                        action='store_true', dest='home')
    parser.add_argument('-d', help='specify target path', nargs=1, type=str,\
                        dest='dest')
    parser.add_argument('-g', help='creates a git repository in the target directory',\
                        action='store_true', dest='git')
    parser.add_argument('-u', help='updates the dotfile repo via \'git pull\'',\
                        action='store_true', dest='update')
    parser.add_argument('-p', help='tries to push changes if the target is a git repo\
                        (requires -g)', action='store_true', dest='push')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.update:
        print('=== Updating Repository ===\n')
        out, err = git_pull(script_dir)
        if out:
            print(out.decode())
        if err:
            print(err.decode())
        print('\n')

    # @TODO If statement working on args.dest[0]?
    if args.home or args.dest:
        if args.home:
            dest = os.environ['HOME']
        else:
            dest = args.dest[0]
        print('=== Select Your Configuration ===\n')
        bricks = choose_bricks()
        dev = choose_device()
        print('\n')
        print('=== Building the Configuration ===\n')
        build_to_dir(bricks, dev, dest)
        print('\n')
        if args.git:
            print('=== Handling Git Arguments ===\n')
            if os.path.exists(os.path.join(dest, '.git')):
                print('=> Git add')
                out, err = git_add(dest)
                if out:
                    print(out.decode())
                if err:
                    print(err.decode())
            else:
                print('=> Git init')
                out, err = git_init(dest)
                if out:
                    print(out.decode())
                if err:
                    print(err.decode())
                print('=> Git add')
                out, err = git_add(dest)
                if out:
                    print(out.decode())
                if err:
                    print(err.decode())
            print('=> Git commit')
            out, err = git_commit(dest, 'New configs')
            if out:
                print(out.decode())
            if err:
                print(err.decode())

            if args.push:
                print('=> Git push')
                out, err = git_push(dest)
                if out:
                    print(out.decode())
                if err:
                    print(err.decode())
        print('Done')
    else:
        print('No target directory specified. Use -H or -d to define a destination or -h for help.')


