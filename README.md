# island_game

Full-stack Challenge - Engineering Mastery Nordeus - Job Fair 2024

Bugs/problems encountered:

1. recursive dfs on a deepcopy of heights caused max recursion depth - I first solved this by using the original list of
   heights but later changed the recursive dfs to iterative one
2. inverted coordinates (x, y) so the islands were showing rotated, this caused more errors mainly about the way
   everything is calculated - I noticed this because the list of heights didn't match the visual representation I was
   getting, also the clicks on the map weren't corresponding to the appropriate cell.
3. cells with height 1000 appeared as water because of the way I calculated the height - solved this by changing the way
   of determining which tile belongs to which island (in previous versions I used to manipulate the height of the tile
   to
   determine which island it belongs to)
4. hearts representing remaining lives were not showing correctly (empty hearts did not show because I drew them over
   full ones) - solved by firstly drawing all hearts empty and only then drawing the correct number of full hearts.
5. clicking outside the island map caused the game to crash - this bug only occurred once, and I am not sure if it is
   fixed because I couldn't recreate it.
6. in some cases buttons/text were not showing correctly because I forgot to flip the screen.
7. not a bug but color pallet gave me trouble to get decent (still don't think it is).
8. when tried to make islands pulse when selected they just wouldn't because I didn't understand pygame.Surface and how
   it is drawn.

Ways I would test other projects:

1. Island detection - I would test the function that identifies the connected cells that represent the islands, if there
   is one and make sure islands are correctly detected.
2. Island representation - I would make sure that the islands are showing correctly according to the input list of
   heights (both in space and height-wise).
3. Handling input - I would try to test every input possible (clicking everything should work and every possible input
   should be handled correctly).
4. Edge cases - Testing the game by giving it edge case arguments (zero cells game, only cells with water game, only
   cells with height>0, only 1 cell with height > 0, etc.).
5. Game loop - testing if the game can be played repeatedly without errors.
6. UI - test if every interaction with the game gives apropriate feedback.
7. Give other people the game to test and give feedback on it - more heads are smarter than one and this way I think the
   bugs/missing features would be found the fastest.

Improvements I would make:

1. better graphics is the biggest and the most important improvement I would love to make
2. starting screen before the game is initially started
3. better ending screen
4. some settings (e.g. difficulty, colors, music, graphics)
5. showing the user in the end what each island's average height is and more quality of life features
6. levels of difficulty
7. adding a timer to each level
8. some hints or power ups for when the game becomes harder
9. multiplayer mode would be nice so the players can play each other in competitive mode and earn points by guessing
   first

How some factors could affect my solution:

1. map size - this would presumably only change the ROWS and COLS consts in settings.py (potentially also the TILESIZE)
2. number of lives - change to the number of lives would be easily implemented as only the lives attribute of the game
   class would need to be changed