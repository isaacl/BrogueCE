This page is a complete list of all the changes CE has made from 1.7.5. This information is current as of CE 1.14.0

# Gameplay Differences
_The changes below have some impact on game difficulty._

### Monsters

* Fixed an issue that prevented allies (e.g. kraken) from learning abilities from monsters that die in certain terrain (e.g. deep water)

* Dar priestesses are now included in the 'Mage' monster class. A weapon of mage slaying will instantly kill them, and armor of mage immunity will provide invulnerability to their feeble attacks

* Goblin conjurers no longer have the spear attack pattern in contradiction with their attack message

* Liches/phoenixes polymorphed into other creatures no longer spawn phylacteries/eggs on death

* Allies can no longer learn abilities from the spectral clones created by armor of multiplicity

* Mutated jellies now properly keep mutations when splitting

* Cautious monsters now enter corridors if they have been attacked recently and are below 50% health

### Items

* Drinking a strength potion now causes weakness to be removed from a character immediately, so that receiving another weakening attack on the same turn does not completely negate the potion

* Fixed a bug where Jellies would split when hit with a slaying or quietus weapon. They now die without splitting

* Fixed a bug which caused staffs of firebolt and lightning to deal a fixed amount of damage instead of a variable amount

* Wands of empowerment no longer increase the target's health regeneration rate

* Wands of empowerment have been strengthened to a middle-ground between their 1.7.4 and 1.7.5 versions

* Nerfed charm of teleportation recharge time. At +1 it starts at the same value, but becomes 1 turn at +13 instead of +11

* Charm of protection absorbs 26% less damage at all levels and the recharge time is capped to a minimum of 20 turns

* Guardian charm lasts for 4 additional turns but recharges in 18 more turns at all levels

* Health charm recharge time increased by 3 turns at nearly all levels

* Negation charm radius increased by 1 at all levels

* Shattering charm radius increased by 4 at all levels

* Buffed staff of protection duration. At /N max charges, the duration is now 13 x 1.4^(N-2) instead of 5 x 1.53^(N-2)

* Fixed a bug which caused staff of protection, staff of poison, and protection charm to malfunction at high enchant levels

* Fixed a bug which caused the bolt name from unidentified staffs or wands to be revealed when reflected

* Fixed a bug which caused some staffs to appear in treasure vaults without their max charges being shown

* Fixed a bug which caused unidentified rings to be revealed as negative in the ring description after reading a scroll of remove curse

* Wands of invisibility auto-ID if they turn an monster invisible while the player has a telepathic bond

* Nerfed Staff of Obstruction by (1) preventing crystals from persisting on cells occupied by creatures, and (2) allowing hunting monsters
to remain hunting as long as they are close enough and can see the player, even if impassable transparent terrain is between them

* Increased average damage for flails by 0.5, and flails now have a 2.5% (up from 0%) chance to be runic

* Increased the minimum damage absorbed by the absorption runic from 0 to 1

* When the player is telepathic, correct monsters are shown when also hallucinating

* Fixed an issue where unidentified rings could have higher bonuses than they would have once identified

* Fixed an issue where unidentified positive rings would be 1 enchant lower than they should

### Combat

* Allies can now spear attack over the player

* Monsters with a spear or whip attack can no longer attack around corners

* The rapier lunge attack works against invisible enemies when you are telepathic

* A discordant ally will no longer swap places with the player and can be attacked. Attacks require player confirmation and will not make the ally an enemy.

* Discordant allies that cast negation will no longer target other discordant allies for the sole purpose of negating the discordant status. They will still target discordant allies if negation will also have a harmful effect, such as removing haste.

* Fixed a bug with the spear attack pattern which resulted in hitting allies

* Fixed a bug which allowed fast-attacking monsters to attack the player before falling down a chasm or hole

* Fixed a bug which prevented discordant allies from attacking the player diagonally

* Fixed a bug which caused ranged-melee attackers (e.g. goblins, salamanders) with the grappling mutation to attempt to seize non-adjacent targets. Now they only seize adjacent targets and perform normal, damage-dealing, ranged attacks on non-adjacent targets

* Allies will no longer attack or cast spells at sacrifice targets

### Dungeon Generation

* Captive and shackled allies are more common

* Fixed a bug which caused some traps to be generated on cells with foliage, leading to odd behavior

* Added a sanctuary tile in front of spark turret vaults to prevent allies from destroying the turrets

* Fixed a bug where summoned minions could spawn with a carried item which was then deleted, making it unavailable for future monster drops and leading to differences in available items for players playing the same seed

* Dungeon generation on ARM processors is now the same as with x86

* Fixed doors sometimes being generated adjacent to one another

* Fix a bug which prevented sacrifice monsters from spawning on depth 21

* Levers are now indestructible via shattering and tunneling, which would leave some vaults impossible to open.

### Mechanics

* Fixed a bug where a closed door affected by descent would no longer be visible but would still block visibility. They now remain visible.

* The auto-targeting system now understands much more about whether the used item will have an effect, and skips target where it won't. This includes taking into account reflection, fire immunity, health (for domination and healing), negatable abilities, proximity (for beckoning), and weapon immunity.

* When using a known staff of tunneling, turrets and sentinels will now be auto-targeted.

* Fixed issues where auto-targeting leaked information about an unknown staff or wand

* Fixed a bug where items in deep water could drift through walls. Items can now only drift to an available adjacent cell.

* Fixed a bug where shattering failed to destroy sentinels at the edge of the dungeon

* When arriving on a level with items "obstructing" the stairs, the player now appears by the stairs like normal, on top of the item, instead of being placed on a nearby free cell. A message is displayed describing the item.

* Monsters that are summoned by allies (furies, phantoms, vampire bats) are no longer eligible for resurrection. Only the summoner will be resurrected.

* Fixed a bug which treated obsidian as shallow water, allowing a kraken to both traverse it and seize monsters or the player standing in it

* Destroying a phoenix egg or phylactery now counts toward weapon auto-ID

* Removed nearly impossible feats 'Pacifist', 'Archivist', 'Indomitable', and 'Ascetic'

* The 'Paladin' feat is no longer lost when the player is unaware of the monster, the player is seized, the monster is generated immobile (totems, turrets, etc.), or the monster is immune to physical attacks

* The 'Companion' feat now requires exploring only (approximately) 13 floors with an ally instead of 20. Exploration is measured by the number of newly discovered traversable squares while an ally is within one floor of the player.

* The 'Pure Mage' feat now allows the player to attack with their fists. Good luck with that.

* Resurrection altars now function differently for phoenixes and liches. The phoenix egg or phylactery will be revived instead, and the ability to turn into a phoenix or lich restored. Similarly, a vampire's ability to spawn vampire bats will be restored.

* Revamped the searching system. Instead of performing a strong search only after five consecutive turns of pressing 's', you now perform a weaker, single-turn search every time you press 's', with a stronger one on the fifth. (Control+s will perform five searches, stopping if interrupted, just like old 'S'.)

* Fixed a bug which caused hunting monsters to have a 97% chance to lose track of the player for each turn they spend outside of the player's stealth range, instead of the intended 3% chance

* Fixed a bug that could cause monkeys with keys to jump into lava

* Discordant wandering monsters no longer target the player with bolts/spells from beyond stealth range

* Fixed a bug which prevented a discorded ally from returning to normal after losing a stolen item in deep water

* Explosive monsters no longer explode over chasms when they would die by falling

* Fixed issues with off-level monster pathing that could cause monsters to go into a corrupted state that cannot be attacked

* Fast/slow monsters now move the correct distance and to the correct spot when reloading a level

* The player can fall through chasms into deep water without damage. Falling into shallow water or bog deals half the damage as hitting hard floor. 

* Items can fall through chasms into lava, deep water, or another chasm

* Items falling from the previous level will now trigger any traps they land on

* Items and monsters falling from the previous level will no longer fall into reward rooms

* You are now prompted when stepping onto a chasm tile with Mangrove Dryad vines on it, since you fall through them

* Aiming at a target now automatically aims for or avoids enemies/allies/walls/unknown cells, depending on the projectile type. This removes most of the need to aim for a cell beyond your intended target to get the best result. It also applies to spells cast by enemies!

* Scrolls of sanctuary can now be used on brimstone and obsidian

* When wearing known respiration armor, don't warn when stepping on immune gas traps

* When throwing a potion, auto-targeting is now enabled only for potions known to be malevolent. When throwing a melee weapon, auto-targeting is now
disabled

* Fixed a bug with machine rooms where events (such as guardian movement) could trigger twice

* Fixed a bug which slightly delayed the reset of stuck status after blinking or teleporting in or out of a web/net. Adjacent monsters at the destination were afforded a free hit while the player was "dangling helplessly" in error

* Resurrection altars prioritize allies by number of times empowered, instead of by most recent death. In the case of a tie, they choose the monster type which is found deepest in the dungeon.

* Autopilot is stopped when an item is stolen or a health alert is displayed

* Auto-explore now avoids items on candle-lit altars outside of vaults

* Fixed over-cautious pathing through deeper dungeon levels when revealed by magic mapping

* Auto-explore no longer walks through dangerous gases when wearing unidentified respiration armor

* Fixed an issue with beckoning bolt paths. This could cause mirrored totems to instakill the player and made it difficult to target enemies behind obstacles

### Informational

* Changed the color of the message when you try to pick up an item when your inventory is full, so it stands out more

* Staves and wands that affect allies are now displayed correctly on the discovered items screen

* If the player occupies a location with an item, the item is now shown in the sidebar. Additionally, the item is included in the description when inspecting the player's location.

* When inspecting a location, item descriptions now include details if space permits.

* A weapon of slaying now includes a note that the weapon doesn't degrade when attacking an acidic monster in the slaying class.

* Changed the ability description for some monsters to differentiate those that can sometimes reflect magic spells from those that always reflect spells back at the caster.

* The monster details window now includes information about the effect of negation if the player has a known means to negate the monster.

* The monster details window now includes information about the effect of tunneling or shattering if the player has such a staff.

* When an inanimate monster (e.g. turret or totem) is negated, a combat message is now displayed and the sidebar will show the negated status.

* Players can now view summary statistics of games played by selecting the "Game Stats" option from the "View" menu. Statistics are collected only for games played since the menu option became available.

* Added a new "Feats" menu option that shows a screen with all the feats and whether the player has achieved or failed them

* The "blue" player-to-monster combat information is now displayed in ally tooltips (so you can more easily assess how much health they have)

* The sidebar now displays whether a monster is carrying an item

* Magic-detected cells are now described with "you remember seeing here" when the item has been seen

* Fixed a bug where inspecting an out-of-sight lumenstone would say "you remember seeing a lumenstone from depth 0" instead of the depth it was found

* Fixed a bug where some item quantities were remembered incorrectly on leaving and revisiting a level

* Fixed a bug where staff of healing and ring of wisdom showed incorrect tooltip information

* Fixed incorrect descriptions of remembered items when hallucinating

* Fixed a rare bug on Linux where some item names would not show

* Generate a complete catalog of the items, allies, and altars for a seed (see brogue --help for details on --print-seed-catalog command line usage)

* Expected damage info in monster info boxes now accounts for the strength bonus from unidentified weapons

* When a mutated monster is negated, the mutation label is removed from the sidebar. Excludes agile and juggernaut mutations, since they cannot be negated

* Wands of negation auto-ID if the bolt has an effect. A combat message is shown for any monster affected by negation

* The sidebar and monster details now prominently display that a monster has been affected by negation

* Low health alerts no longer show on every turn when using autopilot or watching replays

* Fixed incorrect percentage health change info in sidebar

* Fixed the player's health bar showing a negative percentage when landing a hit with a transference ring equipped

* Fixed incorrect percentages in the ring of wisdom tooltip

* Repeated messages now sometimes collapse together with a count

* The message archive is now larger, and can be navigated with the up and down arrow keys. Holding shift scrolls one line at a time, holding control jumps to the end

* Staff descriptions now report the number of turns since their last use

* Fixed a bug that caused negated weapons and armor to remain illuminated when out of line of sight

* Items are automatically identified when it is possible to deduce them from the discovered items screen

* Potions of hallucination are identified when thrown if all benevolent potions are either identified or magic-detected

* When "display stealth range" is on, lit and dark areas are shown more clearly

* Items which were taken from a vault now have a note indicating this in their item description

* Identified +0 armor is prefixed with a +0, just like weapons

* Changed the graphic and description of statues that can be broken with shattering, to clearly distinguish them from regular statues

* Updated rapier description to use 'triple damage' instead of 'treble damage'

* Lumenstones are worth 500 gold on death, instead of 0

### Game Modes

* Wizard mode - Play with teleportation, immortality, overpowered items, the ability to create any item or monster. From the main menu choose Play > Change Mode > Wizard. Or start the game with the -W/--wizard command-line option.

# Non-Gameplay Differences
_The changes below have no impact on game difficulty._

### Notable Enhancements

* Added support for game variants

* Added the Rapid Brogue game variant. Fast-paced and a quarter-length of classic Brogue.

* Switch game modes from the main menu (normal/easy/wizard)

* Improved stability. Game crashes and out-of-sync errors are rare

* Improved performance and decreased CPU usage

* Support for graphical tiles (toggle with 'G') largely based on Oryx's tileset

* The game window is freely resizable, to perfectly fit any monitor up to 4K size; tiles and fonts auto-scale but stay sharp

* High DPI displays are supported on all platforms

* Seeds are now 64-bits, going up to 18446744073709551615! There are now 2 billion times more dungeons to explore!

### Other Enhancements

* Various improvements to playback and navigation of recordings

* Animations such as auto-explore and using a staff now run at a consistent speed

* Added a re-throw command (T), which throws the last item at the last-chosen monster

* Pressing "w" will hot-swap between recently equipped gear, enabling weapon/armor/ring juggling

* Turning on autopilot requires confirmation

* The maximum seed able to be input in the main menu is now the same on all platforms (2^32 - 1 = 4294967295)

* The full identified inventory is now shown on the post-victory screen

* Pressing the PrintScreen key now saves a screenshot to the save directory

* Added seed and level into default save and recording file names

* Recordings are now sorted by date descending (newest on top) and all dates (high scores, saved games, recordings) are now displayed as "YYYY-MM-DD"

* Added F12 and Alt+Enter as shortcuts for full-screen mode

* Added brogue-cmd.bat file for Windows. brogue.exe does not print output when run from a command prompt window, so use this script instead if you want to see it, e.g. when printing a seed catalog

* (For developers) You can now take control of recordings in debug mode by pressing 'P'

* Added many new command line options to specify settings on launch

* Added a hybrid graphical mode that uses text for creatures and items but graphical tiles for everything else

* "Untempted" feat has been added, for picking up no gold

* "Mystic" feat has been renamed to "Ascetic"

* Use 24-bit colors when the terminal supports it (curses build)

* Brogue now starts with a reasonable window size on ultra-wide monitors

* Fixed a bug in the terminal version where commands that use the control key (such as Ctrl+S for long search) were not working

* Added a -vn command-line option to play a replay headlessly
