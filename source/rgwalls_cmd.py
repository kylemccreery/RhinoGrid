import Rhino
import scriptcontext
import System.Guid
import rhinoscriptsyntax as rs

from rhinogrid import *

__commandname__ = "rgwalls"


def RunCommand( is_interactive ):
    corner = Rhino.Input.Custom.GetPoint()
    corner.SetCommandPrompt("Grid corner")
    units_width = 1
    units_length = 1
    units_height = 1
    
    width_opt = Rhino.Input.Custom.OptionInteger(units_width)
    length_opt = Rhino.Input.Custom.OptionInteger(units_length)
    height_opt = Rhino.Input.Custom.OptionInteger(units_height)

    corner.AddOptionInteger("Width", width_opt)
    corner.AddOptionInteger("Length", length_opt)
    corner.AddOptionInteger("Height", height_opt)

    while True:
       selected_corner = corner.Get()
       if corner.CommandResult() != Rhino.Commands.Result.Success:
           return corner.CommandResult()
       if scriptcontext.escape_test(False):
           return Rhino.Commands.Result.Cancel

       # Point was selected
       if selected_corner == Rhino.Input.GetResult.Point:
           current_point = corner.Point()
           break   
    
    rs.EnableRedraw(False)

    full_top_object = create_bin_walls(current_point, length_opt.CurrentValue, width_opt.CurrentValue, height_opt.CurrentValue)

    rs.EnableRedraw(True)

    return 0

#RunCommand(True)
