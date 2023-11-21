# RhinoGrid
Rhino python library and plugin using it to draw Gridfinity compatible bins, or just create the requisite parts to ease development of custom storage.

Can be installed by double clicking the .rhi file.

Written in python using rhinocommon and rhinoscriptsyntax.

Big thing to note is the surface_from_parallels function is incredibly jank but is meant to counteract the sweep2 and loft tendencies to create broken surfaces based on non-matching lengths of the composite lines. There is also a startling lack of built in chamfer functionality from rhinoscriptsyntax, so this both handles rounded chamfered edges and makes consistent vertical rounded rectangle polysurfaces. Since it works for both, I'm pretty in favor of using it over other more "correct" options.

Used the rs.Command for rectangle command for rounded rectangles since it was a lot simpler than actually drawing the curve manually. Abstracted the gross syntax of that command into the rounded_rectangle function for better readability.

Redraw is disabled per command to allow for not disabling it when using the gridfinity.py library to create other commands. Having redraw disabled makes the actual generation of the shapes much faster, but it is way less satisfying to watch.

Demo video of rgbin command (click thumbnail to watch on youtube):

[![Demo video of rgbin being used](https://img.youtube.com/vi/D340Aelf3B4/0.jpg)](https://www.youtube.com/watch?v=D340Aelf3B4)
