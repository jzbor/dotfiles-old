# My Dotfiles

## Finding stuff
I know the repo can seem a little messy as it tries to provide multiple "themes" and versions of dotfiles.
If you are just looking for the basics here is a list that might help:

* [.vimrc](bricks/default/.vimrc)
* [i3/config](bricks/default/.config/i3/config)

## New Build Concept:
1. User chooses bricks in relevant order
2. User chooses device
3. Script saves config for later rebuild
4. Script builds into given dir
    1. If a .git folder exists the repo gets updated
    2. If there is no such folder a repo gets initialised in the folder
    3. The user wishes not to create a git repo

* Create config file for behavior like automatic pushing, repo creation etc.

