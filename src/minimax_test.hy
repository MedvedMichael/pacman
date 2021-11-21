(import [maze_generate [maze_generate]]
        [minimax [GameState generate_tree]])


(setv maze (maze_generate 5 5 (, 0 2) [(, 3 2)]))
(setv state (GameState maze))
(setv tree (generate_tree state (, 5 5)))
(print tree)