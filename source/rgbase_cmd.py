import Rhino
import scriptcontext
import System.Guid
import rhinoscriptsyntax as rs

from rhinogrid import *

__commandname__ = "rgbase"

def RunCommand( is_interactive ):
    corner = Rhino.Input.Custom.GetPoint()
    corner.SetCommandPrompt("Grid corner")
    units_width = 1
    units_length = 1
    width_opt = Rhino.Input.Custom.OptionInteger(units_width)
    length_opt = Rhino.Input.Custom.OptionInteger(units_length)

    corner.AddOptionInteger("Width", width_opt)
    corner.AddOptionInteger("Length", length_opt)

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

    full_base_object = build_tiled_base(current_point, length_opt.CurrentValue, width_opt.CurrentValue)

    rs.EnableRedraw(True)

    return 0

#RunCommand(True)
