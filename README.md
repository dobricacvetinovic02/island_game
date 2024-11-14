# island_game
Full-stack Challenge - Engineering Mastery Nordeus - Job Fair 2024


Bugs encountered:
1. recursive dfs on deepcopy of heights caused max recursion depth (changed to iterative later)
2. inverted coordinates so the islands were showing rotated (this caused more errors than I want to admit)
3. cells with height 1000 appeared as water because of the way I calculated the height
