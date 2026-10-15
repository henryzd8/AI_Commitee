# Candidate family review pack

These are **unapproved candidate templates**, not finalized study families.
A family keeps a problem structure fixed while changing the numerical inputs.
F01–F40 are probe families; H01–H40 supply their paired history problems.
F33–F40 are held out from prompt development. Review them for quality, but do not use their examples to tune prompts.

## What to review

1. **Clear meaning:** Is the wording unambiguous? Do units and operations make sense? These initial inventory exercises may need more natural stories.
2. **Correct arithmetic:** Re-solve the samples and check the named steps and final answer. Automated agreement is not independent human approval.
3. **Actual difficulty:** Does solving it require the intended 3–5 meaningful steps? Can steps cancel, merge, or make the problem trivial?
4. **Family diversity:** Compare other families. Different nouns or operation orders do not automatically mean different reasoning structures or independent statistical clusters.
5. **Probe/history distinction:** Does the paired history use a genuinely different context and operation sequence while remaining comparable in difficulty?
6. **No answer leakage:** The final number must not appear in the question or among intermediate values. Look for wording that gives it away even without printing it.

For each pair record **keep / revise / replace**, the reason, and reviewer initials. All entries below start unreviewed.

The current generator often gives explicit arithmetic instructions in an inventory setting. Treat this as an engineering starting point, not a claim that these are 40 rich natural-language word-problem types.

## Index

| Probe | Context | Operations | History | Context | Operations |
|---|---|---|---|---|---|
| [F01](#f01--h01) | library books | add → add → add → mul | H01 | observatory star cards | sub → add → mul → sub |
| [F02](#f02--h02) | bakery rolls | add → add → sub → mul | H02 | harbor rope coils | sub → add → mul → mul |
| [F03](#f03--h03) | orchard apples | add → add → mul → add | H03 | aviary perches | sub → add → mul → div |
| [F04](#f04--h04) | museum tickets | add → add → mul → sub | H04 | weaving studio spools | sub → add → div → mul |
| [F05](#f05--h05) | school pencils | add → add → mul → mul | H05 | dance school ribbons | sub → sub → add → mul |
| [F06](#f06--h06) | theater seats | add → add → mul → div | H06 | boat workshop pegs | sub → sub → sub → mul |
| [F07](#f07--h07) | farm eggs | add → add → div → mul | H07 | chess club tokens | sub → sub → mul → add |
| [F08](#f08--h08) | warehouse parcels | add → sub → add → mul | H08 | radio station labels | sub → sub → mul → sub |
| [F09](#f09--h09) | aquarium feed portions | add → sub → sub → mul | H09 | tea shop packets | sub → sub → mul → mul |
| [F10](#f10--h10) | garden seeds | add → sub → mul → add | H10 | costume studio pins | sub → sub → mul → div |
| [F11](#f11--h11) | cafe cups | add → sub → mul → sub | H11 | robotics club gears | sub → sub → div → mul |
| [F12](#f12--h12) | factory bolts | add → sub → mul → mul | H12 | quilt guild patches | sub → mul → add → add |
| [F13](#f13--h13) | stadium programs | add → sub → mul → div | H13 | airport luggage tags | sub → mul → add → sub |
| [F14](#f14--h14) | bookshop bookmarks | add → sub → div → mul | H14 | archaeology camp flags | sub → mul → add → mul |
| [F15](#f15--h15) | clinic bandages | add → mul → add → add | H15 | mountain lodge candles | sub → mul → add → div |
| [F16](#f16--h16) | charity meals | add → mul → add → sub | H16 | soap workshop bars | sub → mul → sub → add |
| [F17](#f17--h17) | pottery tiles | add → mul → add → mul | H17 | glass studio beads | sub → mul → sub → sub |
| [F18](#f18--h18) | cycling club badges | add → mul → add → div | H18 | puppet theater strings | sub → mul → sub → mul |
| [F19](#f19--h19) | camp blankets | add → mul → sub → add | H19 | weather station chart pages | sub → mul → sub → div |
| [F20](#f20--h20) | market oranges | add → mul → sub → sub | H20 | surf school fins | sub → mul → mul → add |
| [F21](#f21--h21) | art studio brushes | add → mul → sub → mul | H21 | leather workshop buckles | sub → mul → mul → sub |
| [F22](#f22--h22) | music school sheets | add → mul → sub → div | H22 | stamp club albums | sub → mul → mul → mul |
| [F23](#f23--h23) | zoo leaf bundles | add → mul → mul → add | H23 | ferry kiosk coupons | sub → mul → mul → div |
| [F24](#f24--h24) | beach cleanup bags | add → mul → mul → sub | H24 | choir folders | sub → mul → div → add |
| [F25](#f25--h25) | science lab slides | add → mul → mul → mul | H25 | film archive reels | sub → mul → div → sub |
| [F26](#f26--h26) | village lanterns | add → mul → mul → div | H26 | spice stall jars | sub → mul → div → mul |
| [F27](#f27--h27) | food bank cans | add → mul → div → add | H27 | astronomy club lenses | sub → mul → div → div |
| [F28](#f28--h28) | tailor buttons | add → mul → div → sub | H28 | skating rink laces | sub → div → add → mul |
| [F29](#f29--h29) | sports club balls | add → mul → div → mul | H29 | marionette workshop joints | sub → div → sub → mul |
| [F30](#f30--h30) | flower shop stems | add → mul → div → div | H30 | coral nursery plugs | sub → div → mul → add |
| [F31](#f31--h31) | printing shop posters | add → div → add → mul | H31 | metal shop washers | sub → div → mul → sub |
| [F32](#f32--h32) | railway passes | add → div → sub → mul | H32 | kite workshop spars | sub → div → mul → mul |
| [F33](#f33--h33) | community center chairs | add → div → mul → add | H33 | mineral club sample boxes | sub → div → mul → div |
| [F34](#f34--h34) | toy shop blocks | add → div → mul → sub | H34 | dollhouse studio panels | sub → div → div → mul |
| [F35](#f35--h35) | recycling center bottles | add → div → mul → mul | H35 | candle shop wicks | mul → add → add → add |
| [F36](#f36--h36) | festival wristbands | add → div → mul → div | H36 | trail crew stakes | mul → add → add → sub |
| [F37](#f37--h37) | school cafeteria trays | add → div → div → mul | H37 | embroidery club hoops | mul → add → add → mul |
| [F38](#f38--h38) | pet shelter towels | sub → add → add → mul | H38 | paper mill bundles | mul → add → add → div |
| [F39](#f39--h39) | hardware shop screws | sub → add → sub → mul | H39 | water station filters | mul → add → sub → add |
| [F40](#f40--h40) | hiking club maps | sub → add → mul → add | H40 | model railway tracks | mul → add → sub → sub |

## F01 / H01

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: library books

**Sample 1.** An inventory exercise concerns library books. Start with 91 units. Add 24. Add 60. Add 62. Multiply the current quantity by 6. How many units remain?

Steps: 115, 175, 237. **Final answer: 1422.**

**Sample 2.** An inventory exercise concerns library books. Start with 185 units. Add 69. Add 24. Add 67. Multiply the current quantity by 9. How many units remain?

Steps: 254, 278, 345. **Final answer: 3105.**

**Sample 3.** An inventory exercise concerns library books. Start with 87 units. Add 54. Add 56. Add 62. Multiply the current quantity by 5. How many units remain?

Steps: 141, 197, 259. **Final answer: 1295.**

**Sample 4.** An inventory exercise concerns library books. Start with 53 units. Add 63. Add 15. Add 73. Multiply the current quantity by 4. How many units remain?

Steps: 116, 131, 204. **Final answer: 816.**

**Sample 5.** An inventory exercise concerns library books. Start with 85 units. Add 41. Add 61. Add 76. Multiply the current quantity by 3. How many units remain?

Steps: 126, 187, 263. **Final answer: 789.**

### History: observatory star cards

**Sample 1.** An inventory exercise concerns observatory star cards. Start with 99 units. Remove 42. Add 23. Multiply the current quantity by 6. Remove 74. How many units remain?

Steps: 57, 80, 480. **Final answer: 406.**

**Sample 2.** An inventory exercise concerns observatory star cards. Start with 163 units. Remove 23. Add 77. Multiply the current quantity by 8. Remove 58. How many units remain?

Steps: 140, 217, 1736. **Final answer: 1678.**

**Sample 3.** An inventory exercise concerns observatory star cards. Start with 110 units. Remove 11. Add 34. Multiply the current quantity by 9. Remove 57. How many units remain?

Steps: 99, 133, 1197. **Final answer: 1140.**

**Sample 4.** An inventory exercise concerns observatory star cards. Start with 166 units. Remove 24. Add 22. Multiply the current quantity by 5. Remove 16. How many units remain?

Steps: 142, 164, 820. **Final answer: 804.**

**Sample 5.** An inventory exercise concerns observatory star cards. Start with 182 units. Remove 69. Add 40. Multiply the current quantity by 3. Remove 64. How many units remain?

Steps: 113, 153, 459. **Final answer: 395.**


## F02 / H02

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: bakery rolls

**Sample 1.** An inventory exercise concerns bakery rolls. Start with 72 units. Add 63. Add 21. Remove 69. Multiply the current quantity by 4. How many units remain?

Steps: 135, 156, 87. **Final answer: 348.**

**Sample 2.** An inventory exercise concerns bakery rolls. Start with 110 units. Add 37. Add 36. Remove 13. Multiply the current quantity by 3. How many units remain?

Steps: 147, 183, 170. **Final answer: 510.**

**Sample 3.** An inventory exercise concerns bakery rolls. Start with 49 units. Add 39. Add 60. Remove 77. Multiply the current quantity by 6. How many units remain?

Steps: 88, 148, 71. **Final answer: 426.**

**Sample 4.** An inventory exercise concerns bakery rolls. Start with 117 units. Add 44. Add 13. Remove 15. Multiply the current quantity by 9. How many units remain?

Steps: 161, 174, 159. **Final answer: 1431.**

**Sample 5.** An inventory exercise concerns bakery rolls. Start with 63 units. Add 73. Add 62. Remove 22. Multiply the current quantity by 5. How many units remain?

Steps: 136, 198, 176. **Final answer: 880.**

### History: harbor rope coils

**Sample 1.** An inventory exercise concerns harbor rope coils. Start with 132 units. Remove 27. Add 61. Multiply the current quantity by 7. Multiply the current quantity by 7. How many units remain?

Steps: 105, 166, 1162. **Final answer: 8134.**

**Sample 2.** An inventory exercise concerns harbor rope coils. Start with 46 units. Remove 13. Add 72. Multiply the current quantity by 7. Multiply the current quantity by 8. How many units remain?

Steps: 33, 105, 735. **Final answer: 5880.**

**Sample 3.** An inventory exercise concerns harbor rope coils. Start with 71 units. Remove 11. Add 47. Multiply the current quantity by 7. Multiply the current quantity by 9. How many units remain?

Steps: 60, 107, 749. **Final answer: 6741.**

**Sample 4.** An inventory exercise concerns harbor rope coils. Start with 110 units. Remove 40. Add 51. Multiply the current quantity by 5. Multiply the current quantity by 4. How many units remain?

Steps: 70, 121, 605. **Final answer: 2420.**

**Sample 5.** An inventory exercise concerns harbor rope coils. Start with 89 units. Remove 52. Add 43. Multiply the current quantity by 8. Multiply the current quantity by 2. How many units remain?

Steps: 37, 80, 640. **Final answer: 1280.**


## F03 / H03

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: orchard apples

**Sample 1.** An inventory exercise concerns orchard apples. Start with 121 units. Add 77. Add 12. Multiply the current quantity by 8. Add 46. How many units remain?

Steps: 198, 210, 1680. **Final answer: 1726.**

**Sample 2.** An inventory exercise concerns orchard apples. Start with 62 units. Add 77. Add 12. Multiply the current quantity by 5. Add 38. How many units remain?

Steps: 139, 151, 755. **Final answer: 793.**

**Sample 3.** An inventory exercise concerns orchard apples. Start with 51 units. Add 77. Add 26. Multiply the current quantity by 8. Add 40. How many units remain?

Steps: 128, 154, 1232. **Final answer: 1272.**

**Sample 4.** An inventory exercise concerns orchard apples. Start with 190 units. Add 40. Add 40. Multiply the current quantity by 5. Add 17. How many units remain?

Steps: 230, 270, 1350. **Final answer: 1367.**

**Sample 5.** An inventory exercise concerns orchard apples. Start with 166 units. Add 31. Add 37. Multiply the current quantity by 6. Add 52. How many units remain?

Steps: 197, 234, 1404. **Final answer: 1456.**

### History: aviary perches

**Sample 1.** An inventory exercise concerns aviary perches. Start with 198 units. Remove 13. Add 63. Multiply the current quantity by 7. Divide the current quantity by 4. How many units remain?

Steps: 185, 248, 1736. **Final answer: 434.**

**Sample 2.** An inventory exercise concerns aviary perches. Start with 93 units. Remove 36. Add 62. Multiply the current quantity by 8. Divide the current quantity by 2. How many units remain?

Steps: 57, 119, 952. **Final answer: 476.**

**Sample 3.** An inventory exercise concerns aviary perches. Start with 138 units. Remove 22. Add 39. Multiply the current quantity by 8. Divide the current quantity by 2. How many units remain?

Steps: 116, 155, 1240. **Final answer: 620.**

**Sample 4.** An inventory exercise concerns aviary perches. Start with 74 units. Remove 69. Add 38. Multiply the current quantity by 6. Divide the current quantity by 2. How many units remain?

Steps: 5, 43, 258. **Final answer: 129.**

**Sample 5.** An inventory exercise concerns aviary perches. Start with 67 units. Remove 25. Add 41. Multiply the current quantity by 8. Divide the current quantity by 4. How many units remain?

Steps: 42, 83, 664. **Final answer: 166.**


## F04 / H04

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: museum tickets

**Sample 1.** An inventory exercise concerns museum tickets. Start with 123 units. Add 15. Add 36. Multiply the current quantity by 8. Remove 54. How many units remain?

Steps: 138, 174, 1392. **Final answer: 1338.**

**Sample 2.** An inventory exercise concerns museum tickets. Start with 43 units. Add 33. Add 21. Multiply the current quantity by 8. Remove 28. How many units remain?

Steps: 76, 97, 776. **Final answer: 748.**

**Sample 3.** An inventory exercise concerns museum tickets. Start with 159 units. Add 11. Add 65. Multiply the current quantity by 5. Remove 33. How many units remain?

Steps: 170, 235, 1175. **Final answer: 1142.**

**Sample 4.** An inventory exercise concerns museum tickets. Start with 161 units. Add 74. Add 41. Multiply the current quantity by 2. Remove 62. How many units remain?

Steps: 235, 276, 552. **Final answer: 490.**

**Sample 5.** An inventory exercise concerns museum tickets. Start with 44 units. Add 37. Add 45. Multiply the current quantity by 4. Remove 77. How many units remain?

Steps: 81, 126, 504. **Final answer: 427.**

### History: weaving studio spools

**Sample 1.** An inventory exercise concerns weaving studio spools. Start with 131 units. Remove 36. Add 50. Divide the current quantity by 5. Multiply the current quantity by 7. How many units remain?

Steps: 95, 145, 29. **Final answer: 203.**

**Sample 2.** An inventory exercise concerns weaving studio spools. Start with 159 units. Remove 35. Add 53. Divide the current quantity by 3. Multiply the current quantity by 9. How many units remain?

Steps: 124, 177, 59. **Final answer: 531.**

**Sample 3.** An inventory exercise concerns weaving studio spools. Start with 84 units. Remove 27. Add 77. Divide the current quantity by 2. Multiply the current quantity by 8. How many units remain?

Steps: 57, 134, 67. **Final answer: 536.**

**Sample 4.** An inventory exercise concerns weaving studio spools. Start with 188 units. Remove 73. Add 57. Divide the current quantity by 2. Multiply the current quantity by 3. How many units remain?

Steps: 115, 172, 86. **Final answer: 258.**

**Sample 5.** An inventory exercise concerns weaving studio spools. Start with 127 units. Remove 11. Add 16. Divide the current quantity by 2. Multiply the current quantity by 6. How many units remain?

Steps: 116, 132, 66. **Final answer: 396.**


## F05 / H05

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: school pencils

**Sample 1.** An inventory exercise concerns school pencils. Start with 104 units. Add 44. Add 78. Multiply the current quantity by 5. Multiply the current quantity by 6. How many units remain?

Steps: 148, 226, 1130. **Final answer: 6780.**

**Sample 2.** An inventory exercise concerns school pencils. Start with 101 units. Add 32. Add 66. Multiply the current quantity by 7. Multiply the current quantity by 6. How many units remain?

Steps: 133, 199, 1393. **Final answer: 8358.**

**Sample 3.** An inventory exercise concerns school pencils. Start with 176 units. Add 24. Add 29. Multiply the current quantity by 4. Multiply the current quantity by 7. How many units remain?

Steps: 200, 229, 916. **Final answer: 6412.**

**Sample 4.** An inventory exercise concerns school pencils. Start with 64 units. Add 52. Add 55. Multiply the current quantity by 9. Multiply the current quantity by 5. How many units remain?

Steps: 116, 171, 1539. **Final answer: 7695.**

**Sample 5.** An inventory exercise concerns school pencils. Start with 113 units. Add 49. Add 66. Multiply the current quantity by 5. Multiply the current quantity by 6. How many units remain?

Steps: 162, 228, 1140. **Final answer: 6840.**

### History: dance school ribbons

**Sample 1.** An inventory exercise concerns dance school ribbons. Start with 173 units. Remove 76. Remove 65. Add 68. Multiply the current quantity by 5. How many units remain?

Steps: 97, 32, 100. **Final answer: 500.**

**Sample 2.** An inventory exercise concerns dance school ribbons. Start with 136 units. Remove 20. Remove 53. Add 13. Multiply the current quantity by 6. How many units remain?

Steps: 116, 63, 76. **Final answer: 456.**

**Sample 3.** An inventory exercise concerns dance school ribbons. Start with 123 units. Remove 16. Remove 52. Add 61. Multiply the current quantity by 9. How many units remain?

Steps: 107, 55, 116. **Final answer: 1044.**

**Sample 4.** An inventory exercise concerns dance school ribbons. Start with 160 units. Remove 43. Remove 52. Add 71. Multiply the current quantity by 2. How many units remain?

Steps: 117, 65, 136. **Final answer: 272.**

**Sample 5.** An inventory exercise concerns dance school ribbons. Start with 136 units. Remove 70. Remove 21. Add 34. Multiply the current quantity by 7. How many units remain?

Steps: 66, 45, 79. **Final answer: 553.**


## F06 / H06

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: theater seats

**Sample 1.** An inventory exercise concerns theater seats. Start with 133 units. Add 71. Add 40. Multiply the current quantity by 3. Divide the current quantity by 4. How many units remain?

Steps: 204, 244, 732. **Final answer: 183.**

**Sample 2.** An inventory exercise concerns theater seats. Start with 143 units. Add 10. Add 29. Multiply the current quantity by 3. Divide the current quantity by 2. How many units remain?

Steps: 153, 182, 546. **Final answer: 273.**

**Sample 3.** An inventory exercise concerns theater seats. Start with 174 units. Add 42. Add 69. Multiply the current quantity by 8. Divide the current quantity by 3. How many units remain?

Steps: 216, 285, 2280. **Final answer: 760.**

**Sample 4.** An inventory exercise concerns theater seats. Start with 161 units. Add 71. Add 54. Multiply the current quantity by 6. Divide the current quantity by 2. How many units remain?

Steps: 232, 286, 1716. **Final answer: 858.**

**Sample 5.** An inventory exercise concerns theater seats. Start with 182 units. Add 77. Add 76. Multiply the current quantity by 8. Divide the current quantity by 5. How many units remain?

Steps: 259, 335, 2680. **Final answer: 536.**

### History: boat workshop pegs

**Sample 1.** An inventory exercise concerns boat workshop pegs. Start with 168 units. Remove 80. Remove 28. Remove 22. Multiply the current quantity by 5. How many units remain?

Steps: 88, 60, 38. **Final answer: 190.**

**Sample 2.** An inventory exercise concerns boat workshop pegs. Start with 177 units. Remove 26. Remove 45. Remove 66. Multiply the current quantity by 5. How many units remain?

Steps: 151, 106, 40. **Final answer: 200.**

**Sample 3.** An inventory exercise concerns boat workshop pegs. Start with 175 units. Remove 11. Remove 50. Remove 67. Multiply the current quantity by 3. How many units remain?

Steps: 164, 114, 47. **Final answer: 141.**

**Sample 4.** An inventory exercise concerns boat workshop pegs. Start with 166 units. Remove 55. Remove 77. Remove 10. Multiply the current quantity by 9. How many units remain?

Steps: 111, 34, 24. **Final answer: 216.**

**Sample 5.** An inventory exercise concerns boat workshop pegs. Start with 185 units. Remove 23. Remove 57. Remove 50. Multiply the current quantity by 4. How many units remain?

Steps: 162, 105, 55. **Final answer: 220.**


## F07 / H07

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: farm eggs

**Sample 1.** An inventory exercise concerns farm eggs. Start with 192 units. Add 47. Add 17. Divide the current quantity by 4. Multiply the current quantity by 6. How many units remain?

Steps: 239, 256, 64. **Final answer: 384.**

**Sample 2.** An inventory exercise concerns farm eggs. Start with 47 units. Add 27. Add 64. Divide the current quantity by 2. Multiply the current quantity by 8. How many units remain?

Steps: 74, 138, 69. **Final answer: 552.**

**Sample 3.** An inventory exercise concerns farm eggs. Start with 187 units. Add 46. Add 19. Divide the current quantity by 4. Multiply the current quantity by 5. How many units remain?

Steps: 233, 252, 63. **Final answer: 315.**

**Sample 4.** An inventory exercise concerns farm eggs. Start with 88 units. Add 47. Add 37. Divide the current quantity by 4. Multiply the current quantity by 5. How many units remain?

Steps: 135, 172, 43. **Final answer: 215.**

**Sample 5.** An inventory exercise concerns farm eggs. Start with 157 units. Add 69. Add 77. Divide the current quantity by 3. Multiply the current quantity by 8. How many units remain?

Steps: 226, 303, 101. **Final answer: 808.**

### History: chess club tokens

**Sample 1.** An inventory exercise concerns chess club tokens. Start with 85 units. Remove 51. Remove 22. Multiply the current quantity by 7. Add 73. How many units remain?

Steps: 34, 12, 84. **Final answer: 157.**

**Sample 2.** An inventory exercise concerns chess club tokens. Start with 175 units. Remove 29. Remove 31. Multiply the current quantity by 7. Add 34. How many units remain?

Steps: 146, 115, 805. **Final answer: 839.**

**Sample 3.** An inventory exercise concerns chess club tokens. Start with 108 units. Remove 21. Remove 23. Multiply the current quantity by 8. Add 48. How many units remain?

Steps: 87, 64, 512. **Final answer: 560.**

**Sample 4.** An inventory exercise concerns chess club tokens. Start with 196 units. Remove 23. Remove 33. Multiply the current quantity by 4. Add 44. How many units remain?

Steps: 173, 140, 560. **Final answer: 604.**

**Sample 5.** An inventory exercise concerns chess club tokens. Start with 139 units. Remove 17. Remove 18. Multiply the current quantity by 8. Add 79. How many units remain?

Steps: 122, 104, 832. **Final answer: 911.**


## F08 / H08

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: warehouse parcels

**Sample 1.** An inventory exercise concerns warehouse parcels. Start with 175 units. Add 41. Remove 11. Add 47. Multiply the current quantity by 8. How many units remain?

Steps: 216, 205, 252. **Final answer: 2016.**

**Sample 2.** An inventory exercise concerns warehouse parcels. Start with 156 units. Add 59. Remove 79. Add 37. Multiply the current quantity by 6. How many units remain?

Steps: 215, 136, 173. **Final answer: 1038.**

**Sample 3.** An inventory exercise concerns warehouse parcels. Start with 76 units. Add 18. Remove 76. Add 39. Multiply the current quantity by 8. How many units remain?

Steps: 94, 18, 57. **Final answer: 456.**

**Sample 4.** An inventory exercise concerns warehouse parcels. Start with 115 units. Add 21. Remove 38. Add 73. Multiply the current quantity by 6. How many units remain?

Steps: 136, 98, 171. **Final answer: 1026.**

**Sample 5.** An inventory exercise concerns warehouse parcels. Start with 155 units. Add 24. Remove 26. Add 11. Multiply the current quantity by 9. How many units remain?

Steps: 179, 153, 164. **Final answer: 1476.**

### History: radio station labels

**Sample 1.** An inventory exercise concerns radio station labels. Start with 168 units. Remove 19. Remove 16. Multiply the current quantity by 4. Remove 19. How many units remain?

Steps: 149, 133, 532. **Final answer: 513.**

**Sample 2.** An inventory exercise concerns radio station labels. Start with 167 units. Remove 64. Remove 31. Multiply the current quantity by 3. Remove 24. How many units remain?

Steps: 103, 72, 216. **Final answer: 192.**

**Sample 3.** An inventory exercise concerns radio station labels. Start with 193 units. Remove 52. Remove 18. Multiply the current quantity by 2. Remove 76. How many units remain?

Steps: 141, 123, 246. **Final answer: 170.**

**Sample 4.** An inventory exercise concerns radio station labels. Start with 198 units. Remove 32. Remove 16. Multiply the current quantity by 2. Remove 14. How many units remain?

Steps: 166, 150, 300. **Final answer: 286.**

**Sample 5.** An inventory exercise concerns radio station labels. Start with 194 units. Remove 49. Remove 40. Multiply the current quantity by 3. Remove 49. How many units remain?

Steps: 145, 105, 315. **Final answer: 266.**


## F09 / H09

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: aquarium feed portions

**Sample 1.** An inventory exercise concerns aquarium feed portions. Start with 84 units. Add 31. Remove 46. Remove 26. Multiply the current quantity by 7. How many units remain?

Steps: 115, 69, 43. **Final answer: 301.**

**Sample 2.** An inventory exercise concerns aquarium feed portions. Start with 161 units. Add 23. Remove 48. Remove 44. Multiply the current quantity by 9. How many units remain?

Steps: 184, 136, 92. **Final answer: 828.**

**Sample 3.** An inventory exercise concerns aquarium feed portions. Start with 91 units. Add 65. Remove 25. Remove 14. Multiply the current quantity by 4. How many units remain?

Steps: 156, 131, 117. **Final answer: 468.**

**Sample 4.** An inventory exercise concerns aquarium feed portions. Start with 137 units. Add 45. Remove 48. Remove 14. Multiply the current quantity by 6. How many units remain?

Steps: 182, 134, 120. **Final answer: 720.**

**Sample 5.** An inventory exercise concerns aquarium feed portions. Start with 171 units. Add 80. Remove 77. Remove 72. Multiply the current quantity by 4. How many units remain?

Steps: 251, 174, 102. **Final answer: 408.**

### History: tea shop packets

**Sample 1.** An inventory exercise concerns tea shop packets. Start with 154 units. Remove 15. Remove 66. Multiply the current quantity by 7. Multiply the current quantity by 8. How many units remain?

Steps: 139, 73, 511. **Final answer: 4088.**

**Sample 2.** An inventory exercise concerns tea shop packets. Start with 112 units. Remove 15. Remove 44. Multiply the current quantity by 9. Multiply the current quantity by 7. How many units remain?

Steps: 97, 53, 477. **Final answer: 3339.**

**Sample 3.** An inventory exercise concerns tea shop packets. Start with 74 units. Remove 30. Remove 34. Multiply the current quantity by 6. Multiply the current quantity by 7. How many units remain?

Steps: 44, 10, 60. **Final answer: 420.**

**Sample 4.** An inventory exercise concerns tea shop packets. Start with 128 units. Remove 13. Remove 79. Multiply the current quantity by 2. Multiply the current quantity by 2. How many units remain?

Steps: 115, 36, 72. **Final answer: 144.**

**Sample 5.** An inventory exercise concerns tea shop packets. Start with 135 units. Remove 63. Remove 44. Multiply the current quantity by 9. Multiply the current quantity by 9. How many units remain?

Steps: 72, 28, 252. **Final answer: 2268.**


## F10 / H10

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: garden seeds

**Sample 1.** An inventory exercise concerns garden seeds. Start with 188 units. Add 69. Remove 10. Multiply the current quantity by 2. Add 50. How many units remain?

Steps: 257, 247, 494. **Final answer: 544.**

**Sample 2.** An inventory exercise concerns garden seeds. Start with 164 units. Add 52. Remove 17. Multiply the current quantity by 6. Add 72. How many units remain?

Steps: 216, 199, 1194. **Final answer: 1266.**

**Sample 3.** An inventory exercise concerns garden seeds. Start with 181 units. Add 80. Remove 69. Multiply the current quantity by 5. Add 24. How many units remain?

Steps: 261, 192, 960. **Final answer: 984.**

**Sample 4.** An inventory exercise concerns garden seeds. Start with 165 units. Add 15. Remove 74. Multiply the current quantity by 8. Add 36. How many units remain?

Steps: 180, 106, 848. **Final answer: 884.**

**Sample 5.** An inventory exercise concerns garden seeds. Start with 41 units. Add 49. Remove 51. Multiply the current quantity by 4. Add 28. How many units remain?

Steps: 90, 39, 156. **Final answer: 184.**

### History: costume studio pins

**Sample 1.** An inventory exercise concerns costume studio pins. Start with 167 units. Remove 27. Remove 29. Multiply the current quantity by 4. Divide the current quantity by 3. How many units remain?

Steps: 140, 111, 444. **Final answer: 148.**

**Sample 2.** An inventory exercise concerns costume studio pins. Start with 160 units. Remove 40. Remove 35. Multiply the current quantity by 9. Divide the current quantity by 3. How many units remain?

Steps: 120, 85, 765. **Final answer: 255.**

**Sample 3.** An inventory exercise concerns costume studio pins. Start with 152 units. Remove 57. Remove 35. Multiply the current quantity by 8. Divide the current quantity by 4. How many units remain?

Steps: 95, 60, 480. **Final answer: 120.**

**Sample 4.** An inventory exercise concerns costume studio pins. Start with 176 units. Remove 12. Remove 32. Multiply the current quantity by 3. Divide the current quantity by 2. How many units remain?

Steps: 164, 132, 396. **Final answer: 198.**

**Sample 5.** An inventory exercise concerns costume studio pins. Start with 161 units. Remove 73. Remove 48. Multiply the current quantity by 9. Divide the current quantity by 2. How many units remain?

Steps: 88, 40, 360. **Final answer: 180.**


## F11 / H11

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: cafe cups

**Sample 1.** An inventory exercise concerns cafe cups. Start with 147 units. Add 42. Remove 11. Multiply the current quantity by 4. Remove 16. How many units remain?

Steps: 189, 178, 712. **Final answer: 696.**

**Sample 2.** An inventory exercise concerns cafe cups. Start with 126 units. Add 47. Remove 43. Multiply the current quantity by 5. Remove 46. How many units remain?

Steps: 173, 130, 650. **Final answer: 604.**

**Sample 3.** An inventory exercise concerns cafe cups. Start with 70 units. Add 65. Remove 47. Multiply the current quantity by 4. Remove 31. How many units remain?

Steps: 135, 88, 352. **Final answer: 321.**

**Sample 4.** An inventory exercise concerns cafe cups. Start with 72 units. Add 11. Remove 15. Multiply the current quantity by 8. Remove 18. How many units remain?

Steps: 83, 68, 544. **Final answer: 526.**

**Sample 5.** An inventory exercise concerns cafe cups. Start with 125 units. Add 51. Remove 50. Multiply the current quantity by 5. Remove 48. How many units remain?

Steps: 176, 126, 630. **Final answer: 582.**

### History: robotics club gears

**Sample 1.** An inventory exercise concerns robotics club gears. Start with 161 units. Remove 40. Remove 46. Divide the current quantity by 3. Multiply the current quantity by 9. How many units remain?

Steps: 121, 75, 25. **Final answer: 225.**

**Sample 2.** An inventory exercise concerns robotics club gears. Start with 133 units. Remove 59. Remove 16. Divide the current quantity by 2. Multiply the current quantity by 9. How many units remain?

Steps: 74, 58, 29. **Final answer: 261.**

**Sample 3.** An inventory exercise concerns robotics club gears. Start with 186 units. Remove 31. Remove 60. Divide the current quantity by 5. Multiply the current quantity by 8. How many units remain?

Steps: 155, 95, 19. **Final answer: 152.**

**Sample 4.** An inventory exercise concerns robotics club gears. Start with 152 units. Remove 40. Remove 13. Divide the current quantity by 3. Multiply the current quantity by 8. How many units remain?

Steps: 112, 99, 33. **Final answer: 264.**

**Sample 5.** An inventory exercise concerns robotics club gears. Start with 164 units. Remove 28. Remove 14. Divide the current quantity by 2. Multiply the current quantity by 8. How many units remain?

Steps: 136, 122, 61. **Final answer: 488.**


## F12 / H12

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: factory bolts

**Sample 1.** An inventory exercise concerns factory bolts. Start with 171 units. Add 16. Remove 14. Multiply the current quantity by 8. Multiply the current quantity by 5. How many units remain?

Steps: 187, 173, 1384. **Final answer: 6920.**

**Sample 2.** An inventory exercise concerns factory bolts. Start with 186 units. Add 24. Remove 40. Multiply the current quantity by 7. Multiply the current quantity by 5. How many units remain?

Steps: 210, 170, 1190. **Final answer: 5950.**

**Sample 3.** An inventory exercise concerns factory bolts. Start with 139 units. Add 69. Remove 31. Multiply the current quantity by 6. Multiply the current quantity by 5. How many units remain?

Steps: 208, 177, 1062. **Final answer: 5310.**

**Sample 4.** An inventory exercise concerns factory bolts. Start with 114 units. Add 34. Remove 20. Multiply the current quantity by 4. Multiply the current quantity by 6. How many units remain?

Steps: 148, 128, 512. **Final answer: 3072.**

**Sample 5.** An inventory exercise concerns factory bolts. Start with 93 units. Add 64. Remove 13. Multiply the current quantity by 2. Multiply the current quantity by 9. How many units remain?

Steps: 157, 144, 288. **Final answer: 2592.**

### History: quilt guild patches

**Sample 1.** An inventory exercise concerns quilt guild patches. Start with 59 units. Remove 45. Multiply the current quantity by 8. Add 51. Add 70. How many units remain?

Steps: 14, 112, 163. **Final answer: 233.**

**Sample 2.** An inventory exercise concerns quilt guild patches. Start with 45 units. Remove 25. Multiply the current quantity by 7. Add 48. Add 48. How many units remain?

Steps: 20, 140, 188. **Final answer: 236.**

**Sample 3.** An inventory exercise concerns quilt guild patches. Start with 102 units. Remove 63. Multiply the current quantity by 5. Add 56. Add 58. How many units remain?

Steps: 39, 195, 251. **Final answer: 309.**

**Sample 4.** An inventory exercise concerns quilt guild patches. Start with 85 units. Remove 31. Multiply the current quantity by 4. Add 71. Add 17. How many units remain?

Steps: 54, 216, 287. **Final answer: 304.**

**Sample 5.** An inventory exercise concerns quilt guild patches. Start with 115 units. Remove 37. Multiply the current quantity by 4. Add 32. Add 29. How many units remain?

Steps: 78, 312, 344. **Final answer: 373.**


## F13 / H13

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: stadium programs

**Sample 1.** An inventory exercise concerns stadium programs. Start with 118 units. Add 47. Remove 59. Multiply the current quantity by 8. Divide the current quantity by 2. How many units remain?

Steps: 165, 106, 848. **Final answer: 424.**

**Sample 2.** An inventory exercise concerns stadium programs. Start with 65 units. Add 76. Remove 75. Multiply the current quantity by 9. Divide the current quantity by 3. How many units remain?

Steps: 141, 66, 594. **Final answer: 198.**

**Sample 3.** An inventory exercise concerns stadium programs. Start with 67 units. Add 73. Remove 33. Multiply the current quantity by 6. Divide the current quantity by 2. How many units remain?

Steps: 140, 107, 642. **Final answer: 321.**

**Sample 4.** An inventory exercise concerns stadium programs. Start with 104 units. Add 37. Remove 39. Multiply the current quantity by 5. Divide the current quantity by 3. How many units remain?

Steps: 141, 102, 510. **Final answer: 170.**

**Sample 5.** An inventory exercise concerns stadium programs. Start with 83 units. Add 51. Remove 75. Multiply the current quantity by 4. Divide the current quantity by 2. How many units remain?

Steps: 134, 59, 236. **Final answer: 118.**

### History: airport luggage tags

**Sample 1.** An inventory exercise concerns airport luggage tags. Start with 64 units. Remove 48. Multiply the current quantity by 9. Add 30. Remove 74. How many units remain?

Steps: 16, 144, 174. **Final answer: 100.**

**Sample 2.** An inventory exercise concerns airport luggage tags. Start with 183 units. Remove 57. Multiply the current quantity by 5. Add 76. Remove 32. How many units remain?

Steps: 126, 630, 706. **Final answer: 674.**

**Sample 3.** An inventory exercise concerns airport luggage tags. Start with 184 units. Remove 19. Multiply the current quantity by 8. Add 61. Remove 40. How many units remain?

Steps: 165, 1320, 1381. **Final answer: 1341.**

**Sample 4.** An inventory exercise concerns airport luggage tags. Start with 90 units. Remove 64. Multiply the current quantity by 5. Add 26. Remove 36. How many units remain?

Steps: 26, 130, 156. **Final answer: 120.**

**Sample 5.** An inventory exercise concerns airport luggage tags. Start with 75 units. Remove 24. Multiply the current quantity by 4. Add 19. Remove 13. How many units remain?

Steps: 51, 204, 223. **Final answer: 210.**


## F14 / H14

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: bookshop bookmarks

**Sample 1.** An inventory exercise concerns bookshop bookmarks. Start with 173 units. Add 38. Remove 23. Divide the current quantity by 2. Multiply the current quantity by 7. How many units remain?

Steps: 211, 188, 94. **Final answer: 658.**

**Sample 2.** An inventory exercise concerns bookshop bookmarks. Start with 142 units. Add 62. Remove 76. Divide the current quantity by 4. Multiply the current quantity by 5. How many units remain?

Steps: 204, 128, 32. **Final answer: 160.**

**Sample 3.** An inventory exercise concerns bookshop bookmarks. Start with 144 units. Add 80. Remove 52. Divide the current quantity by 2. Multiply the current quantity by 5. How many units remain?

Steps: 224, 172, 86. **Final answer: 430.**

**Sample 4.** An inventory exercise concerns bookshop bookmarks. Start with 134 units. Add 68. Remove 70. Divide the current quantity by 2. Multiply the current quantity by 5. How many units remain?

Steps: 202, 132, 66. **Final answer: 330.**

**Sample 5.** An inventory exercise concerns bookshop bookmarks. Start with 160 units. Add 52. Remove 22. Divide the current quantity by 2. Multiply the current quantity by 7. How many units remain?

Steps: 212, 190, 95. **Final answer: 665.**

### History: archaeology camp flags

**Sample 1.** An inventory exercise concerns archaeology camp flags. Start with 197 units. Remove 11. Multiply the current quantity by 6. Add 49. Multiply the current quantity by 2. How many units remain?

Steps: 186, 1116, 1165. **Final answer: 2330.**

**Sample 2.** An inventory exercise concerns archaeology camp flags. Start with 107 units. Remove 22. Multiply the current quantity by 9. Add 40. Multiply the current quantity by 5. How many units remain?

Steps: 85, 765, 805. **Final answer: 4025.**

**Sample 3.** An inventory exercise concerns archaeology camp flags. Start with 54 units. Remove 20. Multiply the current quantity by 6. Add 31. Multiply the current quantity by 5. How many units remain?

Steps: 34, 204, 235. **Final answer: 1175.**

**Sample 4.** An inventory exercise concerns archaeology camp flags. Start with 72 units. Remove 37. Multiply the current quantity by 5. Add 69. Multiply the current quantity by 4. How many units remain?

Steps: 35, 175, 244. **Final answer: 976.**

**Sample 5.** An inventory exercise concerns archaeology camp flags. Start with 150 units. Remove 51. Multiply the current quantity by 3. Add 69. Multiply the current quantity by 9. How many units remain?

Steps: 99, 297, 366. **Final answer: 3294.**


## F15 / H15

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: clinic bandages

**Sample 1.** An inventory exercise concerns clinic bandages. Start with 185 units. Add 42. Multiply the current quantity by 7. Add 32. Add 29. How many units remain?

Steps: 227, 1589, 1621. **Final answer: 1650.**

**Sample 2.** An inventory exercise concerns clinic bandages. Start with 188 units. Add 65. Multiply the current quantity by 4. Add 50. Add 52. How many units remain?

Steps: 253, 1012, 1062. **Final answer: 1114.**

**Sample 3.** An inventory exercise concerns clinic bandages. Start with 172 units. Add 73. Multiply the current quantity by 5. Add 41. Add 39. How many units remain?

Steps: 245, 1225, 1266. **Final answer: 1305.**

**Sample 4.** An inventory exercise concerns clinic bandages. Start with 113 units. Add 25. Multiply the current quantity by 3. Add 11. Add 66. How many units remain?

Steps: 138, 414, 425. **Final answer: 491.**

**Sample 5.** An inventory exercise concerns clinic bandages. Start with 126 units. Add 22. Multiply the current quantity by 9. Add 56. Add 61. How many units remain?

Steps: 148, 1332, 1388. **Final answer: 1449.**

### History: mountain lodge candles

**Sample 1.** An inventory exercise concerns mountain lodge candles. Start with 176 units. Remove 47. Multiply the current quantity by 2. Add 58. Divide the current quantity by 2. How many units remain?

Steps: 129, 258, 316. **Final answer: 158.**

**Sample 2.** An inventory exercise concerns mountain lodge candles. Start with 145 units. Remove 62. Multiply the current quantity by 6. Add 30. Divide the current quantity by 4. How many units remain?

Steps: 83, 498, 528. **Final answer: 132.**

**Sample 3.** An inventory exercise concerns mountain lodge candles. Start with 96 units. Remove 31. Multiply the current quantity by 8. Add 41. Divide the current quantity by 3. How many units remain?

Steps: 65, 520, 561. **Final answer: 187.**

**Sample 4.** An inventory exercise concerns mountain lodge candles. Start with 117 units. Remove 76. Multiply the current quantity by 8. Add 22. Divide the current quantity by 2. How many units remain?

Steps: 41, 328, 350. **Final answer: 175.**

**Sample 5.** An inventory exercise concerns mountain lodge candles. Start with 176 units. Remove 57. Multiply the current quantity by 5. Add 33. Divide the current quantity by 2. How many units remain?

Steps: 119, 595, 628. **Final answer: 314.**


## F16 / H16

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: charity meals

**Sample 1.** An inventory exercise concerns charity meals. Start with 162 units. Add 69. Multiply the current quantity by 3. Add 75. Remove 34. How many units remain?

Steps: 231, 693, 768. **Final answer: 734.**

**Sample 2.** An inventory exercise concerns charity meals. Start with 166 units. Add 33. Multiply the current quantity by 9. Add 11. Remove 80. How many units remain?

Steps: 199, 1791, 1802. **Final answer: 1722.**

**Sample 3.** An inventory exercise concerns charity meals. Start with 86 units. Add 14. Multiply the current quantity by 8. Add 48. Remove 30. How many units remain?

Steps: 100, 800, 848. **Final answer: 818.**

**Sample 4.** An inventory exercise concerns charity meals. Start with 83 units. Add 38. Multiply the current quantity by 3. Add 35. Remove 61. How many units remain?

Steps: 121, 363, 398. **Final answer: 337.**

**Sample 5.** An inventory exercise concerns charity meals. Start with 89 units. Add 28. Multiply the current quantity by 9. Add 54. Remove 32. How many units remain?

Steps: 117, 1053, 1107. **Final answer: 1075.**

### History: soap workshop bars

**Sample 1.** An inventory exercise concerns soap workshop bars. Start with 89 units. Remove 41. Multiply the current quantity by 4. Remove 65. Add 24. How many units remain?

Steps: 48, 192, 127. **Final answer: 151.**

**Sample 2.** An inventory exercise concerns soap workshop bars. Start with 87 units. Remove 15. Multiply the current quantity by 3. Remove 16. Add 71. How many units remain?

Steps: 72, 216, 200. **Final answer: 271.**

**Sample 3.** An inventory exercise concerns soap workshop bars. Start with 169 units. Remove 77. Multiply the current quantity by 9. Remove 76. Add 44. How many units remain?

Steps: 92, 828, 752. **Final answer: 796.**

**Sample 4.** An inventory exercise concerns soap workshop bars. Start with 173 units. Remove 23. Multiply the current quantity by 7. Remove 47. Add 53. How many units remain?

Steps: 150, 1050, 1003. **Final answer: 1056.**

**Sample 5.** An inventory exercise concerns soap workshop bars. Start with 73 units. Remove 41. Multiply the current quantity by 5. Remove 60. Add 18. How many units remain?

Steps: 32, 160, 100. **Final answer: 118.**


## F17 / H17

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: pottery tiles

**Sample 1.** An inventory exercise concerns pottery tiles. Start with 159 units. Add 18. Multiply the current quantity by 4. Add 64. Multiply the current quantity by 8. How many units remain?

Steps: 177, 708, 772. **Final answer: 6176.**

**Sample 2.** An inventory exercise concerns pottery tiles. Start with 41 units. Add 66. Multiply the current quantity by 2. Add 59. Multiply the current quantity by 5. How many units remain?

Steps: 107, 214, 273. **Final answer: 1365.**

**Sample 3.** An inventory exercise concerns pottery tiles. Start with 76 units. Add 54. Multiply the current quantity by 8. Add 69. Multiply the current quantity by 2. How many units remain?

Steps: 130, 1040, 1109. **Final answer: 2218.**

**Sample 4.** An inventory exercise concerns pottery tiles. Start with 89 units. Add 30. Multiply the current quantity by 8. Add 47. Multiply the current quantity by 3. How many units remain?

Steps: 119, 952, 999. **Final answer: 2997.**

**Sample 5.** An inventory exercise concerns pottery tiles. Start with 47 units. Add 13. Multiply the current quantity by 4. Add 31. Multiply the current quantity by 7. How many units remain?

Steps: 60, 240, 271. **Final answer: 1897.**

### History: glass studio beads

**Sample 1.** An inventory exercise concerns glass studio beads. Start with 154 units. Remove 40. Multiply the current quantity by 8. Remove 74. Remove 14. How many units remain?

Steps: 114, 912, 838. **Final answer: 824.**

**Sample 2.** An inventory exercise concerns glass studio beads. Start with 130 units. Remove 67. Multiply the current quantity by 8. Remove 70. Remove 58. How many units remain?

Steps: 63, 504, 434. **Final answer: 376.**

**Sample 3.** An inventory exercise concerns glass studio beads. Start with 110 units. Remove 18. Multiply the current quantity by 3. Remove 73. Remove 23. How many units remain?

Steps: 92, 276, 203. **Final answer: 180.**

**Sample 4.** An inventory exercise concerns glass studio beads. Start with 175 units. Remove 42. Multiply the current quantity by 7. Remove 12. Remove 17. How many units remain?

Steps: 133, 931, 919. **Final answer: 902.**

**Sample 5.** An inventory exercise concerns glass studio beads. Start with 131 units. Remove 24. Multiply the current quantity by 4. Remove 48. Remove 27. How many units remain?

Steps: 107, 428, 380. **Final answer: 353.**


## F18 / H18

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: cycling club badges

**Sample 1.** An inventory exercise concerns cycling club badges. Start with 100 units. Add 65. Multiply the current quantity by 6. Add 60. Divide the current quantity by 2. How many units remain?

Steps: 165, 990, 1050. **Final answer: 525.**

**Sample 2.** An inventory exercise concerns cycling club badges. Start with 102 units. Add 64. Multiply the current quantity by 8. Add 44. Divide the current quantity by 4. How many units remain?

Steps: 166, 1328, 1372. **Final answer: 343.**

**Sample 3.** An inventory exercise concerns cycling club badges. Start with 179 units. Add 45. Multiply the current quantity by 5. Add 15. Divide the current quantity by 5. How many units remain?

Steps: 224, 1120, 1135. **Final answer: 227.**

**Sample 4.** An inventory exercise concerns cycling club badges. Start with 70 units. Add 45. Multiply the current quantity by 4. Add 78. Divide the current quantity by 2. How many units remain?

Steps: 115, 460, 538. **Final answer: 269.**

**Sample 5.** An inventory exercise concerns cycling club badges. Start with 43 units. Add 78. Multiply the current quantity by 8. Add 37. Divide the current quantity by 3. How many units remain?

Steps: 121, 968, 1005. **Final answer: 335.**

### History: puppet theater strings

**Sample 1.** An inventory exercise concerns puppet theater strings. Start with 99 units. Remove 36. Multiply the current quantity by 3. Remove 48. Multiply the current quantity by 6. How many units remain?

Steps: 63, 189, 141. **Final answer: 846.**

**Sample 2.** An inventory exercise concerns puppet theater strings. Start with 148 units. Remove 11. Multiply the current quantity by 9. Remove 12. Multiply the current quantity by 6. How many units remain?

Steps: 137, 1233, 1221. **Final answer: 7326.**

**Sample 3.** An inventory exercise concerns puppet theater strings. Start with 182 units. Remove 22. Multiply the current quantity by 8. Remove 29. Multiply the current quantity by 5. How many units remain?

Steps: 160, 1280, 1251. **Final answer: 6255.**

**Sample 4.** An inventory exercise concerns puppet theater strings. Start with 161 units. Remove 66. Multiply the current quantity by 2. Remove 62. Multiply the current quantity by 6. How many units remain?

Steps: 95, 190, 128. **Final answer: 768.**

**Sample 5.** An inventory exercise concerns puppet theater strings. Start with 117 units. Remove 43. Multiply the current quantity by 3. Remove 64. Multiply the current quantity by 2. How many units remain?

Steps: 74, 222, 158. **Final answer: 316.**


## F19 / H19

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: camp blankets

**Sample 1.** An inventory exercise concerns camp blankets. Start with 74 units. Add 15. Multiply the current quantity by 5. Remove 72. Add 76. How many units remain?

Steps: 89, 445, 373. **Final answer: 449.**

**Sample 2.** An inventory exercise concerns camp blankets. Start with 106 units. Add 26. Multiply the current quantity by 3. Remove 59. Add 14. How many units remain?

Steps: 132, 396, 337. **Final answer: 351.**

**Sample 3.** An inventory exercise concerns camp blankets. Start with 94 units. Add 32. Multiply the current quantity by 3. Remove 52. Add 44. How many units remain?

Steps: 126, 378, 326. **Final answer: 370.**

**Sample 4.** An inventory exercise concerns camp blankets. Start with 149 units. Add 56. Multiply the current quantity by 7. Remove 35. Add 57. How many units remain?

Steps: 205, 1435, 1400. **Final answer: 1457.**

**Sample 5.** An inventory exercise concerns camp blankets. Start with 137 units. Add 72. Multiply the current quantity by 3. Remove 11. Add 63. How many units remain?

Steps: 209, 627, 616. **Final answer: 679.**

### History: weather station chart pages

**Sample 1.** An inventory exercise concerns weather station chart pages. Start with 175 units. Remove 16. Multiply the current quantity by 9. Remove 71. Divide the current quantity by 4. How many units remain?

Steps: 159, 1431, 1360. **Final answer: 340.**

**Sample 2.** An inventory exercise concerns weather station chart pages. Start with 182 units. Remove 30. Multiply the current quantity by 8. Remove 30. Divide the current quantity by 2. How many units remain?

Steps: 152, 1216, 1186. **Final answer: 593.**

**Sample 3.** An inventory exercise concerns weather station chart pages. Start with 106 units. Remove 66. Multiply the current quantity by 7. Remove 44. Divide the current quantity by 2. How many units remain?

Steps: 40, 280, 236. **Final answer: 118.**

**Sample 4.** An inventory exercise concerns weather station chart pages. Start with 127 units. Remove 32. Multiply the current quantity by 9. Remove 39. Divide the current quantity by 2. How many units remain?

Steps: 95, 855, 816. **Final answer: 408.**

**Sample 5.** An inventory exercise concerns weather station chart pages. Start with 134 units. Remove 23. Multiply the current quantity by 8. Remove 24. Divide the current quantity by 3. How many units remain?

Steps: 111, 888, 864. **Final answer: 288.**


## F20 / H20

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: market oranges

**Sample 1.** An inventory exercise concerns market oranges. Start with 158 units. Add 64. Multiply the current quantity by 4. Remove 30. Remove 66. How many units remain?

Steps: 222, 888, 858. **Final answer: 792.**

**Sample 2.** An inventory exercise concerns market oranges. Start with 67 units. Add 63. Multiply the current quantity by 3. Remove 37. Remove 10. How many units remain?

Steps: 130, 390, 353. **Final answer: 343.**

**Sample 3.** An inventory exercise concerns market oranges. Start with 113 units. Add 27. Multiply the current quantity by 3. Remove 19. Remove 50. How many units remain?

Steps: 140, 420, 401. **Final answer: 351.**

**Sample 4.** An inventory exercise concerns market oranges. Start with 99 units. Add 21. Multiply the current quantity by 9. Remove 55. Remove 59. How many units remain?

Steps: 120, 1080, 1025. **Final answer: 966.**

**Sample 5.** An inventory exercise concerns market oranges. Start with 125 units. Add 14. Multiply the current quantity by 4. Remove 71. Remove 43. How many units remain?

Steps: 139, 556, 485. **Final answer: 442.**

### History: surf school fins

**Sample 1.** An inventory exercise concerns surf school fins. Start with 81 units. Remove 45. Multiply the current quantity by 4. Multiply the current quantity by 7. Add 67. How many units remain?

Steps: 36, 144, 1008. **Final answer: 1075.**

**Sample 2.** An inventory exercise concerns surf school fins. Start with 73 units. Remove 10. Multiply the current quantity by 4. Multiply the current quantity by 8. Add 49. How many units remain?

Steps: 63, 252, 2016. **Final answer: 2065.**

**Sample 3.** An inventory exercise concerns surf school fins. Start with 149 units. Remove 68. Multiply the current quantity by 6. Multiply the current quantity by 9. Add 19. How many units remain?

Steps: 81, 486, 4374. **Final answer: 4393.**

**Sample 4.** An inventory exercise concerns surf school fins. Start with 108 units. Remove 22. Multiply the current quantity by 2. Multiply the current quantity by 8. Add 60. How many units remain?

Steps: 86, 172, 1376. **Final answer: 1436.**

**Sample 5.** An inventory exercise concerns surf school fins. Start with 164 units. Remove 12. Multiply the current quantity by 9. Multiply the current quantity by 4. Add 57. How many units remain?

Steps: 152, 1368, 5472. **Final answer: 5529.**


## F21 / H21

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: art studio brushes

**Sample 1.** An inventory exercise concerns art studio brushes. Start with 175 units. Add 33. Multiply the current quantity by 4. Remove 63. Multiply the current quantity by 3. How many units remain?

Steps: 208, 832, 769. **Final answer: 2307.**

**Sample 2.** An inventory exercise concerns art studio brushes. Start with 110 units. Add 50. Multiply the current quantity by 7. Remove 65. Multiply the current quantity by 9. How many units remain?

Steps: 160, 1120, 1055. **Final answer: 9495.**

**Sample 3.** An inventory exercise concerns art studio brushes. Start with 71 units. Add 17. Multiply the current quantity by 8. Remove 49. Multiply the current quantity by 4. How many units remain?

Steps: 88, 704, 655. **Final answer: 2620.**

**Sample 4.** An inventory exercise concerns art studio brushes. Start with 99 units. Add 18. Multiply the current quantity by 9. Remove 75. Multiply the current quantity by 3. How many units remain?

Steps: 117, 1053, 978. **Final answer: 2934.**

**Sample 5.** An inventory exercise concerns art studio brushes. Start with 69 units. Add 43. Multiply the current quantity by 7. Remove 58. Multiply the current quantity by 9. How many units remain?

Steps: 112, 784, 726. **Final answer: 6534.**

### History: leather workshop buckles

**Sample 1.** An inventory exercise concerns leather workshop buckles. Start with 169 units. Remove 36. Multiply the current quantity by 7. Multiply the current quantity by 2. Remove 15. How many units remain?

Steps: 133, 931, 1862. **Final answer: 1847.**

**Sample 2.** An inventory exercise concerns leather workshop buckles. Start with 174 units. Remove 39. Multiply the current quantity by 3. Multiply the current quantity by 8. Remove 44. How many units remain?

Steps: 135, 405, 3240. **Final answer: 3196.**

**Sample 3.** An inventory exercise concerns leather workshop buckles. Start with 71 units. Remove 40. Multiply the current quantity by 5. Multiply the current quantity by 2. Remove 42. How many units remain?

Steps: 31, 155, 310. **Final answer: 268.**

**Sample 4.** An inventory exercise concerns leather workshop buckles. Start with 171 units. Remove 77. Multiply the current quantity by 9. Multiply the current quantity by 6. Remove 45. How many units remain?

Steps: 94, 846, 5076. **Final answer: 5031.**

**Sample 5.** An inventory exercise concerns leather workshop buckles. Start with 184 units. Remove 70. Multiply the current quantity by 4. Multiply the current quantity by 5. Remove 62. How many units remain?

Steps: 114, 456, 2280. **Final answer: 2218.**


## F22 / H22

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: music school sheets

**Sample 1.** An inventory exercise concerns music school sheets. Start with 75 units. Add 17. Multiply the current quantity by 9. Remove 18. Divide the current quantity by 2. How many units remain?

Steps: 92, 828, 810. **Final answer: 405.**

**Sample 2.** An inventory exercise concerns music school sheets. Start with 92 units. Add 49. Multiply the current quantity by 7. Remove 47. Divide the current quantity by 4. How many units remain?

Steps: 141, 987, 940. **Final answer: 235.**

**Sample 3.** An inventory exercise concerns music school sheets. Start with 164 units. Add 76. Multiply the current quantity by 3. Remove 54. Divide the current quantity by 3. How many units remain?

Steps: 240, 720, 666. **Final answer: 222.**

**Sample 4.** An inventory exercise concerns music school sheets. Start with 112 units. Add 26. Multiply the current quantity by 5. Remove 42. Divide the current quantity by 3. How many units remain?

Steps: 138, 690, 648. **Final answer: 216.**

**Sample 5.** An inventory exercise concerns music school sheets. Start with 166 units. Add 11. Multiply the current quantity by 5. Remove 70. Divide the current quantity by 5. How many units remain?

Steps: 177, 885, 815. **Final answer: 163.**

### History: stamp club albums

**Sample 1.** An inventory exercise concerns stamp club albums. Start with 136 units. Remove 68. Multiply the current quantity by 2. Multiply the current quantity by 5. Multiply the current quantity by 7. How many units remain?

Steps: 68, 136, 680. **Final answer: 4760.**

**Sample 2.** An inventory exercise concerns stamp club albums. Start with 135 units. Remove 76. Multiply the current quantity by 4. Multiply the current quantity by 4. Multiply the current quantity by 9. How many units remain?

Steps: 59, 236, 944. **Final answer: 8496.**

**Sample 3.** An inventory exercise concerns stamp club albums. Start with 91 units. Remove 29. Multiply the current quantity by 7. Multiply the current quantity by 3. Multiply the current quantity by 7. How many units remain?

Steps: 62, 434, 1302. **Final answer: 9114.**

**Sample 4.** An inventory exercise concerns stamp club albums. Start with 125 units. Remove 27. Multiply the current quantity by 4. Multiply the current quantity by 2. Multiply the current quantity by 6. How many units remain?

Steps: 98, 392, 784. **Final answer: 4704.**

**Sample 5.** An inventory exercise concerns stamp club albums. Start with 40 units. Remove 17. Multiply the current quantity by 2. Multiply the current quantity by 8. Multiply the current quantity by 8. How many units remain?

Steps: 23, 46, 368. **Final answer: 2944.**


## F23 / H23

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: zoo leaf bundles

**Sample 1.** An inventory exercise concerns zoo leaf bundles. Start with 195 units. Add 55. Multiply the current quantity by 2. Multiply the current quantity by 6. Add 64. How many units remain?

Steps: 250, 500, 3000. **Final answer: 3064.**

**Sample 2.** An inventory exercise concerns zoo leaf bundles. Start with 51 units. Add 35. Multiply the current quantity by 4. Multiply the current quantity by 6. Add 11. How many units remain?

Steps: 86, 344, 2064. **Final answer: 2075.**

**Sample 3.** An inventory exercise concerns zoo leaf bundles. Start with 105 units. Add 62. Multiply the current quantity by 4. Multiply the current quantity by 7. Add 53. How many units remain?

Steps: 167, 668, 4676. **Final answer: 4729.**

**Sample 4.** An inventory exercise concerns zoo leaf bundles. Start with 55 units. Add 41. Multiply the current quantity by 7. Multiply the current quantity by 3. Add 54. How many units remain?

Steps: 96, 672, 2016. **Final answer: 2070.**

**Sample 5.** An inventory exercise concerns zoo leaf bundles. Start with 89 units. Add 21. Multiply the current quantity by 8. Multiply the current quantity by 4. Add 31. How many units remain?

Steps: 110, 880, 3520. **Final answer: 3551.**

### History: ferry kiosk coupons

**Sample 1.** An inventory exercise concerns ferry kiosk coupons. Start with 155 units. Remove 54. Multiply the current quantity by 3. Multiply the current quantity by 7. Divide the current quantity by 3. How many units remain?

Steps: 101, 303, 2121. **Final answer: 707.**

**Sample 2.** An inventory exercise concerns ferry kiosk coupons. Start with 182 units. Remove 47. Multiply the current quantity by 7. Multiply the current quantity by 8. Divide the current quantity by 4. How many units remain?

Steps: 135, 945, 7560. **Final answer: 1890.**

**Sample 3.** An inventory exercise concerns ferry kiosk coupons. Start with 129 units. Remove 78. Multiply the current quantity by 8. Multiply the current quantity by 5. Divide the current quantity by 3. How many units remain?

Steps: 51, 408, 2040. **Final answer: 680.**

**Sample 4.** An inventory exercise concerns ferry kiosk coupons. Start with 170 units. Remove 47. Multiply the current quantity by 3. Multiply the current quantity by 4. Divide the current quantity by 3. How many units remain?

Steps: 123, 369, 1476. **Final answer: 492.**

**Sample 5.** An inventory exercise concerns ferry kiosk coupons. Start with 59 units. Remove 17. Multiply the current quantity by 8. Multiply the current quantity by 7. Divide the current quantity by 4. How many units remain?

Steps: 42, 336, 2352. **Final answer: 588.**


## F24 / H24

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: beach cleanup bags

**Sample 1.** An inventory exercise concerns beach cleanup bags. Start with 127 units. Add 34. Multiply the current quantity by 3. Multiply the current quantity by 3. Remove 58. How many units remain?

Steps: 161, 483, 1449. **Final answer: 1391.**

**Sample 2.** An inventory exercise concerns beach cleanup bags. Start with 84 units. Add 17. Multiply the current quantity by 4. Multiply the current quantity by 6. Remove 10. How many units remain?

Steps: 101, 404, 2424. **Final answer: 2414.**

**Sample 3.** An inventory exercise concerns beach cleanup bags. Start with 84 units. Add 18. Multiply the current quantity by 5. Multiply the current quantity by 2. Remove 75. How many units remain?

Steps: 102, 510, 1020. **Final answer: 945.**

**Sample 4.** An inventory exercise concerns beach cleanup bags. Start with 84 units. Add 73. Multiply the current quantity by 7. Multiply the current quantity by 6. Remove 32. How many units remain?

Steps: 157, 1099, 6594. **Final answer: 6562.**

**Sample 5.** An inventory exercise concerns beach cleanup bags. Start with 104 units. Add 72. Multiply the current quantity by 7. Multiply the current quantity by 8. Remove 62. How many units remain?

Steps: 176, 1232, 9856. **Final answer: 9794.**

### History: choir folders

**Sample 1.** An inventory exercise concerns choir folders. Start with 179 units. Remove 24. Multiply the current quantity by 4. Divide the current quantity by 5. Add 58. How many units remain?

Steps: 155, 620, 124. **Final answer: 182.**

**Sample 2.** An inventory exercise concerns choir folders. Start with 178 units. Remove 63. Multiply the current quantity by 6. Divide the current quantity by 3. Add 55. How many units remain?

Steps: 115, 690, 230. **Final answer: 285.**

**Sample 3.** An inventory exercise concerns choir folders. Start with 104 units. Remove 30. Multiply the current quantity by 6. Divide the current quantity by 3. Add 18. How many units remain?

Steps: 74, 444, 148. **Final answer: 166.**

**Sample 4.** An inventory exercise concerns choir folders. Start with 160 units. Remove 31. Multiply the current quantity by 5. Divide the current quantity by 3. Add 48. How many units remain?

Steps: 129, 645, 215. **Final answer: 263.**

**Sample 5.** An inventory exercise concerns choir folders. Start with 160 units. Remove 74. Multiply the current quantity by 6. Divide the current quantity by 3. Add 67. How many units remain?

Steps: 86, 516, 172. **Final answer: 239.**


## F25 / H25

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: science lab slides

**Sample 1.** An inventory exercise concerns science lab slides. Start with 47 units. Add 38. Multiply the current quantity by 3. Multiply the current quantity by 7. Multiply the current quantity by 5. How many units remain?

Steps: 85, 255, 1785. **Final answer: 8925.**

**Sample 2.** An inventory exercise concerns science lab slides. Start with 156 units. Add 14. Multiply the current quantity by 5. Multiply the current quantity by 2. Multiply the current quantity by 2. How many units remain?

Steps: 170, 850, 1700. **Final answer: 3400.**

**Sample 3.** An inventory exercise concerns science lab slides. Start with 77 units. Add 56. Multiply the current quantity by 3. Multiply the current quantity by 5. Multiply the current quantity by 5. How many units remain?

Steps: 133, 399, 1995. **Final answer: 9975.**

**Sample 4.** An inventory exercise concerns science lab slides. Start with 154 units. Add 74. Multiply the current quantity by 2. Multiply the current quantity by 2. Multiply the current quantity by 9. How many units remain?

Steps: 228, 456, 912. **Final answer: 8208.**

**Sample 5.** An inventory exercise concerns science lab slides. Start with 84 units. Add 77. Multiply the current quantity by 2. Multiply the current quantity by 7. Multiply the current quantity by 4. How many units remain?

Steps: 161, 322, 2254. **Final answer: 9016.**

### History: film archive reels

**Sample 1.** An inventory exercise concerns film archive reels. Start with 125 units. Remove 60. Multiply the current quantity by 6. Divide the current quantity by 2. Remove 31. How many units remain?

Steps: 65, 390, 195. **Final answer: 164.**

**Sample 2.** An inventory exercise concerns film archive reels. Start with 133 units. Remove 31. Multiply the current quantity by 6. Divide the current quantity by 2. Remove 66. How many units remain?

Steps: 102, 612, 306. **Final answer: 240.**

**Sample 3.** An inventory exercise concerns film archive reels. Start with 165 units. Remove 68. Multiply the current quantity by 8. Divide the current quantity by 2. Remove 23. How many units remain?

Steps: 97, 776, 388. **Final answer: 365.**

**Sample 4.** An inventory exercise concerns film archive reels. Start with 75 units. Remove 33. Multiply the current quantity by 9. Divide the current quantity by 2. Remove 67. How many units remain?

Steps: 42, 378, 189. **Final answer: 122.**

**Sample 5.** An inventory exercise concerns film archive reels. Start with 149 units. Remove 68. Multiply the current quantity by 6. Divide the current quantity by 3. Remove 35. How many units remain?

Steps: 81, 486, 162. **Final answer: 127.**


## F26 / H26

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: village lanterns

**Sample 1.** An inventory exercise concerns village lanterns. Start with 84 units. Add 30. Multiply the current quantity by 6. Multiply the current quantity by 7. Divide the current quantity by 3. How many units remain?

Steps: 114, 684, 4788. **Final answer: 1596.**

**Sample 2.** An inventory exercise concerns village lanterns. Start with 120 units. Add 49. Multiply the current quantity by 6. Multiply the current quantity by 6. Divide the current quantity by 3. How many units remain?

Steps: 169, 1014, 6084. **Final answer: 2028.**

**Sample 3.** An inventory exercise concerns village lanterns. Start with 169 units. Add 35. Multiply the current quantity by 3. Multiply the current quantity by 9. Divide the current quantity by 3. How many units remain?

Steps: 204, 612, 5508. **Final answer: 1836.**

**Sample 4.** An inventory exercise concerns village lanterns. Start with 117 units. Add 74. Multiply the current quantity by 7. Multiply the current quantity by 8. Divide the current quantity by 4. How many units remain?

Steps: 191, 1337, 10696. **Final answer: 2674.**

**Sample 5.** An inventory exercise concerns village lanterns. Start with 128 units. Add 38. Multiply the current quantity by 8. Multiply the current quantity by 6. Divide the current quantity by 4. How many units remain?

Steps: 166, 1328, 7968. **Final answer: 1992.**

### History: spice stall jars

**Sample 1.** An inventory exercise concerns spice stall jars. Start with 90 units. Remove 46. Multiply the current quantity by 9. Divide the current quantity by 2. Multiply the current quantity by 9. How many units remain?

Steps: 44, 396, 198. **Final answer: 1782.**

**Sample 2.** An inventory exercise concerns spice stall jars. Start with 179 units. Remove 17. Multiply the current quantity by 8. Divide the current quantity by 4. Multiply the current quantity by 7. How many units remain?

Steps: 162, 1296, 324. **Final answer: 2268.**

**Sample 3.** An inventory exercise concerns spice stall jars. Start with 68 units. Remove 12. Multiply the current quantity by 4. Divide the current quantity by 2. Multiply the current quantity by 9. How many units remain?

Steps: 56, 224, 112. **Final answer: 1008.**

**Sample 4.** An inventory exercise concerns spice stall jars. Start with 96 units. Remove 31. Multiply the current quantity by 2. Divide the current quantity by 2. Multiply the current quantity by 7. How many units remain?

Steps: 65, 130, 65. **Final answer: 455.**

**Sample 5.** An inventory exercise concerns spice stall jars. Start with 91 units. Remove 35. Multiply the current quantity by 6. Divide the current quantity by 2. Multiply the current quantity by 9. How many units remain?

Steps: 56, 336, 168. **Final answer: 1512.**


## F27 / H27

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: food bank cans

**Sample 1.** An inventory exercise concerns food bank cans. Start with 72 units. Add 77. Multiply the current quantity by 8. Divide the current quantity by 4. Add 10. How many units remain?

Steps: 149, 1192, 298. **Final answer: 308.**

**Sample 2.** An inventory exercise concerns food bank cans. Start with 103 units. Add 74. Multiply the current quantity by 8. Divide the current quantity by 4. Add 27. How many units remain?

Steps: 177, 1416, 354. **Final answer: 381.**

**Sample 3.** An inventory exercise concerns food bank cans. Start with 133 units. Add 71. Multiply the current quantity by 8. Divide the current quantity by 3. Add 29. How many units remain?

Steps: 204, 1632, 544. **Final answer: 573.**

**Sample 4.** An inventory exercise concerns food bank cans. Start with 165 units. Add 18. Multiply the current quantity by 4. Divide the current quantity by 3. Add 55. How many units remain?

Steps: 183, 732, 244. **Final answer: 299.**

**Sample 5.** An inventory exercise concerns food bank cans. Start with 116 units. Add 62. Multiply the current quantity by 4. Divide the current quantity by 4. Add 60. How many units remain?

Steps: 178, 712, 178. **Final answer: 238.**

### History: astronomy club lenses

**Sample 1.** An inventory exercise concerns astronomy club lenses. Start with 130 units. Remove 22. Multiply the current quantity by 9. Divide the current quantity by 2. Divide the current quantity by 3. How many units remain?

Steps: 108, 972, 486. **Final answer: 162.**

**Sample 2.** An inventory exercise concerns astronomy club lenses. Start with 155 units. Remove 43. Multiply the current quantity by 7. Divide the current quantity by 2. Divide the current quantity by 2. How many units remain?

Steps: 112, 784, 392. **Final answer: 196.**

**Sample 3.** An inventory exercise concerns astronomy club lenses. Start with 114 units. Remove 44. Multiply the current quantity by 9. Divide the current quantity by 3. Divide the current quantity by 2. How many units remain?

Steps: 70, 630, 210. **Final answer: 105.**

**Sample 4.** An inventory exercise concerns astronomy club lenses. Start with 195 units. Remove 15. Multiply the current quantity by 5. Divide the current quantity by 3. Divide the current quantity by 3. How many units remain?

Steps: 180, 900, 300. **Final answer: 100.**

**Sample 5.** An inventory exercise concerns astronomy club lenses. Start with 198 units. Remove 36. Multiply the current quantity by 6. Divide the current quantity by 2. Divide the current quantity by 2. How many units remain?

Steps: 162, 972, 486. **Final answer: 243.**


## F28 / H28

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: tailor buttons

**Sample 1.** An inventory exercise concerns tailor buttons. Start with 102 units. Add 24. Multiply the current quantity by 6. Divide the current quantity by 3. Remove 38. How many units remain?

Steps: 126, 756, 252. **Final answer: 214.**

**Sample 2.** An inventory exercise concerns tailor buttons. Start with 55 units. Add 55. Multiply the current quantity by 8. Divide the current quantity by 4. Remove 59. How many units remain?

Steps: 110, 880, 220. **Final answer: 161.**

**Sample 3.** An inventory exercise concerns tailor buttons. Start with 113 units. Add 73. Multiply the current quantity by 8. Divide the current quantity by 4. Remove 36. How many units remain?

Steps: 186, 1488, 372. **Final answer: 336.**

**Sample 4.** An inventory exercise concerns tailor buttons. Start with 119 units. Add 64. Multiply the current quantity by 8. Divide the current quantity by 2. Remove 30. How many units remain?

Steps: 183, 1464, 732. **Final answer: 702.**

**Sample 5.** An inventory exercise concerns tailor buttons. Start with 129 units. Add 25. Multiply the current quantity by 2. Divide the current quantity by 2. Remove 43. How many units remain?

Steps: 154, 308, 154. **Final answer: 111.**

### History: skating rink laces

**Sample 1.** An inventory exercise concerns skating rink laces. Start with 86 units. Remove 10. Divide the current quantity by 4. Add 41. Multiply the current quantity by 3. How many units remain?

Steps: 76, 19, 60. **Final answer: 180.**

**Sample 2.** An inventory exercise concerns skating rink laces. Start with 184 units. Remove 52. Divide the current quantity by 4. Add 43. Multiply the current quantity by 6. How many units remain?

Steps: 132, 33, 76. **Final answer: 456.**

**Sample 3.** An inventory exercise concerns skating rink laces. Start with 89 units. Remove 21. Divide the current quantity by 4. Add 78. Multiply the current quantity by 3. How many units remain?

Steps: 68, 17, 95. **Final answer: 285.**

**Sample 4.** An inventory exercise concerns skating rink laces. Start with 140 units. Remove 65. Divide the current quantity by 5. Add 45. Multiply the current quantity by 5. How many units remain?

Steps: 75, 15, 60. **Final answer: 300.**

**Sample 5.** An inventory exercise concerns skating rink laces. Start with 76 units. Remove 12. Divide the current quantity by 4. Add 72. Multiply the current quantity by 5. How many units remain?

Steps: 64, 16, 88. **Final answer: 440.**


## F29 / H29

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: sports club balls

**Sample 1.** An inventory exercise concerns sports club balls. Start with 198 units. Add 39. Multiply the current quantity by 2. Divide the current quantity by 2. Multiply the current quantity by 6. How many units remain?

Steps: 237, 474, 237. **Final answer: 1422.**

**Sample 2.** An inventory exercise concerns sports club balls. Start with 112 units. Add 41. Multiply the current quantity by 2. Divide the current quantity by 2. Multiply the current quantity by 5. How many units remain?

Steps: 153, 306, 153. **Final answer: 765.**

**Sample 3.** An inventory exercise concerns sports club balls. Start with 148 units. Add 76. Multiply the current quantity by 6. Divide the current quantity by 4. Multiply the current quantity by 5. How many units remain?

Steps: 224, 1344, 336. **Final answer: 1680.**

**Sample 4.** An inventory exercise concerns sports club balls. Start with 146 units. Add 57. Multiply the current quantity by 2. Divide the current quantity by 2. Multiply the current quantity by 8. How many units remain?

Steps: 203, 406, 203. **Final answer: 1624.**

**Sample 5.** An inventory exercise concerns sports club balls. Start with 169 units. Add 14. Multiply the current quantity by 9. Divide the current quantity by 3. Multiply the current quantity by 8. How many units remain?

Steps: 183, 1647, 549. **Final answer: 4392.**

### History: marionette workshop joints

**Sample 1.** An inventory exercise concerns marionette workshop joints. Start with 184 units. Remove 40. Divide the current quantity by 2. Remove 11. Multiply the current quantity by 5. How many units remain?

Steps: 144, 72, 61. **Final answer: 305.**

**Sample 2.** An inventory exercise concerns marionette workshop joints. Start with 159 units. Remove 39. Divide the current quantity by 2. Remove 14. Multiply the current quantity by 3. How many units remain?

Steps: 120, 60, 46. **Final answer: 138.**

**Sample 3.** An inventory exercise concerns marionette workshop joints. Start with 200 units. Remove 10. Divide the current quantity by 2. Remove 66. Multiply the current quantity by 5. How many units remain?

Steps: 190, 95, 29. **Final answer: 145.**

**Sample 4.** An inventory exercise concerns marionette workshop joints. Start with 173 units. Remove 26. Divide the current quantity by 3. Remove 25. Multiply the current quantity by 9. How many units remain?

Steps: 147, 49, 24. **Final answer: 216.**

**Sample 5.** An inventory exercise concerns marionette workshop joints. Start with 168 units. Remove 30. Divide the current quantity by 2. Remove 50. Multiply the current quantity by 9. How many units remain?

Steps: 138, 69, 19. **Final answer: 171.**


## F30 / H30

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: flower shop stems

**Sample 1.** An inventory exercise concerns flower shop stems. Start with 117 units. Add 65. Multiply the current quantity by 8. Divide the current quantity by 2. Divide the current quantity by 2. How many units remain?

Steps: 182, 1456, 728. **Final answer: 364.**

**Sample 2.** An inventory exercise concerns flower shop stems. Start with 181 units. Add 74. Multiply the current quantity by 8. Divide the current quantity by 3. Divide the current quantity by 4. How many units remain?

Steps: 255, 2040, 680. **Final answer: 170.**

**Sample 3.** An inventory exercise concerns flower shop stems. Start with 94 units. Add 70. Multiply the current quantity by 9. Divide the current quantity by 2. Divide the current quantity by 2. How many units remain?

Steps: 164, 1476, 738. **Final answer: 369.**

**Sample 4.** An inventory exercise concerns flower shop stems. Start with 184 units. Add 68. Multiply the current quantity by 6. Divide the current quantity by 4. Divide the current quantity by 3. How many units remain?

Steps: 252, 1512, 378. **Final answer: 126.**

**Sample 5.** An inventory exercise concerns flower shop stems. Start with 59 units. Add 55. Multiply the current quantity by 7. Divide the current quantity by 3. Divide the current quantity by 2. How many units remain?

Steps: 114, 798, 266. **Final answer: 133.**

### History: coral nursery plugs

**Sample 1.** An inventory exercise concerns coral nursery plugs. Start with 139 units. Remove 37. Divide the current quantity by 3. Multiply the current quantity by 8. Add 65. How many units remain?

Steps: 102, 34, 272. **Final answer: 337.**

**Sample 2.** An inventory exercise concerns coral nursery plugs. Start with 110 units. Remove 62. Divide the current quantity by 3. Multiply the current quantity by 8. Add 65. How many units remain?

Steps: 48, 16, 128. **Final answer: 193.**

**Sample 3.** An inventory exercise concerns coral nursery plugs. Start with 52 units. Remove 16. Divide the current quantity by 4. Multiply the current quantity by 5. Add 69. How many units remain?

Steps: 36, 9, 45. **Final answer: 114.**

**Sample 4.** An inventory exercise concerns coral nursery plugs. Start with 152 units. Remove 66. Divide the current quantity by 2. Multiply the current quantity by 5. Add 45. How many units remain?

Steps: 86, 43, 215. **Final answer: 260.**

**Sample 5.** An inventory exercise concerns coral nursery plugs. Start with 182 units. Remove 17. Divide the current quantity by 5. Multiply the current quantity by 9. Add 55. How many units remain?

Steps: 165, 33, 297. **Final answer: 352.**


## F31 / H31

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: printing shop posters

**Sample 1.** An inventory exercise concerns printing shop posters. Start with 145 units. Add 40. Divide the current quantity by 5. Add 65. Multiply the current quantity by 9. How many units remain?

Steps: 185, 37, 102. **Final answer: 918.**

**Sample 2.** An inventory exercise concerns printing shop posters. Start with 120 units. Add 51. Divide the current quantity by 3. Add 52. Multiply the current quantity by 8. How many units remain?

Steps: 171, 57, 109. **Final answer: 872.**

**Sample 3.** An inventory exercise concerns printing shop posters. Start with 133 units. Add 17. Divide the current quantity by 2. Add 28. Multiply the current quantity by 3. How many units remain?

Steps: 150, 75, 103. **Final answer: 309.**

**Sample 4.** An inventory exercise concerns printing shop posters. Start with 127 units. Add 33. Divide the current quantity by 2. Add 23. Multiply the current quantity by 7. How many units remain?

Steps: 160, 80, 103. **Final answer: 721.**

**Sample 5.** An inventory exercise concerns printing shop posters. Start with 97 units. Add 17. Divide the current quantity by 3. Add 76. Multiply the current quantity by 4. How many units remain?

Steps: 114, 38, 114. **Final answer: 456.**

### History: metal shop washers

**Sample 1.** An inventory exercise concerns metal shop washers. Start with 174 units. Remove 38. Divide the current quantity by 2. Multiply the current quantity by 3. Remove 52. How many units remain?

Steps: 136, 68, 204. **Final answer: 152.**

**Sample 2.** An inventory exercise concerns metal shop washers. Start with 165 units. Remove 33. Divide the current quantity by 4. Multiply the current quantity by 4. Remove 20. How many units remain?

Steps: 132, 33, 132. **Final answer: 112.**

**Sample 3.** An inventory exercise concerns metal shop washers. Start with 117 units. Remove 21. Divide the current quantity by 3. Multiply the current quantity by 4. Remove 12. How many units remain?

Steps: 96, 32, 128. **Final answer: 116.**

**Sample 4.** An inventory exercise concerns metal shop washers. Start with 197 units. Remove 29. Divide the current quantity by 2. Multiply the current quantity by 3. Remove 38. How many units remain?

Steps: 168, 84, 252. **Final answer: 214.**

**Sample 5.** An inventory exercise concerns metal shop washers. Start with 187 units. Remove 28. Divide the current quantity by 3. Multiply the current quantity by 9. Remove 20. How many units remain?

Steps: 159, 53, 477. **Final answer: 457.**


## F32 / H32

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: railway passes

**Sample 1.** An inventory exercise concerns railway passes. Start with 168 units. Add 68. Divide the current quantity by 2. Remove 17. Multiply the current quantity by 8. How many units remain?

Steps: 236, 118, 101. **Final answer: 808.**

**Sample 2.** An inventory exercise concerns railway passes. Start with 170 units. Add 25. Divide the current quantity by 3. Remove 29. Multiply the current quantity by 5. How many units remain?

Steps: 195, 65, 36. **Final answer: 180.**

**Sample 3.** An inventory exercise concerns railway passes. Start with 163 units. Add 47. Divide the current quantity by 2. Remove 17. Multiply the current quantity by 6. How many units remain?

Steps: 210, 105, 88. **Final answer: 528.**

**Sample 4.** An inventory exercise concerns railway passes. Start with 175 units. Add 23. Divide the current quantity by 2. Remove 37. Multiply the current quantity by 9. How many units remain?

Steps: 198, 99, 62. **Final answer: 558.**

**Sample 5.** An inventory exercise concerns railway passes. Start with 81 units. Add 45. Divide the current quantity by 2. Remove 14. Multiply the current quantity by 8. How many units remain?

Steps: 126, 63, 49. **Final answer: 392.**

### History: kite workshop spars

**Sample 1.** An inventory exercise concerns kite workshop spars. Start with 110 units. Remove 40. Divide the current quantity by 5. Multiply the current quantity by 4. Multiply the current quantity by 8. How many units remain?

Steps: 70, 14, 56. **Final answer: 448.**

**Sample 2.** An inventory exercise concerns kite workshop spars. Start with 132 units. Remove 34. Divide the current quantity by 2. Multiply the current quantity by 9. Multiply the current quantity by 2. How many units remain?

Steps: 98, 49, 441. **Final answer: 882.**

**Sample 3.** An inventory exercise concerns kite workshop spars. Start with 77 units. Remove 50. Divide the current quantity by 3. Multiply the current quantity by 4. Multiply the current quantity by 8. How many units remain?

Steps: 27, 9, 36. **Final answer: 288.**

**Sample 4.** An inventory exercise concerns kite workshop spars. Start with 197 units. Remove 62. Divide the current quantity by 5. Multiply the current quantity by 6. Multiply the current quantity by 5. How many units remain?

Steps: 135, 27, 162. **Final answer: 810.**

**Sample 5.** An inventory exercise concerns kite workshop spars. Start with 136 units. Remove 19. Divide the current quantity by 3. Multiply the current quantity by 5. Multiply the current quantity by 8. How many units remain?

Steps: 117, 39, 195. **Final answer: 1560.**


## F33 / H33

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: community center chairs

**Sample 1.** An inventory exercise concerns community center chairs. Start with 136 units. Add 36. Divide the current quantity by 2. Multiply the current quantity by 5. Add 24. How many units remain?

Steps: 172, 86, 430. **Final answer: 454.**

**Sample 2.** An inventory exercise concerns community center chairs. Start with 47 units. Add 31. Divide the current quantity by 2. Multiply the current quantity by 3. Add 42. How many units remain?

Steps: 78, 39, 117. **Final answer: 159.**

**Sample 3.** An inventory exercise concerns community center chairs. Start with 66 units. Add 10. Divide the current quantity by 2. Multiply the current quantity by 7. Add 27. How many units remain?

Steps: 76, 38, 266. **Final answer: 293.**

**Sample 4.** An inventory exercise concerns community center chairs. Start with 78 units. Add 14. Divide the current quantity by 4. Multiply the current quantity by 4. Add 59. How many units remain?

Steps: 92, 23, 92. **Final answer: 151.**

**Sample 5.** An inventory exercise concerns community center chairs. Start with 47 units. Add 43. Divide the current quantity by 2. Multiply the current quantity by 9. Add 28. How many units remain?

Steps: 90, 45, 405. **Final answer: 433.**

### History: mineral club sample boxes

**Sample 1.** An inventory exercise concerns mineral club sample boxes. Start with 199 units. Remove 61. Divide the current quantity by 2. Multiply the current quantity by 8. Divide the current quantity by 3. How many units remain?

Steps: 138, 69, 552. **Final answer: 184.**

**Sample 2.** An inventory exercise concerns mineral club sample boxes. Start with 186 units. Remove 46. Divide the current quantity by 5. Multiply the current quantity by 8. Divide the current quantity by 2. How many units remain?

Steps: 140, 28, 224. **Final answer: 112.**

**Sample 3.** An inventory exercise concerns mineral club sample boxes. Start with 184 units. Remove 14. Divide the current quantity by 2. Multiply the current quantity by 9. Divide the current quantity by 5. How many units remain?

Steps: 170, 85, 765. **Final answer: 153.**

**Sample 4.** An inventory exercise concerns mineral club sample boxes. Start with 142 units. Remove 22. Divide the current quantity by 3. Multiply the current quantity by 9. Divide the current quantity by 2. How many units remain?

Steps: 120, 40, 360. **Final answer: 180.**

**Sample 5.** An inventory exercise concerns mineral club sample boxes. Start with 151 units. Remove 15. Divide the current quantity by 2. Multiply the current quantity by 6. Divide the current quantity by 2. How many units remain?

Steps: 136, 68, 408. **Final answer: 204.**


## F34 / H34

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: toy shop blocks

**Sample 1.** An inventory exercise concerns toy shop blocks. Start with 66 units. Add 78. Divide the current quantity by 2. Multiply the current quantity by 2. Remove 33. How many units remain?

Steps: 144, 72, 144. **Final answer: 111.**

**Sample 2.** An inventory exercise concerns toy shop blocks. Start with 195 units. Add 69. Divide the current quantity by 3. Multiply the current quantity by 5. Remove 31. How many units remain?

Steps: 264, 88, 440. **Final answer: 409.**

**Sample 3.** An inventory exercise concerns toy shop blocks. Start with 83 units. Add 73. Divide the current quantity by 2. Multiply the current quantity by 7. Remove 72. How many units remain?

Steps: 156, 78, 546. **Final answer: 474.**

**Sample 4.** An inventory exercise concerns toy shop blocks. Start with 58 units. Add 50. Divide the current quantity by 3. Multiply the current quantity by 7. Remove 14. How many units remain?

Steps: 108, 36, 252. **Final answer: 238.**

**Sample 5.** An inventory exercise concerns toy shop blocks. Start with 179 units. Add 10. Divide the current quantity by 3. Multiply the current quantity by 4. Remove 74. How many units remain?

Steps: 189, 63, 252. **Final answer: 178.**

### History: dollhouse studio panels

**Sample 1.** An inventory exercise concerns dollhouse studio panels. Start with 196 units. Remove 60. Divide the current quantity by 2. Divide the current quantity by 2. Multiply the current quantity by 7. How many units remain?

Steps: 136, 68, 34. **Final answer: 238.**

**Sample 2.** An inventory exercise concerns dollhouse studio panels. Start with 158 units. Remove 10. Divide the current quantity by 2. Divide the current quantity by 2. Multiply the current quantity by 9. How many units remain?

Steps: 148, 74, 37. **Final answer: 333.**

**Sample 3.** An inventory exercise concerns dollhouse studio panels. Start with 178 units. Remove 22. Divide the current quantity by 2. Divide the current quantity by 2. Multiply the current quantity by 6. How many units remain?

Steps: 156, 78, 39. **Final answer: 234.**

**Sample 4.** An inventory exercise concerns dollhouse studio panels. Start with 196 units. Remove 58. Divide the current quantity by 3. Divide the current quantity by 2. Multiply the current quantity by 8. How many units remain?

Steps: 138, 46, 23. **Final answer: 184.**

**Sample 5.** An inventory exercise concerns dollhouse studio panels. Start with 106 units. Remove 10. Divide the current quantity by 2. Divide the current quantity by 3. Multiply the current quantity by 8. How many units remain?

Steps: 96, 48, 16. **Final answer: 128.**


## F35 / H35

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: recycling center bottles

**Sample 1.** An inventory exercise concerns recycling center bottles. Start with 115 units. Add 23. Divide the current quantity by 3. Multiply the current quantity by 9. Multiply the current quantity by 2. How many units remain?

Steps: 138, 46, 414. **Final answer: 828.**

**Sample 2.** An inventory exercise concerns recycling center bottles. Start with 133 units. Add 17. Divide the current quantity by 3. Multiply the current quantity by 9. Multiply the current quantity by 9. How many units remain?

Steps: 150, 50, 450. **Final answer: 4050.**

**Sample 3.** An inventory exercise concerns recycling center bottles. Start with 125 units. Add 17. Divide the current quantity by 2. Multiply the current quantity by 3. Multiply the current quantity by 4. How many units remain?

Steps: 142, 71, 213. **Final answer: 852.**

**Sample 4.** An inventory exercise concerns recycling center bottles. Start with 58 units. Add 74. Divide the current quantity by 3. Multiply the current quantity by 6. Multiply the current quantity by 4. How many units remain?

Steps: 132, 44, 264. **Final answer: 1056.**

**Sample 5.** An inventory exercise concerns recycling center bottles. Start with 53 units. Add 47. Divide the current quantity by 5. Multiply the current quantity by 4. Multiply the current quantity by 9. How many units remain?

Steps: 100, 20, 80. **Final answer: 720.**

### History: candle shop wicks

**Sample 1.** An inventory exercise concerns candle shop wicks. Start with 128 units. Multiply the current quantity by 5. Add 26. Add 61. Add 38. How many units remain?

Steps: 640, 666, 727. **Final answer: 765.**

**Sample 2.** An inventory exercise concerns candle shop wicks. Start with 170 units. Multiply the current quantity by 8. Add 62. Add 43. Add 34. How many units remain?

Steps: 1360, 1422, 1465. **Final answer: 1499.**

**Sample 3.** An inventory exercise concerns candle shop wicks. Start with 53 units. Multiply the current quantity by 8. Add 46. Add 59. Add 79. How many units remain?

Steps: 424, 470, 529. **Final answer: 608.**

**Sample 4.** An inventory exercise concerns candle shop wicks. Start with 119 units. Multiply the current quantity by 6. Add 45. Add 25. Add 66. How many units remain?

Steps: 714, 759, 784. **Final answer: 850.**

**Sample 5.** An inventory exercise concerns candle shop wicks. Start with 123 units. Multiply the current quantity by 9. Add 75. Add 75. Add 19. How many units remain?

Steps: 1107, 1182, 1257. **Final answer: 1276.**


## F36 / H36

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: festival wristbands

**Sample 1.** An inventory exercise concerns festival wristbands. Start with 65 units. Add 49. Divide the current quantity by 3. Multiply the current quantity by 7. Divide the current quantity by 2. How many units remain?

Steps: 114, 38, 266. **Final answer: 133.**

**Sample 2.** An inventory exercise concerns festival wristbands. Start with 118 units. Add 47. Divide the current quantity by 3. Multiply the current quantity by 6. Divide the current quantity by 3. How many units remain?

Steps: 165, 55, 330. **Final answer: 110.**

**Sample 3.** An inventory exercise concerns festival wristbands. Start with 140 units. Add 32. Divide the current quantity by 4. Multiply the current quantity by 6. Divide the current quantity by 2. How many units remain?

Steps: 172, 43, 258. **Final answer: 129.**

**Sample 4.** An inventory exercise concerns festival wristbands. Start with 177 units. Add 23. Divide the current quantity by 4. Multiply the current quantity by 7. Divide the current quantity by 2. How many units remain?

Steps: 200, 50, 350. **Final answer: 175.**

**Sample 5.** An inventory exercise concerns festival wristbands. Start with 175 units. Add 25. Divide the current quantity by 2. Multiply the current quantity by 7. Divide the current quantity by 2. How many units remain?

Steps: 200, 100, 700. **Final answer: 350.**

### History: trail crew stakes

**Sample 1.** An inventory exercise concerns trail crew stakes. Start with 119 units. Multiply the current quantity by 2. Add 25. Add 23. Remove 80. How many units remain?

Steps: 238, 263, 286. **Final answer: 206.**

**Sample 2.** An inventory exercise concerns trail crew stakes. Start with 95 units. Multiply the current quantity by 2. Add 50. Add 75. Remove 55. How many units remain?

Steps: 190, 240, 315. **Final answer: 260.**

**Sample 3.** An inventory exercise concerns trail crew stakes. Start with 63 units. Multiply the current quantity by 2. Add 38. Add 35. Remove 17. How many units remain?

Steps: 126, 164, 199. **Final answer: 182.**

**Sample 4.** An inventory exercise concerns trail crew stakes. Start with 78 units. Multiply the current quantity by 2. Add 10. Add 62. Remove 59. How many units remain?

Steps: 156, 166, 228. **Final answer: 169.**

**Sample 5.** An inventory exercise concerns trail crew stakes. Start with 89 units. Multiply the current quantity by 2. Add 28. Add 59. Remove 33. How many units remain?

Steps: 178, 206, 265. **Final answer: 232.**


## F37 / H37

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: school cafeteria trays

**Sample 1.** An inventory exercise concerns school cafeteria trays. Start with 195 units. Add 61. Divide the current quantity by 2. Divide the current quantity by 4. Multiply the current quantity by 5. How many units remain?

Steps: 256, 128, 32. **Final answer: 160.**

**Sample 2.** An inventory exercise concerns school cafeteria trays. Start with 188 units. Add 40. Divide the current quantity by 3. Divide the current quantity by 4. Multiply the current quantity by 9. How many units remain?

Steps: 228, 76, 19. **Final answer: 171.**

**Sample 3.** An inventory exercise concerns school cafeteria trays. Start with 171 units. Add 57. Divide the current quantity by 4. Divide the current quantity by 3. Multiply the current quantity by 8. How many units remain?

Steps: 228, 57, 19. **Final answer: 152.**

**Sample 4.** An inventory exercise concerns school cafeteria trays. Start with 60 units. Add 78. Divide the current quantity by 2. Divide the current quantity by 3. Multiply the current quantity by 7. How many units remain?

Steps: 138, 69, 23. **Final answer: 161.**

**Sample 5.** An inventory exercise concerns school cafeteria trays. Start with 159 units. Add 45. Divide the current quantity by 2. Divide the current quantity by 2. Multiply the current quantity by 8. How many units remain?

Steps: 204, 102, 51. **Final answer: 408.**

### History: embroidery club hoops

**Sample 1.** An inventory exercise concerns embroidery club hoops. Start with 197 units. Multiply the current quantity by 8. Add 17. Add 49. Multiply the current quantity by 5. How many units remain?

Steps: 1576, 1593, 1642. **Final answer: 8210.**

**Sample 2.** An inventory exercise concerns embroidery club hoops. Start with 194 units. Multiply the current quantity by 4. Add 14. Add 31. Multiply the current quantity by 6. How many units remain?

Steps: 776, 790, 821. **Final answer: 4926.**

**Sample 3.** An inventory exercise concerns embroidery club hoops. Start with 111 units. Multiply the current quantity by 5. Add 15. Add 16. Multiply the current quantity by 7. How many units remain?

Steps: 555, 570, 586. **Final answer: 4102.**

**Sample 4.** An inventory exercise concerns embroidery club hoops. Start with 48 units. Multiply the current quantity by 5. Add 79. Add 48. Multiply the current quantity by 4. How many units remain?

Steps: 240, 319, 367. **Final answer: 1468.**

**Sample 5.** An inventory exercise concerns embroidery club hoops. Start with 95 units. Multiply the current quantity by 2. Add 35. Add 48. Multiply the current quantity by 7. How many units remain?

Steps: 190, 225, 273. **Final answer: 1911.**


## F38 / H38

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: pet shelter towels

**Sample 1.** An inventory exercise concerns pet shelter towels. Start with 82 units. Remove 46. Add 62. Add 15. Multiply the current quantity by 3. How many units remain?

Steps: 36, 98, 113. **Final answer: 339.**

**Sample 2.** An inventory exercise concerns pet shelter towels. Start with 135 units. Remove 19. Add 38. Add 61. Multiply the current quantity by 6. How many units remain?

Steps: 116, 154, 215. **Final answer: 1290.**

**Sample 3.** An inventory exercise concerns pet shelter towels. Start with 188 units. Remove 13. Add 14. Add 59. Multiply the current quantity by 8. How many units remain?

Steps: 175, 189, 248. **Final answer: 1984.**

**Sample 4.** An inventory exercise concerns pet shelter towels. Start with 188 units. Remove 25. Add 31. Add 51. Multiply the current quantity by 4. How many units remain?

Steps: 163, 194, 245. **Final answer: 980.**

**Sample 5.** An inventory exercise concerns pet shelter towels. Start with 200 units. Remove 65. Add 48. Add 70. Multiply the current quantity by 3. How many units remain?

Steps: 135, 183, 253. **Final answer: 759.**

### History: paper mill bundles

**Sample 1.** An inventory exercise concerns paper mill bundles. Start with 176 units. Multiply the current quantity by 5. Add 59. Add 26. Divide the current quantity by 5. How many units remain?

Steps: 880, 939, 965. **Final answer: 193.**

**Sample 2.** An inventory exercise concerns paper mill bundles. Start with 112 units. Multiply the current quantity by 5. Add 10. Add 30. Divide the current quantity by 4. How many units remain?

Steps: 560, 570, 600. **Final answer: 150.**

**Sample 3.** An inventory exercise concerns paper mill bundles. Start with 119 units. Multiply the current quantity by 6. Add 64. Add 77. Divide the current quantity by 5. How many units remain?

Steps: 714, 778, 855. **Final answer: 171.**

**Sample 4.** An inventory exercise concerns paper mill bundles. Start with 82 units. Multiply the current quantity by 7. Add 47. Add 55. Divide the current quantity by 4. How many units remain?

Steps: 574, 621, 676. **Final answer: 169.**

**Sample 5.** An inventory exercise concerns paper mill bundles. Start with 122 units. Multiply the current quantity by 6. Add 57. Add 43. Divide the current quantity by 2. How many units remain?

Steps: 732, 789, 832. **Final answer: 416.**


## F39 / H39

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: hardware shop screws

**Sample 1.** An inventory exercise concerns hardware shop screws. Start with 84 units. Remove 49. Add 29. Remove 36. Multiply the current quantity by 4. How many units remain?

Steps: 35, 64, 28. **Final answer: 112.**

**Sample 2.** An inventory exercise concerns hardware shop screws. Start with 99 units. Remove 23. Add 43. Remove 76. Multiply the current quantity by 3. How many units remain?

Steps: 76, 119, 43. **Final answer: 129.**

**Sample 3.** An inventory exercise concerns hardware shop screws. Start with 163 units. Remove 58. Add 36. Remove 43. Multiply the current quantity by 8. How many units remain?

Steps: 105, 141, 98. **Final answer: 784.**

**Sample 4.** An inventory exercise concerns hardware shop screws. Start with 79 units. Remove 11. Add 73. Remove 36. Multiply the current quantity by 4. How many units remain?

Steps: 68, 141, 105. **Final answer: 420.**

**Sample 5.** An inventory exercise concerns hardware shop screws. Start with 140 units. Remove 19. Add 32. Remove 63. Multiply the current quantity by 5. How many units remain?

Steps: 121, 153, 90. **Final answer: 450.**

### History: water station filters

**Sample 1.** An inventory exercise concerns water station filters. Start with 160 units. Multiply the current quantity by 8. Add 66. Remove 50. Add 22. How many units remain?

Steps: 1280, 1346, 1296. **Final answer: 1318.**

**Sample 2.** An inventory exercise concerns water station filters. Start with 62 units. Multiply the current quantity by 7. Add 52. Remove 41. Add 46. How many units remain?

Steps: 434, 486, 445. **Final answer: 491.**

**Sample 3.** An inventory exercise concerns water station filters. Start with 136 units. Multiply the current quantity by 4. Add 28. Remove 13. Add 58. How many units remain?

Steps: 544, 572, 559. **Final answer: 617.**

**Sample 4.** An inventory exercise concerns water station filters. Start with 116 units. Multiply the current quantity by 5. Add 19. Remove 19. Add 39. How many units remain?

Steps: 580, 599, 580. **Final answer: 619.**

**Sample 5.** An inventory exercise concerns water station filters. Start with 176 units. Multiply the current quantity by 7. Add 29. Remove 31. Add 50. How many units remain?

Steps: 1232, 1261, 1230. **Final answer: 1280.**


## F40 / H40

**Decision:** unreviewed · **Reviewer:** ______ · **Reason/changes:** ______

### Probe: hiking club maps

**Sample 1.** An inventory exercise concerns hiking club maps. Start with 144 units. Remove 50. Add 66. Multiply the current quantity by 9. Add 35. How many units remain?

Steps: 94, 160, 1440. **Final answer: 1475.**

**Sample 2.** An inventory exercise concerns hiking club maps. Start with 45 units. Remove 28. Add 19. Multiply the current quantity by 4. Add 70. How many units remain?

Steps: 17, 36, 144. **Final answer: 214.**

**Sample 3.** An inventory exercise concerns hiking club maps. Start with 83 units. Remove 19. Add 21. Multiply the current quantity by 6. Add 67. How many units remain?

Steps: 64, 85, 510. **Final answer: 577.**

**Sample 4.** An inventory exercise concerns hiking club maps. Start with 173 units. Remove 17. Add 14. Multiply the current quantity by 5. Add 38. How many units remain?

Steps: 156, 170, 850. **Final answer: 888.**

**Sample 5.** An inventory exercise concerns hiking club maps. Start with 153 units. Remove 79. Add 48. Multiply the current quantity by 9. Add 57. How many units remain?

Steps: 74, 122, 1098. **Final answer: 1155.**

### History: model railway tracks

**Sample 1.** An inventory exercise concerns model railway tracks. Start with 78 units. Multiply the current quantity by 3. Add 21. Remove 31. Remove 74. How many units remain?

Steps: 234, 255, 224. **Final answer: 150.**

**Sample 2.** An inventory exercise concerns model railway tracks. Start with 54 units. Multiply the current quantity by 8. Add 33. Remove 21. Remove 13. How many units remain?

Steps: 432, 465, 444. **Final answer: 431.**

**Sample 3.** An inventory exercise concerns model railway tracks. Start with 128 units. Multiply the current quantity by 2. Add 27. Remove 30. Remove 48. How many units remain?

Steps: 256, 283, 253. **Final answer: 205.**

**Sample 4.** An inventory exercise concerns model railway tracks. Start with 134 units. Multiply the current quantity by 8. Add 78. Remove 60. Remove 13. How many units remain?

Steps: 1072, 1150, 1090. **Final answer: 1077.**

**Sample 5.** An inventory exercise concerns model railway tracks. Start with 111 units. Multiply the current quantity by 7. Add 46. Remove 21. Remove 44. How many units remain?

Steps: 777, 823, 802. **Final answer: 758.**
