# Sims4SlowGrowthMod

A mod that grows all female sims (height and chest size) over time.

## How to use

Note: this works with the base game, but other mods are needed first.

1. Download dependent mods:
    - [Height slider](https://modthesims.info/d/588159/height-slider.html). I downloaded the `1515` version since Sims 4 Studio allows for easy editing of the max height (see farther down on this page for how to do that).
    - [Breast augmentation](https://modthesims.info/d/536790/breast-augmentation.html). I downloaded the `222` version. This technically isn't _necessary_, but if you stumbled on this page, then you probably want this mod.
1. Download all Python files from this repo and save them to **a subfolder** in your Sims 4 mods folder. On Windows, this is `%userprofile%\Documents\Electronic Arts\The Sims 4\Mods`. The final path of those files should look something like this: `C:\Users\your_name\Documents\Electronic Arts\The Sims 4\Mods\SlowGrowth\main.py`.
1. Launch The Sims 4, go to Game Options, then Other, then check "Script Mods Allowed" (and restart The Sims 4).
1. Press ctrl+shift+C to open the cheat console and type `s`. Any time you travel in the game, enter the character editor, or restart the game, you'll need to perform this step again.

You should see messages indicating that it initialized successfully.

## How it works

- You type `s` to initialize the mod. Males get an assigned height of 0 (i.e. the standard size of roughly 6 ft. or 183 cm.) and a growth of 0. Females get a height of -30 (roughly 5 ft. or 152 cm.) and a random growth rate.
- Every 30 in-game minutes, a "tick" occurs.
- Every tick, all sims grow according to their growth rates. Males are set to 0, so they don't grow.
- Every tick, females have a chance of increasing in growth rate up to a certain limit. This is called "auto-blessing".

## Other usage notes

### Editing Python files with the game open

This is highly recommended since I didn't spend any time addressing usability, so you'll probably be editing these files a lot to get things how you like them.

If you want to edit the values of the mod yourself without having to keep reloading the game, follow [these steps](https://medium.com/swlh/the-sims-4-modern-python-modding-part-5-project-template-c9ffee48ab4e). By doing this, you'll be able to type `devmode.reload name_of_script`, e.g. `devmode.reload main` or `devmode.reload size_tracker`.

### Commands

These come from `main.py`:

- `s`: **s**tart the mod. It'll read the sizes of each sim from a file on disk and set up the logger. If you're not seeing output, try running `save` followed by `s`.
- `save`: save the sizes of each sim to disk. You can then edit this file to customize height, chest, or growth rates.
- `fast <sim's first name>`: grow a sim much faster than normal. In addition to the normal growth every 30 minutes, the sim will get extra growth every 5 minutes.
- `tick [num_times=1]`: cause `num_times` growth ticks to occur.
- `wipe`: wipe out all sizes of all sims. Any sims in the current zone will have their models reset. Any not in the current zone won't have their models reset until the next tick. Invoke `tick` manually when you see them to fix this.
- `bless <sim's first name> [times=4]`: it's like `tick` but only for a specific sim.
- `chest <sim's first name> [times=4]`: adds `times` to the chest value. This scale goes from -100 to 100.
- `blessrate <sim's first name> [times=2]`: multiplies the sim's growth rate by `times`. This gets automatically reset back to a cap whenever a sim is "auto-blessed".

### Camera modes

- Pressing `tab` enters a free-roam camera mode. WASD will move, Q and E will change heights. Holding shift will doing those will increase their speed.
- Shift+tab enters first-person camera. If you launch through Steam, then you'll need to change the Steam hotkey to activate this.

### Updating the max height of the height-slider mod

1. Download [Sims 4 Studio](https://sims4studio.com/thread/1523/downloading-sims-4-studio).
1. Click the "My Projects" button on the main page, then open the `.package` file of the height-slider mod.
1. Depending on the variant of the mod you got, you may or may not have a Bone Pose for `Instance==5773388F834E4180`. If you don't, then try another variant. If you do, then click "Edit Items..." in the right-hand panel and change the scale to something like `0.6,0.6,0.6`. That's _roughly_ ten feet, which is the ceiling height of a single floor in a house. I set mine to `12,12,12` and just control the height in a more fine-tuned way through code.

### Ridiculous proportions

The extremes of most of these mods look ridiculous. Animations will look messed up with even minor height changes.

### Other nice mods

- [Height chart](https://modthesims.info/d/656665/height-chart.html): it's just a wallpaper that you can apply in Build Mode with metric/imperial markings.

## Miscellaneous development notes

- `ts4script` files are simply zipped archives. They typically have `.pyc` files (compiled Python). Python can be decompiled with [`decompyle3`](https://pypi.org/project/decompyle3/), [`unpyc3`](https://github.com/figment/unpyc3), or [`uncompyle6`](https://pypi.org/project/uncompyle6/). It's not always successful.
- Python 3.7 is used for everything. Don't try other Python versions.
- These were some helpful snippets for getting started with scripting:
  - <https://lot51.cc/snippets>
  - <https://github.com/LuquanLi/TheSims4ScriptModBuilder>
- I do not plan on improving this mod, adding features, making it easier to use, etc. I hope someone enjoys it (but this is a throwaway account and I probably won't check on it for a long time).
- I hate using "male" and "female" to refer to sims, but that's the terminology that's used everywhere.
