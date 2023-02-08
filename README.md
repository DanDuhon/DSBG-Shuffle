# DSBG-Shuffle
A program to shuffle the enemies in an encounter.  Allows new combinations of enemies that are not available officially.

The idea behind this program is to provide backwards and forwards compatibility for Dark Souls The Board Game.  When the new core sets came out, they made no references to the older content. The encounter design of the new core sets are much more interesting than the old design, and I believe people should be able to use their existing enemies in this new design (or bring new enemies into the older encounters as well).  That's what I aim to accomplish here.  Users should be able to select which core sets/expansions that contain enemies.  This will inform which encounters are available (more on that later).



## How to run/Installation
1. Click the green "Code" button, then click "Download ZIP".
2. Inside the zip file is a folder called "DSBG-Shuffle-main".  Unzip this folder anywhere you want.
3. Open the folder, and run "Dark Souls The Board Game Enemy Shuffler.exe" inside it.  There isn't an installer, you just run the .exe.


## FAQ
### Are you going to support future expansions/core sets?

Yes, as time allows.  The lion's share of work is done, but new enemies will have to be analyzed and the new encounter design tends to need some custom code to do correctly.

### Are you going to support the Dark Souls Forbidden Lore Library content?

Yes, as time allows.  I'm going to prioritize official content, and I'm not going to keep on top of additions to the Library so please create an issue for things you want added!

### Can we add custom enemies/encounters ourselves?

No (unless you branch the code and do it yourself), and I don't intend to support that.  Calculating enemy strength and generating enemy combinations for an encounter can take hours depending on your machine and the size of the encounter.

### Are you going to create a version for Mac/Linux/Android/iPhone?

I'd like to, but I don't have any of experience with that sort of thing (this project is my only experience making a Windows app and I'm not even going to take much credit for that, thanks to auto-py-to-exe).  So.. eventually?  Feel free to contribute!  A workaround for Mac/Linux is if you have Python 3 installed, you can just run the enemy_swapper.py script and that should work.  You may have to install the Pillow module.

### Why are some encounters missing from the list?

Encounters shown are dependent on the enemies you have available.  For example, there are no (at the time of writing) single enemies that are valid alternatives to a Crow Demon.  So if you don't have The Painted World of Ariamis checked in the settings, it's not going to show the Cloak and Feathers encounter because there are no valid enemy alternatives.  Iron Keep encounters that include Crystal Lizards will not show up if you don't have Iron Keep.  Encounters that contain invaders/mimics will not show up if you don't have Explorers or Phantoms (but will show up if you have either).

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
If you want more details about how everything works, feel free to read through the code there!
