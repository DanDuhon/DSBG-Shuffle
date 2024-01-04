# DSBG-Shuffle
A program to shuffle the enemies in an encounter.  Allows new combinations of enemies that are not available officially.

The idea behind this program is to provide backwards and forwards compatibility for Dark Souls The Board Game.  When the new core sets came out, they made no references to the older content. The encounter design of the new core sets are much more interesting than the old design, and I believe people should be able to use their existing enemies in this new design (or bring new enemies into the older encounters as well).  That's what I aim to accomplish here.  Users should be able to select which core sets/expansions that contain enemies.  This will inform which encounters are available (more on that later).



## How to run/Installation
1. Go to [Releases](https://github.com/DanDuhon/DSBG-Shuffle/releases) and click on "Source code (zip)" or "Source code (tar.gz)", whichever archive format is your preference.
2. Inside the archive file is a folder called "DSBG-Shuffle-main".  Unzip this folder anywhere you want.
3. Open the folder, and run "DSBG-Shuffle.exe" inside it.  There isn't an installer (mostly because it's too big for GitHub), you just run the .exe.  If you're not running Windows, see the FAQ for workarounds for Mac/Linux.


## Roadmap
Beyond future expansions, I'm really not sure where to go from here.  Possibly a v2 campaign generator.


## FAQ
### Are you going to support future expansions/core sets?

Yes, as time allows.  The lion's share of work is done, but new enemies will have to be analyzed and the new encounter design tends to need some custom code to do correctly.

### Are you going to support fan-made content?

I'm willing, but only if there's interest in it.  If you know of some great fan-made content you want to see added, [please open an issue](https://github.com/DanDuhon/DSBG-Shuffle/issues) and I'll work on it!

### Can we add custom enemies/encounters ourselves?

No (unless you branch the code and do it yourself), and I don't intend to support that.  Calculating enemy strength and generating enemy combinations for an encounter can take hours depending on your machine and the size of the encounter.

### I found a bug!

Great!  If you can, reproduce it then find the log.txt file in the same folder as the .exe file.  Then [please open an issue](https://github.com/DanDuhon/DSBG-Shuffle/issues) and attach or paste in the log so I can investigate.

### Are you going to create a version for Mac/Linux/Android/iPhone/web?

There are a couple workaround options for Mac/Linux.
- The easy way: use [Wine](https://wiki.winehq.org/Main_Page).
- The might work way:
  1. Install [Python 3](https://www.python.org/downloads/) (requires Python 3.1 or higher).
  2. Install [pip](https://pip.pypa.io/en/stable/installation/).
  3. Install the following modules using pip: [Pillow](https://pillow.readthedocs.io/en/stable/installation.html#basic-installation), [fpdf](https://pypi.org/project/fpdf/).  All other modules used should come bundled with Python 3, but here they are in case you're missing some: collections, datetime, inspect, json, logging, math, os, platform, random, requests, statistics, sys, tkinter, webbrowser.
  4. Create a directory to install the font: `mkdir /usr/local/share/fonts/truetype`
  5. Copy the font from the repo's lib directory to the one just created: `cp "[path to lib dir]/Adobe Caslon Pro Semibold.ttf" /usr/local/share/fonts/truetype/`
  6. Refresh the system font cache: `fc-cache -fv` (you might need to install fc-cache with `apt install fontconfig`)
  7. Run the lib/dsbg-shuffle.py script.
In my testing, the "might work" way has some awful graphical glitches.  That may just be because I was using a Linux subsystem on Windows, but maybe not.

As for mobile, I'd like to, but I don't have any of experience with that sort of thing, and my brief looks into Android development left me confused.  So.. eventually, maybe?  Feel free to contribute or reach out if you'd like to collaborate!

For web, I'd really like to get this up as a web app, since then I wouldn't have to maintain different versions.  However, I also know nothing about web development.  So again, eventually maybe, but please reach out if you'd like to help with that!

### Why are some encounters missing from the list?

Encounters shown are dependent on the enemies you have available.  For example, there are no (at the time of writing) single enemies that are valid alternatives to a Crow Demon.  So if you don't have The Painted World of Ariamis checked in the settings, it's not going to show the Cloak and Feathers encounter because there are no valid enemy alternatives.  Iron Keep encounters that include Crystal Lizards will not show up if you don't have Iron Keep.  Encounters that contain invaders will not show up if you don't have Phantoms.

### What happened to the Hungry Mimic and Voracious Mimic?

They are no longer valid alternatives to an invader due to the new Mimic from The Sunless City.  Honestly, I think the new Mimic design is better so the Hungry Mimic and Voracious Mimic are just relics of the past, now.

### How do you decide what enemies to swap in?

This is a complex answer, so buckle up.  I want to more or less maintain the encounter's level of difficulty.  I also wanted to do as little arbritrary value assignment as possible, so I came up with a way to score enemies.  An encounter's difficulty is the sum of the scores of the enemies in the encounter.  I calculated enemy combinations that:
  1. Have the same number of enemies.
  2. Have the same number of ranged enemies as the original encounter (one exception is that Snow Rats and Crow Demons from The Painted World of Ariamis can be counted as ranged because there are no ranged enemies in that set).
  3. The sum of enemy difficulty is between 90% and 110% of the original encounter's difficulty.

Enemies are analyzed for two scores: damage and toughness.

Damage is calculated by calculating damage done to all possible character loadouts (excluding upgrades, as of the release of The Painted World of Ariamis and Tomb of Giants).  That is, I generated every combination of weapons and armor and calculated the expected damage of the enemy to that loadout.  This also uses a concept called "reach", which is an enemy's movement (prior to attacking) plus attack range.  That tells me how many nodes away from the enemy's starting position it can attack.  Enemy damage is modified by its ability to be in a position to attack based on all possible positions of the enemy and its target.  For example, an enemy with 1 move and 0 range can attack its target about 45% of the time.  Increasing either the move or range by 1 means the enemy can attack its target about 82% of the time.  Some special accommodations had to be made for bleed - I tracked potential bleed damage, and then reduced it based on the chance the average expected damage across all enemies that gets past armor/resist.  The total score is the sum of the expected damage.
Toughness is calculated by creating all dice results for every weapon, randomizing the order of those attacks, and applying them to the enemy.  I kept track of current health, poison, bleed, and the number of times the enemy dies throughout the attacks (resetting health and clearing conditions upon death).  The total score is the number of deaths.

Damage divided by toughness is the overall enemy strength.  This is what is used to do the shuffling.

### Why isn't the code for the above answer in this repo?

Because it's here: [DSBG-Encounters](https://github.com/DanDuhon/DSBG-Encounters)
None of that code actually runs with this app (this app essentially runs the output, which I only need to generate once), so I decided to keep them separate.
If you want more details about how everything works, feel free to read through the code there!
