# Save format notes

This file contains some notes about the save format. Many keys are straightforward, like 'rubies'. However, some are less so.

## Buildings

Each building consists of 6 keys:
- id: The name of the building (not including unique buildings, but includes alignment). A translation [can be found here](https://github.com/dox4242/dox4242.github.io/blob/a94559278f1b8adb6fb99ff0934dd97a44c510e2/lib/util.js#L243)
- q: The quantity of the building
- t: Total number built this reincarnation
- r: Total number built in previous reincarnations
- m: Max number built this reincarnation
- e: Max number built in all reincarnations

## Faction coins and Lineage levels

Faction coins and Lineage Levels are an array with the following order:
- Fairy
- Elven
- Angel
- Goblin
- Undead
- Demon
- Titan
- Druid
- Faceless
- Dwarven
- Drow
- Dragon
- Archon
- Maker  # DOUBLE CHECK THIS ORDER WITH ARCHON
- Djinn
- Mercenary

Of course, for faction coins specifically, entries such as Titan or Mercenary which have no faction coins, will always be 0.

## Spells

Each spell contains of 15 keys:
- id: The name of the spell. Translation [can be found here](https://github.com/dox4242/dox4242.github.io/blob/a94559278f1b8adb6fb99ff0934dd97a44c510e2/lib/util.js#L603)
- a: Boolean, if the spell is on autocasting
- active0: Active time this Abdication
- active1: Active time previous Abdications, this Reincarnation
- active2: Active time previous Reincarnations
- activeTiers:
- c: Number of spells cast this Abdication
- e: Number of spells cast previous Reincarnations
- n: Silver autocasting order, or -1 if spell is not on silver autocasting
- n2: Gold autocasting order, or -1 if the spell is not on gold autocasting
- n3: Bronze autocasting order, or -1 if the spell is not on bronze autocasting
- r: Number of spells cast previous Abdications, this Reincarnation
- s: RNG state. Only applies for Lightning Strike, Dragon's Breath, Maelstrom, Limited Wish and Catalyst
- t: Remaining duration
- tierstat1:

activeTiers reflect the autocasting tier, or the currently active tier. I'm not sure yet.

## Stats

Various stats such as gold gained, time affiliated with faction, etcetera. Each consists of 3 fields:
- stats: The stat this Abdication
- statsRei: The stat in previous Reincarnations
- statsReset: The stat in previous Abdications, this Reincarnation

The stats have this layout:

- 0-5: Gold Earned, Playtime, Good playtime, Evil playtime, Clicks, Gold earned by clicking
- 6-11: Faction coins earned for Fairy through Demon
- 12-16: Max Buildings, Max Upgrades purchased, Balance playtime, Spells cast, Mana produced
- 17-22: Number of times affiliated with Fairy through Demon
- 23-31: Assistant Squishes, Exchanged made, Gold earned by assistants, Gold spent, Mana spent, Total Abdications, Playtime last game, Gems gained last abdication, Max gold
- 32-34: Number of times affiliated with Titan through Faceless
- 35-40: Excavations made, Chaos playtime, Lightning Strike cast (alt?), Consecutive Faceless Affiliations, Max Playtime, Max spells cast
- 41, 42: Faction coins earned for Dwarven and Drow
- 43, 44: Number of times affiliated with Dwarven and Drow
- 45-48: Offline playtime, Max offline playtime, Diamond Pickaxe FC, Order playtime
- 49: Number of times affiliated with Mercenary
- 50-60: Time spent for Fairy through Drow
- 61,62: Time spent Mercenary, Time spent Unaffiliated
- 63-65: Autoclicks, Consecutive Goblin Greed casts, Goblin Crowns collected
- 66-76: Faction upgrades bought for Fairy through Drow
- 77-81: Mercenary upgrades bought, Number of times affiliated with Dragon, Time spent as Dragon, Dragon upgrades bought, Dragon Egg Timer
- And many more 

## Trophies

## Upgrades