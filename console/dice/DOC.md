# DiceTable (dt)
A simple interpreted language for building dice tables (for random encounters, or anything really.)

A stupid project made in about 45 minutes.

## Usage of DT
When executing DT, use `python dicetable.py [filename]`.
You can use the following commands:
- `roll [#]`: rolls the default entry table (`entry`) `#` amount of times.
- `roll [#table] [#]`: rolls `#table` `#` amount of times.
- `exit`: leave
- any macros configured in the script

## Example program
Comments do not exist. `//` will cause errors or will be read as text.

```c
entry #entrytable // Set entry table
custom help : roll 1 // custom macro, typing help will bring up help table
custom start : roll #random_encounters 1 // quickly execute #random_encounters table

table d1 #entrytable // This has only one option, acting as an effective help table
1 Type 'start' to roll random encounters. Other tables: #random_combat table.
.

table d8 #random_encounters // Main random encounters table
1 	Dead body in middle of trail.
2 	Broken signpost pointing to imaginary trail.
3 	Stray horse runs past the party.
4 #flight_animals // redirect to flight animals
5 	A ruined and fallen carriage at the side of the trail.
6 	A heavy mist covers the trail.
7 	An unmarked diversion in the trail.
8 #random_combat // redirect to combat options
.

table d6 #random_combat // combat table
1 	(1d4+1) giant bats
2 	(1d6+2) zombies
3 	(1d4) skeleton horse riders
4 	(2d6) tribal warriors
5 	(2d4) owlbears
6 	(2d4) twig blights, (1d4) vine blights
.

table d3 #flight_animals // flight animals table
1 #flight_birds // another redirection
2 	Several dozen bats fly overhead.
3 	Several hundred small flies fly past.
.

table d2 #flight_birds // flight birds table
1 	Several dozen ravens fly overhead.
2 	Several dozen sparrows fly overhead
.
```

## Syntax
There are three functions in DT:
- `entry` : what table to default to
- `table .` : building dice tables
- `custom` : custom macros (e.g. `start -> roll #my_dice_table 4`)

**Important Note:** tokens are broken up with spaces and not lexed. This means ensuring there is a space (not tab) between every token is important.
You can have tab spaces in your table options to make them appear indented, but they must: `10 \tHello!`. \t does not work, but the key thing here is the space.

### table .
```c
table [dice] [table id]
1 [message]
2 [message]
3 ...
.
```
_dice_ - type of dice (/ number of options), must begin with `d`. e.g. `d5`, `d12`

_table id_ - table identifier, must begin with `#`. e.g. `#random_encounters`

_message_ - the line begins with the applicable number and a message. The message can be text or a single ID to redirect the roll to. e.g. `(2d4) bats` or `#combat`.

_._ - all table must be closed

```c
table d4 #my_table
1 Hello, world!
2 Welcome!
3 What's your name?
4 #choice
.

table d2 #choice
1 True!
2 False!
.
```

### entry
`entry [table id]`

*table id* - name of table to default to (all table names must begin with `#`)

### custom
`custom [1cmd] : [2cmd]`

*1cmd* - command to be replaced, e.g. `help`

*2cmd* - command to replace with, e.g. `roll 1`
