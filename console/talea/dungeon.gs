enter -> starting_area

*exit_type {
  "Door (roll on the Door Type table)" -> door
  "Corridor, 10 ft. long"
}

*nchamber_exits {
  "EXITS -> 0"
  "EXITS -> 0"
  "EXITS -> 0"
  "EXITS -> 0"
  "EXITS -> 0"
  "EXITS -> 1" -> exit_type
  "EXITS -> 1" -> exit_type
  "EXITS -> 1" -> exit_type
  "EXITS -> 1" -> exit_type
  "EXITS -> 1" -> exit_type
  "EXITS -> 1" -> exit_type
  "EXITS -> 2" -> exit_type exit_type
  "EXITS -> 2" -> exit_type exit_type
  "EXITS -> 2" -> exit_type exit_type
  "EXITS -> 2" -> exit_type exit_type
  "EXITS -> 3" -> exit_type exit_type exit_type
  "EXITS -> 3" -> exit_type exit_type exit_type
  "EXITS -> 3" -> exit_type exit_type exit_type
  "EXITS -> 4" -> exit_type exit_type exit_type exit_type
  "EXITS -> 4" -> exit_type exit_type exit_type exit_type
}

*lchamber_exits {
  "EXITS -> 0"
  "EXITS -> 0"
  "EXITS -> 0"
  "EXITS -> 1" -> exit_type
  "EXITS -> 1" -> exit_type
  "EXITS -> 1" -> exit_type
  "EXITS -> 1" -> exit_type
  "EXITS -> 1" -> exit_type
  "EXITS -> 2" -> exit_type exit_type
  "EXITS -> 2" -> exit_type exit_type
  "EXITS -> 2" -> exit_type exit_type
  "EXITS -> 2" -> exit_type exit_type
  "EXITS -> 2" -> exit_type exit_type
  "EXITS -> 3" -> exit_type exit_type exit_type
  "EXITS -> 3" -> exit_type exit_type exit_type
  "EXITS -> 3" -> exit_type exit_type exit_type
  "EXITS -> 3" -> exit_type exit_type exit_type
  "EXITS -> 4" -> exit_type exit_type exit_type exit_type
  "EXITS -> 5" -> exit_type exit_type exit_type exit_type exit_type
  "EXITS -> 6" -> exit_type exit_type exit_type exit_type exit_type exit_type
}

*chamber {
  "Square, 20 x 20 ft." -> nchamber_exits
  "Square, 20 x 20 ft." -> nchamber_exits
  "Square, 30 x 30 ft." -> nchamber_exits
  "Square, 30 x 30 ft." -> nchamber_exits
  "Square, 40 x 40 ft." -> nchamber_exits
  "Square, 40 x 40 ft." -> nchamber_exits
  "Rectangle, 20 x 30 ft." -> nchamber_exits
  "Rectangle, 20 x 30 ft." -> nchamber_exits
  "Rectangle, 20 x 30 ft." -> nchamber_exits
  "Rectangle, 30 x 40 ft." -> nchamber_exits
  "Rectangle, 30 x 40 ft." -> nchamber_exits
  "Rectangle, 30 x 40 ft." -> nchamber_exits
  "Rectangle, 40 x 50 ft." -> lchamber_exits
  "Rectangle, 40 x 50 ft." -> lchamber_exits
  "Rectangle, 50 x 80 ft." -> lchamber_exits
  "Circle, 30 ft. diameter" -> nchamber_exits
  "Circle, 50 ft. diameter" -> lchamber_exits
  "Octagon, 40 x 40 ft." -> lchamber_exits
  "Octagon, 60 x 60 ft." -> lchamber_exits
  "Trapezoid, roughly 40 x 60 ft." -> lchamber_exits
}

*stairs {
  "Down one level to a chamber" -> chamber
  "Down one level to a chamber" -> chamber
  "Down one level to a chamber" -> chamber
  "Down one level to a chamber" -> chamber
  "Down one level to a passage 20 ft. long"
  "Down one level to a passage 20 ft. long"
  "Down one level to a passage 20 ft. long"
  "Down one level to a passage 20 ft. long"
  "Down two levels to a chamber" -> chamber
  "Down two levels to a passage 20 ft. long"
  "Down three levels to a chamber" -> chamber
  "Down three levels to a passage 20 ft. long"
  "Up one level to a chamber" -> chamber
  "Up one level to a passage 20 ft. long"
  "Up to a dead end"
  "Down to a dead end"
  "Chimney up one level to a passage 20 ft. long"
  "Chimney up two levels to a passage 20 ft. long"
  "Shaft (with or without elevator) down one level to a chamber" -> chamber
  "Shaft (with or without elevator) up one level to a chamber and down one level to a chamber" -> chamber chamber
}

*secret_door {
  "Passage extending 10 ft., then T intersection extending 10 ft. to the right and left" -> force_secret_type
  "Passage extending 10 ft., then T intersection extending 10 ft. to the right and left" -> force_secret_type
  "Passage 20 ft. straight ahead" -> force_secret_type
  "Passage 20 ft. straight ahead" -> force_secret_type
  "Passage 20 ft. straight ahead" -> force_secret_type
  "Passage 20 ft. straight ahead" -> force_secret_type
  "Passage 20 ft. straight ahead" -> force_secret_type
  "Passage 20 ft. straight ahead" -> force_secret_type
  "Chamber (roll on the Chamber table)" -> force_secret_type chamber
  "Chamber (roll on the Chamber table)" -> force_secret_type chamber
  "Chamber (roll on the Chamber table)" -> force_secret_type chamber
  "Chamber (roll on the Chamber table)" -> force_secret_type chamber
  "Chamber (roll on the Chamber table)" -> force_secret_type chamber
  "Chamber (roll on the Chamber table)" -> force_secret_type chamber
  "Chamber (roll on the Chamber table)" -> force_secret_type chamber
  "Chamber (roll on the Chamber table)" -> force_secret_type chamber
  "Chamber (roll on the Chamber table)" -> force_secret_type chamber
  "Chamber (roll on the Chamber table)" -> force_secret_type chamber
  "Stairs (roll on the Stairs table)" -> force_secret_type stairs
  "False door with trap" -> force_secret_type
}

*ten_secret {
  "No secret door."
  "No secret door."
  "No secret door."
  "No secret door."
  "No secret door."
  "No secret door."
  "No secret door."
  "No secret door."
  "No secret door."
  "Secret door!" -> secret_door
}

*door_type {
  "TYPE -> Wooden"
  "TYPE -> Wooden"
  "TYPE -> Wooden"
  "TYPE -> Wooden"
  "TYPE -> Wooden"
  "TYPE -> Wooden"
  "TYPE -> Wooden"
  "TYPE -> Wooden"
  "TYPE -> Wooden"
  "TYPE -> Wooden"
  "TYPE -> Wooden, barred or locked"
  "TYPE -> Wooden, barred or locked"
  "TYPE -> Stone"
  "TYPE -> Stone, barred or locked"
  "TYPE -> Iron"
  "TYPE -> Iron, barred or locked"
  "TYPE -> Portcullis"
  "TYPE -> Portcullis, locked in place"
  "TYPE -> Secret door"
  "TYPE -> Secret door, barred or locked"
}

*force_secret_type {
  "TYPE -> Secret door"
  "TYPE -> Secret door, barred or locked"
}

*door {
  "Passage extending 10 ft., then T intersection extending 10 ft. to the right and left" -> door_type
  "Passage extending 10 ft., then T intersection extending 10 ft. to the right and left" -> door_type
  "Passage 20 ft. straight ahead" -> door_type
  "Passage 20 ft. straight ahead" -> door_type
  "Passage 20 ft. straight ahead" -> door_type
  "Passage 20 ft. straight ahead" -> door_type
  "Passage 20 ft. straight ahead" -> door_type
  "Passage 20 ft. straight ahead" -> door_type
  "Chamber (roll on the Chamber table)" -> door_type chamber
  "Chamber (roll on the Chamber table)" -> door_type chamber
  "Chamber (roll on the Chamber table)" -> door_type chamber
  "Chamber (roll on the Chamber table)" -> door_type chamber
  "Chamber (roll on the Chamber table)" -> door_type chamber
  "Chamber (roll on the Chamber table)" -> door_type chamber
  "Chamber (roll on the Chamber table)" -> door_type chamber
  "Chamber (roll on the Chamber table)" -> door_type chamber
  "Chamber (roll on the Chamber table)" -> door_type chamber
  "Chamber (roll on the Chamber table)" -> door_type chamber
  "Stairs (roll on the Stairs table)" -> door_type stairs
  "False door with trap" -> door_type
}


*passage_width {
  "WIDTH -> 5 ft."
  "WIDTH -> 5 ft."
  "WIDTH -> 10 ft."
  "WIDTH -> 10 ft."
  "WIDTH -> 10 ft."
  "WIDTH -> 10 ft."
  "WIDTH -> 10 ft."
  "WIDTH -> 10 ft."
  "WIDTH -> 10 ft."
  "WIDTH -> 10 ft."
  "WIDTH -> 10 ft."
  "WIDTH -> 10 ft."
  "WIDTH -> 20 ft."
  "WIDTH -> 20 ft."
  "WIDTH -> 30 ft."
  "WIDTH -> 30 ft."
  "WIDTH -> 40 ft., with row of pillars down the middle"
  "WIDTH -> 40 ft., with double row of pillars"
  "WIDTH -> 40 ft. wide, 20 ft. high"
  "WIDTH -> 40 ft. wide, 20 ft. high, gallery 10 ft. above floor allows access to level above"
}

*ppassage_width {
  "WIDTH -> 5 ft."
  "WIDTH -> 5 ft."
  "WIDTH -> 10 ft."
  "WIDTH -> 10 ft."
  "WIDTH -> 10 ft."
  "WIDTH -> 10 ft."
  "WIDTH -> 10 ft."
  "WIDTH -> 10 ft."
  "WIDTH -> 10 ft."
  "WIDTH -> 10 ft."
  "WIDTH -> 10 ft."
  "WIDTH -> 10 ft."
}

*passage_fc {
  "Continue straight 30 ft., no doors or side passages" -> passage_width
  "Continue straight 30 ft., no doors or side passages" -> passage_width
  "	Continue straight 20 ft., door to the right, then an additional 10 ft. ahead" -> passage_width door
  "Continue straight 20 ft., door to the left, then an additional 10 ft. ahead" -> passage_width door
  "Continue straight 20 ft.; passage ends in a door" -> passage_width door
  "Continue straight 20 ft., side passage to the right, then an additional 10 ft. ahead" -> passage_width passage_fp
  "Continue straight 20 ft., side passage to the rig_fpht, then an additional 10 ft. ahead" -> passage_width passage_fp
  "Continue straight 20 ft., side passage to the left, then an additional 10 ft. ahead" -> passage_width passage_fp
  "Continue straight 20 ft., side passage to the left, then an additional 10 ft. ahead" -> passage_width passage_fp
  "Continue straight 20 ft., comes to a dead end; 10 percent chance of a secret door" -> passage_width ten_secret
  "Continue straight 20 ft., then the passage turns left and continues 10 ft." -> passage_width
  "Continue straight 20 ft., then the passage turns left and continues 10 ft." -> passage_width
  "Continue straight 20 ft., then the passage turns right and continues 10 ft." -> passage_width
  "Continue straight 20 ft., then the passage turns right and continues 10 ft." -> passage_width
  "Chamber (roll on the Chamber table)" -> passage_width chamber
  "Chamber (roll on the Chamber table)" -> passage_width chamber
  "Chamber (roll on the Chamber table)" -> passage_width chamber
  "Chamber (roll on the Chamber table)" -> passage_width chamber
  "Chamber (roll on the Chamber table)" -> passage_width chamber
  "Stairs* (roll on the Stairs table)" -> passage_width stairs
}

*passage_fp {
  "Continue straight 30 ft., no doors or side passages" -> ppassage_width
  "Continue straight 30 ft., no doors or side passages" -> ppassage_width
  "	Continue straight 20 ft., door to the right, then an additional 10 ft. ahead" -> ppassage_width door
  "Continue straight 20 ft., door to the left, then an additional 10 ft. ahead" -> ppassage_width door
  "Continue straight 20 ft.; passage ends in a door" -> ppassage_width door
  "Continue straight 20 ft., side passage to the right, then an additional 10 ft. ahead" -> ppassage_width passage_fp
  "Continue straight 20 ft., side passage to the right, then an additional 10 ft. ahead" -> ppassage_width passage_fp
  "Continue straight 20 ft., side passage to the left, then an additional 10 ft. ahead" -> ppassage_width passage_fp
  "Continue straight 20 ft., side passage to the left, then an additional 10 ft. ahead" -> ppassage_width passage_fp
  "Continue straight 20 ft., comes to a dead end; 10 percent chance of a secret door" -> ppassage_width ten_secret
  "Continue straight 20 ft., then the passage turns left and continues 10 ft." -> ppassage_width
  "Continue straight 20 ft., then the passage turns left and continues 10 ft." -> ppassage_width
  "Continue straight 20 ft., then the passage turns right and continues 10 ft." -> ppassage_width
  "Continue straight 20 ft., then the passage turns right and continues 10 ft." -> ppassage_width
  "Chamber (roll on the Chamber table)" -> ppassage_width chamber
  "Chamber (roll on the Chamber table)" -> ppassage_width chamber
  "Chamber (roll on the Chamber table)" -> ppassage_width chamber
  "Chamber (roll on the Chamber table)" -> ppassage_width chamber
  "Chamber (roll on the Chamber table)" -> ppassage_width chamber
  "Stairs* (roll on the Stairs table)" -> ppassage_width stairs
}


*starting_area {
  "Square, 20 x 20 ft.; passage on each wall" -> passage_fc passage_fc passage_fc
  "Square, 20 x 20 ft.; door on two walls, passage in third wall" -> door door
  "Square, 40 x 40 ft.; doors on three walls" -> door door
  "Rectangle, 80 x 20 ft., with row of pillars down the middle; two passages leading from each long wall, doors on each short wall" -> passage_fc door door
  "Rectangle, 20 x 40 ft.; passage on each wall" -> passage_fc passage_fc passage_fc
  "Circle, 40 ft. diameter; one passage at each cardinal direction" -> passage_fc passage_fc passage_fc
  "Circle, 40 ft. diameter; one passage in each cardinal direction; well in middle of room (might lead down to lower level)" -> passage_fc passage_fc passage_fc
  "Square, 20 x 20 ft.; door on two walls, passage on third wall, secret door on fourth wall" -> door door secret_door
  "Passage, 10 ft. wide; T intersection" -> passage_fc passage_fc
  "Passage, 10 ft. wide; four-way intersection" -> passage_fc passage_fc passage_fc
}
