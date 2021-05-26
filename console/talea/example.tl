field #which_table 0-4 5-10

? #which_table 0-4
	. roll: #ind_treasure_04

? #which_table 5-10
	. roll: #ind_treasure_510

table #ind_treasure_04 [1d100]
	. 1-30 print: [5d6] cp
	. 31-60 print: [4d6] sp
	. 61-70 print: [3d6] ep
	. 71-95 print: [3d6] gp
	. 96-100 print: [1d6] pp

table #ind_treasure_510 [1d100]
	. 1-30 print: [4d6 * 100] cp, [1d6 * 10] ep
	. 31-60 print: [6d6 * 10] sp, [2d6 * 10] gp
	. 61-70 print: [1d6 * 100] ep, [2d6 * 10] gp
	. 71-95 print: [4d6 * 10] gp
	. 96-100 print: [2d6 * 10] gp, [3d6] pp
