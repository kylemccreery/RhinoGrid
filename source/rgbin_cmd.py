import Rhino
import scriptcontext
import System.Guid
import rhinoscriptsyntax as rs

from rhinogrid import *

__commandname__ = "rgbin"


def RunCommand( is_interactive ):
    corner = Rhino.Input.Custom.GetPoint()
    corner.SetCommandPrompt("Grid corner")
    units_length = 1
    units_width = 1
    units_height = 2
    
    length_opt = Rhino.Input.Custom.OptionInteger(units_length)
    width_opt = Rhino.Input.Custom.OptionInteger(units_width)
    height_opt = Rhino.Input.Custom.OptionInteger(units_height)

    corner.AddOptionInteger("Length", length_opt)
    corner.AddOptionInteger("Width", width_opt)
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

    full_top_object = build_full_bin(current_point, length_opt.CurrentValue, width_opt.CurrentValue, height_opt.CurrentValue)

    rs.EnableRedraw(True)

    return 0

#RunCommand(True)
