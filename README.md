# island_game
Full-stack Challenge - Engineering Mastery Nordeus - Job Fair 2024


Bugs/problems encountered:
1. recursive dfs on deepcopy of heights caused max recursion depth (changed to iterative later)
2. inverted coordinates so the islands were showing rotated (this caused more errors than I want to admit)
3. cells with height 1000 appeared as water because of the way I calculated the height
4. hearts representing remaining lives were not showing correctly (empty hearts did not show because I drew them over full ones)
5. clicking outside the island map caused the game to crash 
6. in some cases buttons/text were not showing correctly because I forgot to flip
7. not a bug but color pallet gave me trouble to get decent (still don't think it is)
8. when tried to make islands pulse when selected they just wouldn't 