# Talea
Upgraded DT.

## Example script
```lisp
field #race human elf random

? #race human
. print: Rolling a human NPC
. roll: #humanNPCName
. roll: #NPCHeight
. print: Age > [4d25 + 15] years

? #race elf
. print: Rolling an elf NPC
. roll: #elfNPCName
. roll: #NPCHeight
. print: Age > [10d100] years

? #race random
. roll: #randomNPC

table #randomNPC [1d2]
. 1 print: Rolling a human NPC
. 1-1 roll: #humanNPCName
. 1-1-1 roll: #NPCHeight
. 1-1-1-1 print: Age > [4d25 + 15] years
. 2 print: Rolling an elf NPC
. 2-2 roll: #elfNPCName
. 2-2-2 roll: #NPCHeight
. 2-2-2-2 print: Age > [10d100] years

table #humanNPCName [1d10]
. 1 print: Name > Borivik
. 2 print: Name > Faurgar
. 3 print: Name > Jandar
. 4 print: Name > Kanithar
. 5 print: Name > Madislak
. 6 print: Name > Ralmevik
. 7 print: Name > Shaumar
. 8 print: Name > Vladislak
. 9 print: Name > Fyevarra
. 10 print: Name > Hulmarra

table #elfNPCName [1d10]
. 1 print: Name > Adrie
. 2 print: Name > Althaea
. 3 print: Name > Anastrianna
. 4 print: Name > Andraste
. 5 print: Name > Antinua
. 6 print: Name > Bethrynna
. 7 print: Name > Birel
. 8 print: Name > Caelynn
. 9 print: Name > Drusilia
. 10 print: Name > Enna

table #NPCHeight [1d4]
. 1 print: Height > [1d3 + 4]' [1d12]"
. 2 print: Height > [1d2 + 4]' [1d12]"
. 3 print: Height > [1d3 + 3]' [1d12]"
. 4 print: Height > [1d2 + 5]' [1d12]"
```

## Dice format
First you need to understand dice format. Dice format is anything enclosed in `[]`. 
Things inside `[]` will be interpreted as dice. Dice format can be filled with basic math `+-*/` and dice `#d#`.
For example:
```c
[2d4 + 2]
[1d4 * 100]
```

## Tables
Tables are initialized with the `table` command.
```c
table [name] [dice]
. [dice roll] [command]
. [dice range] [command]
```
This can be filled out like this:
```c
table #ind_treasure_04 [1d100]
. 1-30 print: [5d6] cp
. 31-60 print: [4d6] sp
. 61-70 print: [3d6] ep
. 71-95 print: [3d6] gp
. 96-100 print: [1d6] pp
```

### Commands
- `roll: [table name]`: Roll on table \[table name]. e.g. `roll #ind_treasure_04`
- `print: [text]`: Print \[text], text will be brought through dice format. e.g. `print: [2d4] gp` --> `5 gp`

## Fields and ?
Fields and ? can add branching. You can add a field and it's choices with:
```c
field [name] [choice] [...]
```
Which can be filled out as:
```c
field #race human halfling orc elf half-elf
```

The ? operator can create different behaviours based on field input:
```c
? [name] [choice]
. [command]
```
Which can be filled out as:
```c
? #race human
. print: Rolling a human NPC:
. roll: #humanNPC
```
