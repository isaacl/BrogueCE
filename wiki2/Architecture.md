This page should give an overview of the concepts and processes used in the implementation of Brogue.

## Dungeon

The dungeon is made up of 40 levels. Each level of the dungeon is made up of a fixed-size grid of cells. Each cell is made up of

* four layers of terrain tiles: dungeon, surface, liquid, and gas
* an optional creature
* an optional item

A cell has metadata describing e.g. whether it is visible, whether it has been discovered, etc. Terrain tiles only have metadata associated with their type, and none for their specific cells.

## Creatures

All inhabitants of the dungeon are creatures, including the player. Non-player creatures are called monsters.

### Visibility

Visibility is determined with the following definitions. A creature is

* *revealed* if it is entranced, telepathically linked, or the player has telepathy (i.e. its position is known when out of sight);
* *hidden* if it is not a teammate of the observer, and is either submerged, invisible and not in gas, or dormant;
* *seen* if it is not hidden and either on a visible cell or is revealed (i.e. its kind and position are known).

The player is always seen.

### Hordes and minions

A horde is a definition of a collection of monsters. It consists of a leader and zero or more minions. spawnHorde spawns these hordes into the dungeon. It calls spawnMinions to spawn the minions.

Some monsters have a spell which allows them to summon more minions. The logic of this spell is contained in monsterSummons. It calls summonMinions to actually perform the summoning. This function selects the group of monsters to spawn via a different type of entry in the horde catalog: one which is lead by the summoning monster and has the HORDE_IS_SUMMONED flag. These entries are ignored by the normal generation process.

Some summoners have an ability MA_ENTER_SUMMONS. When such monsters summon minions, they actually move inside one of them (into the struct field carriedMonster) to be dropped when the host is destroyed. This is how eggs work (phoenix eggs and phylacteries). First an egg is spawned, via a normal horde with the egg as a leader and no minions. The egg is a summoner, so it summons a HORDE_IS_SUMMONED horde lead by its type, which contains the "chicken" creature (lich or phoenix) as a follower. The egg also has the entering flag, so it then moves inside the "chicken." When the chicken dies, the egg is dropped, and if enough time passes then the egg re-summons a chicken and moves inside it again.

## Time

Brogue processes time in ticks. Under normal conditions, each player turn is 100 ticks. The player moves first, and then monsters and the environment are processed.

Any attribute that is named as a speed (such as movement speeds or attack speeds) are actually rates, i.e. periods in ticks between actions. For example, a "move speed" of 50 means moving twice as fast as a "move speed" of 100.

## Control flow

A lot of Brogue's control flow is handled by function call nesting; some functions return values or set global variables which alter the control flow in the caller. UI code is mixed with game behaviour code.

When playing the game, Brogue runs like this, in chronological/nested order:

1. main in platform/platformdependent.c (entry point)
1. gameLoop of the current brogueConsole struct, defined in platform/
1. rogueMain in RogueMain.c
1. mainBrogueJunction in MainMenu.c (essentially the main menu button behaviours)
1. (Assuming a game was started) mainInputLoop in IO.c (creates/reads brogueEvents)
1. executeEvent in RogueMain.c
1. ... further calls based on the event type ...

If the player is viewing a recording, instead of mainInputLoop, we have

1. custom outer main loop in mainBrogueJunction
1. (If playback has been paused) pausePlayback, which calls mainInputLoop, which runs a recording UI event loop which uses executePlaybackInput in Recordings.c
1. nextBrogueEvent in IO.c, which runs its own event loop to check for UI events (by recursively calling itself with realInputEvenInPlayback=true, and calling executePlaybackInput) and then returns a recalled event
1. executeEvent, running the recalled recording event

In debug mode the user can switch to playing, which occurs in executePlaybackInput, and then causes the mainInputLoop in pausePlayback to be a normal game main loop.