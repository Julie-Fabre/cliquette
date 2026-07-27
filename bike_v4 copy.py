# =============================================================================
#  bike_v4  --  BikeCAD export + jig orientation
#
#  Section 1  parameters
#  Section 2  BikeCAD export body (verbatim geometry -- do not hand-edit)
#  Section 3  jig orientation, reference geometry, measurements
#
#  To update the frame: re-export from BikeCAD and replace everything between
#  the BEGIN/END EXPORT BODY markers. Section 3 is self-contained and derives
#  the seat tube angle from the geometry, so it needs no edits.
# =============================================================================

# ------------------------- Section 1: parameters -----------------------------

DOC_NAME = "bike_v4"

Head_Tube_id = 45.0
Head_Tube_top_id = 45.0
Head_Tube_mid_id = 42.6

Pinch_boss_length = 20.0
ST_slot_width = 2.0
ST_slot_depth = 35.0
ST_slot_hole_dia = 4.0
Waterbottle_boss_dia = 6.35
Waterbottle_boss_hole_dia = 4.2
Waterbottle_boss_length = 8.0

LogoThickness1 = 0.25
LogoThickness2 = 0.35
DOurl = "https://www.bikecad.ca/fcad/do/"
DOName = 'PD000'
BoltsExtra = ''
DOInsertR = 'PA445'
DOInsertL = 'PA426'

Bridge_hole_diameter = 6.0

BB_id = 44.8

# --- jig parameters (new) ---
Jig_dummy_dia = 6.0        # dia of reference tubes; keep small, HT pair is ~3 mm apart
Jig_dummy_overhang = 80.0  # how far reference geometry runs past the points it marks
Jig_marker_dia = 8.0       # intersection marker spheres
Jig_move_BB_to_origin = True

# -----------------------------------------------------------------------------

import os
import math
import tempfile

import Part
from FreeCAD import Base

try:
    import requests
except ImportError:
    requests = None
    print("requests not available -- dropout STEP parts will be skipped")

App.newDocument(DOC_NAME)
App.setActiveDocument(DOC_NAME)

yokeTool = False
dropTool = False


# =========================== BEGIN EXPORT BODY ===============================

# --- downloaded dropout hardware ---------------------------------------------

def fetch_step(filename, objname, placement):
    """Download a STEP part from bikecad.ca and add it. Returns True on success."""
    if requests is None:
        return False
    try:
        r = requests.get(DOurl + filename, timeout=20)
    except Exception as exc:
        print("download failed for %s: %s" % (filename, exc))
        return False
    if r.status_code != 200:
        print(filename + " not found")
        return False
    tmp = os.path.join(tempfile.gettempdir(), filename)
    with open(tmp, "wb") as fh:
        fh.write(r.content)
    shape = Part.Shape()
    shape.read(tmp)
    try:
        os.remove(tmp)
    except OSError:
        pass
    obj = App.ActiveDocument.addObject("Part::Feature", objname)
    obj.Shape = shape
    obj.Placement = placement
    return True


DROP_PARTS = [
    (DOName + "L.step",                   "DropoutL",       -67.5, (1.0, 1.0, 1.0)),
    (DOName + "R.step",                   "DropoutR",        67.5, (1.0, 1.0, 1.0)),
    (DOInsertR + ".step",                 "DropoutInsertR",  67.5, (0.003921569,) * 3),
    (DOInsertL + ".step",                 "DropoutInsertL", -67.5, (0.003921569,) * 3),
    (DOName + BoltsExtra + "BoltsR.step", "DropoutBoltsR",   67.5, (0.6, 0.6, 0.6)),
    (DOName + BoltsExtra + "BoltsL.step", "DropoutBoltsL",  -67.5, (0.6, 0.6, 0.6)),
]

dropout_objs = []
for _fname, _objname, _z, _colour in DROP_PARTS:
    _pl = Base.Placement(Base.Vector(365.0, 355.0, _z), Base.Rotation(-5.0, 0, 0))
    if fetch_step(_fname, _objname, _pl):
        dropout_objs.append((_objname, _colour))

# --- headset ------------------------------------------------------------------

App.ActiveDocument.addObject("Part::Revolution", "Headset")

bez0 = Part.BezierCurve()
bez0.setPoles([Base.Vector(25.0, 0.0, 0.0), Base.Vector(30.5, 0.0, 0.0), Base.Vector(30.5, -6.0, 0.0)])
bez1 = Part.BezierCurve()
bez1.setPoles([Base.Vector(30.5, -6.0, 0.0), Base.Vector(30.5, -12.0, 0.0), Base.Vector(25.0, -12.0, 0.0)])
headsetProfileWire0 = Part.Wire([
    Part.makeLine((22.5, 0.0, 0), (25.0, 0.0, 0)),
    bez0.toShape(),
    bez1.toShape(),
    Part.makeLine((25.0, -12.0, 0), (22.5, -12.0, 0)),
    Part.makeLine((22.5, -12.0, 0), (22.5, 0.0, 0.0)),
])

obj = App.ActiveDocument.addObject('Part::Feature', 'HS_profile')
obj.Shape = headsetProfileWire0
App.ActiveDocument.Headset.Source = App.ActiveDocument.HS_profile
App.ActiveDocument.Headset.Axis = (0, 1, 0)
App.ActiveDocument.Headset.Base = (0, 0, 0)
App.ActiveDocument.Headset.Angle = 360.0
App.ActiveDocument.Headset.Solid = True
App.ActiveDocument.Headset.Symmetric = False
App.ActiveDocument.Headset.Placement = Base.Placement(Base.Vector(1233.425, 737.083, 0), Base.Rotation(18.2, 0, 0))
App.ActiveDocument.HS_profile.Visibility = False

# --- head tube ----------------------------------------------------------------

App.ActiveDocument.addObject("Part::Revolution", "HT_tube")

htbackProfileWire0 = Part.Wire([
    Part.makeLine((1233.425, 737.083, 0), (1209.675, 729.275, 0)),
    Part.makeLine((1209.675, 729.275, 0), (1208.114, 734.025, 0)),
    Part.makeLine((1208.114, 734.025, 0), (1206.849, 741.714, 0)),
    Part.makeLine((1206.849, 741.714, 0), (1174.178, 841.081, 0)),
    Part.makeLine((1174.178, 841.081, 0), (1170.633, 848.021, 0)),
    Part.makeLine((1170.633, 848.021, 0), (1169.072, 852.771, 0)),
    Part.makeLine((1169.072, 852.771, 0), (1192.821, 860.58, 0)),
    Part.makeLine((1192.821, 860.58, 0), (1233.425, 737.083, 0.0)),
])

obj = App.ActiveDocument.addObject('Part::Feature', 'HT_profile')
obj.Shape = htbackProfileWire0
App.ActiveDocument.HT_tube.Source = App.ActiveDocument.HT_profile
App.ActiveDocument.HT_tube.Axis = (-40.604, 123.497, 0.0)
App.ActiveDocument.HT_tube.Base = (1233.425, 737.083, 0.0)
App.ActiveDocument.HT_tube.Angle = 360.0
App.ActiveDocument.HT_tube.Solid = True
App.ActiveDocument.HT_tube.Symmetric = False
App.ActiveDocument.HT_profile.Visibility = False

App.ActiveDocument.addObject("Part::Cylinder", "HT_cut1")
App.ActiveDocument.HT_cut1.Radius = Head_Tube_id / 2
App.ActiveDocument.HT_cut1.Height = 6.0
App.ActiveDocument.HT_cut1.Placement = Base.Placement(Base.Vector(1233.737, 736.133, 0.0), Base.Rotation(108.2, 90, 0))
App.ActiveDocument.addObject("Part::Cylinder", "HT_cut2")
App.ActiveDocument.HT_cut2.Radius = Head_Tube_top_id / 2
App.ActiveDocument.HT_cut2.Height = 10.0
App.ActiveDocument.HT_cut2.Placement = Base.Placement(Base.Vector(1194.383, 855.83, 0.0), Base.Rotation(108.2, 90, 0))
App.ActiveDocument.addObject("Part::Cylinder", "HT_cut3")
App.ActiveDocument.HT_cut3.Radius = min(Head_Tube_id, Head_Tube_mid_id, Head_Tube_top_id) / 2
App.ActiveDocument.HT_cut3.Height = 130.0
App.ActiveDocument.HT_cut3.Placement = Base.Placement(Base.Vector(1233.425, 737.083, 0.0), Base.Rotation(108.2, 90, 0))
App.activeDocument().addObject("Part::MultiFuse", "HT_cut")
App.activeDocument().HT_cut.Shapes = [App.activeDocument().HT_cut1,
                                      App.activeDocument().HT_cut2,
                                      App.activeDocument().HT_cut3]
App.activeDocument().addObject("Part::Cut", "HT_Finished")
App.ActiveDocument.ActiveObject.Base = App.activeDocument().HT_tube
App.ActiveDocument.ActiveObject.Tool = App.activeDocument().HT_cut

# --- drive-side chainstay -----------------------------------------------------

obj = App.ActiveDocument.addObject("Part::Feature", "dCS3D_CL")
WireCLdCS = Part.makeLine((479.55, 321.89, 71.5), (813.125, 276.291, 19.136))
obj.Shape = WireCLdCS
profiledCS1 = App.ActiveDocument.addObject("Part::Feature", "dCS_XSec1")
profiledCS1.Shape = Part.makeCircle(6.25, Base.Vector(479.55, 321.89, 71.5), Base.Vector(0.991, -0.135, -0.166))
profiledCS2 = App.ActiveDocument.addObject("Part::Feature", "dCS_XSec2")
profiledCS2.Shape = Part.Ellipse(Base.Vector(709.463, 305.601, 32.808), Base.Vector(708.758, 290.739, 40.697), Base.Vector(707.431, 290.739, 32.808)).toShape()
profiledCS3 = App.ActiveDocument.addObject("Part::Feature", "dCS_XSec3")
profiledCS3.Shape = Part.Ellipse(Base.Vector(770.175, 297.302, 22.5), Base.Vector(769.471, 282.44, 30.389), Base.Vector(768.144, 282.44, 22.5)).toShape()
profiledCS4 = App.ActiveDocument.addObject("Part::Feature", "dCS_XSec4")
profiledCS4.Shape = Part.Ellipse(Base.Vector(795.682, 293.815, 18.169), Base.Vector(794.977, 278.953, 26.058), Base.Vector(793.65, 278.953, 18.169)).toShape()
if dropTool:
    sweepdCS = App.ActiveDocument.addObject('Part::Sweep', 'dCS_tube1')
else:
    sweepdCS = App.ActiveDocument.addObject('Part::Sweep', 'dCS_tube')
sweepdCS.Sections = [profiledCS1, profiledCS2, profiledCS3]
sweepdCS.Spine = App.ActiveDocument.getObject('dCS3D_CL')
sweepdCS.Solid = True
sweepdCS.Frenet = False
sweepdCS.Transition = 2

App.ActiveDocument.recompute()
App.activeDocument().dCS3D_CL.Visibility = False
App.activeDocument().dCS_XSec1.Visibility = False
if dropTool:
    App.activeDocument().addObject("Part::Cut", 'dCS_tube')
    App.ActiveDocument.ActiveObject.Base = App.activeDocument().dCS_tube1
    App.ActiveDocument.ActiveObject.Tool = App.activeDocument().DropoutTOOL
    App.ActiveDocument.recompute()
App.activeDocument().dCS_XSec2.Visibility = False
App.activeDocument().dCS_XSec3.Visibility = False
App.activeDocument().dCS_XSec4.Visibility = False

# --- drive-side seatstay ------------------------------------------------------

obj = App.ActiveDocument.addObject("Part::Feature", "dSS3D_CL")
WireCLdSS = Part.makeLine((384.089, 412.555, 71.5), (660.355, 719.367, 17.0))
obj.Shape = WireCLdSS
profiledSS1 = App.ActiveDocument.addObject("Part::Feature", "dSS_XSec1")
profiledSS1.Shape = Part.makeCircle(6.25, Base.Vector(384.089, 412.555, 71.5), Base.Vector(0.669, 0.743, -0.131))
profiledSS2 = App.ActiveDocument.addObject("Part::Feature", "dSS_XSec2")
profiledSS2.Shape = Part.makeCircle(8.0, Base.Vector(551.375, 598.338, 38.499), Base.Vector(0.669, 0.743, -0.131))
profiledSS3 = App.ActiveDocument.addObject("Part::Feature", "dSS_XSec3")
profiledSS3.Shape = Part.makeCircle(8.0, Base.Vector(660.355, 719.367, 17.0), Base.Vector(0.669, 0.743, -0.131))
profiledSS4 = App.ActiveDocument.addObject("Part::Feature", "dSS_XSec4")
profiledSS4.Shape = Part.makeCircle(8.0, Base.Vector(660.355, 719.367, 17.0), Base.Vector(0.669, 0.743, -0.131))
if dropTool:
    sweepdSS = App.ActiveDocument.addObject('Part::Sweep', 'dSS_tube1')
else:
    sweepdSS = App.ActiveDocument.addObject('Part::Sweep', 'dSS_tube')
sweepdSS.Sections = [profiledSS1, profiledSS2, profiledSS3]
sweepdSS.Spine = App.ActiveDocument.getObject('dSS3D_CL')
sweepdSS.Solid = True
sweepdSS.Frenet = False
sweepdSS.Transition = 2

App.ActiveDocument.recompute()
App.activeDocument().dSS3D_CL.Visibility = False
App.activeDocument().dSS_XSec1.Visibility = False
if dropTool:
    App.activeDocument().addObject("Part::Cut", 'dSS_tube')
    App.ActiveDocument.ActiveObject.Base = App.activeDocument().dSS_tube1
    App.ActiveDocument.ActiveObject.Tool = App.activeDocument().DropoutTOOL
    App.ActiveDocument.recompute()
App.activeDocument().dSS_XSec2.Visibility = False
App.activeDocument().dSS_XSec3.Visibility = False
App.activeDocument().dSS_XSec4.Visibility = False

# --- non-drive-side chainstay -------------------------------------------------

obj = App.ActiveDocument.addObject("Part::Feature", "nCS3D_CL")
WireCLnCS = Part.makeLine((479.55, 321.89, -71.5), (813.125, 276.291, -19.136))
obj.Shape = WireCLnCS
profilenCS1 = App.ActiveDocument.addObject("Part::Feature", "nCS_XSec1")
profilenCS1.Shape = Part.makeCircle(6.25, Base.Vector(479.55, 321.89, -71.5), Base.Vector(0.991, -0.135, 0.166))
profilenCS2 = App.ActiveDocument.addObject("Part::Feature", "nCS_XSec2")
profilenCS2.Shape = Part.Ellipse(Base.Vector(709.463, 305.601, -32.808), Base.Vector(706.104, 290.739, -24.919), Base.Vector(707.431, 290.739, -32.808)).toShape()
profilenCS3 = App.ActiveDocument.addObject("Part::Feature", "nCS_XSec3")
profilenCS3.Shape = Part.Ellipse(Base.Vector(770.175, 297.302, -22.5), Base.Vector(766.816, 282.44, -14.611), Base.Vector(768.144, 282.44, -22.5)).toShape()
profilenCS4 = App.ActiveDocument.addObject("Part::Feature", "nCS_XSec4")
profilenCS4.Shape = Part.Ellipse(Base.Vector(795.682, 293.815, -18.169), Base.Vector(792.323, 278.953, -10.28), Base.Vector(793.65, 278.953, -18.169)).toShape()
if dropTool:
    sweepnCS = App.ActiveDocument.addObject('Part::Sweep', 'nCS_tube1')
else:
    sweepnCS = App.ActiveDocument.addObject('Part::Sweep', 'nCS_tube')
sweepnCS.Sections = [profilenCS1, profilenCS2, profilenCS3]
sweepnCS.Spine = App.ActiveDocument.getObject('nCS3D_CL')
sweepnCS.Solid = True
sweepnCS.Frenet = False
sweepnCS.Transition = 2

App.ActiveDocument.recompute()
App.activeDocument().nCS3D_CL.Visibility = False
App.activeDocument().nCS_XSec1.Visibility = False
if dropTool:
    App.activeDocument().addObject("Part::Cut", 'nCS_tube')
    App.ActiveDocument.ActiveObject.Base = App.activeDocument().nCS_tube1
    App.ActiveDocument.ActiveObject.Tool = App.activeDocument().DropoutTOOL
    App.ActiveDocument.recompute()
App.activeDocument().nCS_XSec2.Visibility = False
App.activeDocument().nCS_XSec3.Visibility = False
App.activeDocument().nCS_XSec4.Visibility = False

# --- non-drive-side seatstay --------------------------------------------------

obj = App.ActiveDocument.addObject("Part::Feature", "nSS3D_CL")
WireCLnSS = Part.makeLine((384.089, 412.555, -71.5), (660.355, 719.367, -17.0))
obj.Shape = WireCLnSS
profilenSS1 = App.ActiveDocument.addObject("Part::Feature", "nSS_XSec1")
profilenSS1.Shape = Part.makeCircle(6.25, Base.Vector(384.089, 412.555, -71.5), Base.Vector(0.669, 0.743, 0.131))
profilenSS2 = App.ActiveDocument.addObject("Part::Feature", "nSS_XSec2")
profilenSS2.Shape = Part.makeCircle(8.0, Base.Vector(551.375, 598.338, -38.499), Base.Vector(0.669, 0.743, 0.131))
profilenSS3 = App.ActiveDocument.addObject("Part::Feature", "nSS_XSec3")
profilenSS3.Shape = Part.makeCircle(8.0, Base.Vector(660.355, 719.367, -17.0), Base.Vector(0.669, 0.743, 0.131))
profilenSS4 = App.ActiveDocument.addObject("Part::Feature", "nSS_XSec4")
profilenSS4.Shape = Part.makeCircle(8.0, Base.Vector(660.355, 719.367, -17.0), Base.Vector(0.669, 0.743, 0.131))
if dropTool:
    sweepnSS = App.ActiveDocument.addObject('Part::Sweep', 'nSS_tube1')
else:
    sweepnSS = App.ActiveDocument.addObject('Part::Sweep', 'nSS_tube')
sweepnSS.Sections = [profilenSS1, profilenSS2, profilenSS3]
sweepnSS.Spine = App.ActiveDocument.getObject('nSS3D_CL')
sweepnSS.Solid = True
sweepnSS.Frenet = False
sweepnSS.Transition = 2

App.ActiveDocument.recompute()
App.activeDocument().nSS3D_CL.Visibility = False
App.activeDocument().nSS_XSec1.Visibility = False
if dropTool:
    App.activeDocument().addObject("Part::Cut", 'nSS_tube')
    App.ActiveDocument.ActiveObject.Base = App.activeDocument().nSS_tube1
    App.ActiveDocument.ActiveObject.Tool = App.activeDocument().DropoutTOOL
    App.ActiveDocument.recompute()
App.activeDocument().nSS_XSec2.Visibility = False
App.activeDocument().nSS_XSec3.Visibility = False
App.activeDocument().nSS_XSec4.Visibility = False

# --- bridges ------------------------------------------------------------------

myssB = Part.makeCylinder(8.0, 58.869, Base.Vector(597.323, 649.366, 29.435), Base.Vector(0.0, 0.0, -58.869))
obj = App.ActiveDocument.addObject('Part::Feature', 'ssBridge')
obj.Shape = myssB
mycsB = Part.makeCylinder(9.0, 56.66, Base.Vector(733.808, 287.134, 28.33), Base.Vector(0.0, 0.0, -56.66))
obj = App.ActiveDocument.addObject('Part::Feature', 'csBridge')
obj.Shape = mycsB

# --- down tube ----------------------------------------------------------------

profileDT1 = App.ActiveDocument.addObject("Part::Feature", "DT_XSec1")
profileDT1.Shape = Part.makeCircle(17.5, Base.Vector(793.309, 279.0, 0.0), Base.Vector(0.64381206, 0.7651837, 0))
WireCLDT = Part.makeLine((793.309, 279.0, 0.0), (1218.058, 783.822, 0.0))
spineDT = App.ActiveDocument.addObject("Part::Feature", "DT_CLine")
spineDT.Shape = WireCLDT
sweepDT = App.ActiveDocument.addObject('Part::Sweep', 'DT_tube')
sweepDT.Sections = [profileDT1]
sweepDT.Spine = spineDT
sweepDT.Solid = True
sweepDT.Frenet = False
sweepDT.Transition = 2
App.ActiveDocument.recompute()
App.activeDocument().DT_CLine.Visibility = False
App.activeDocument().DT_XSec1.Visibility = False

# --- seat tube ----------------------------------------------------------------

profileST1 = App.ActiveDocument.addObject("Part::Feature", "ST_XSec1")
profileST1.Shape = Part.makeCircle(14.3, Base.Vector(793.309, 279.0, 0.0), Base.Vector(-0.2890318, 0.9573195, 0))
WireCLST = Part.makeLine((793.309, 279.0, 0.0), (648.794, 757.66, 0.0))
profileST3 = App.ActiveDocument.addObject("Part::Feature", "ST_XSec3")
profileST3.Shape = Part.makeCircle(14.9, Base.Vector(648.794, 757.66, 0.0), Base.Vector(-0.2890318, 0.9573195, 0))

spineST = App.ActiveDocument.addObject("Part::Feature", "ST_CLine")
spineST.Shape = WireCLST
sweepST = App.ActiveDocument.addObject('Part::Sweep', 'ST_tube')
sweepST.Sections = [profileST1, profileST3]
sweepST.Spine = spineST
sweepST.Solid = True
sweepST.Frenet = False
sweepST.Transition = 2
App.ActiveDocument.recompute()
App.activeDocument().ST_CLine.Visibility = False
App.activeDocument().ST_XSec1.Visibility = False
App.activeDocument().ST_XSec3.Visibility = False

# --- top tube -----------------------------------------------------------------

profileTT1 = App.ActiveDocument.addObject("Part::Feature", "TT_XSec1")
profileTT1.Shape = Part.makeCircle(14.3, Base.Vector(660.355, 719.367, 0.0), Base.Vector(0.97863716, 0.20559515, 0))
WireCLTT = Part.makeLine((660.355, 719.367, 0.0), (1201.848, 833.125, 0.0))
spineTT = App.ActiveDocument.addObject("Part::Feature", "TT_CLine")
spineTT.Shape = WireCLTT
sweepTT = App.ActiveDocument.addObject('Part::Sweep', 'TT_tube')
sweepTT.Sections = [profileTT1]
sweepTT.Spine = spineTT
sweepTT.Solid = True
sweepTT.Frenet = False
sweepTT.Transition = 2
App.ActiveDocument.recompute()
App.activeDocument().TT_CLine.Visibility = False
App.activeDocument().TT_XSec1.Visibility = False

# --- bottom bracket -----------------------------------------------------------

GBox = False
myBB = Part.makeCylinder(25.4, 73.0, Base.Vector(793.309, 279.0, -36.5), Base.Vector(0, 0, 1))
obj = App.ActiveDocument.addObject('Part::Feature', 'BBGearBoxCut')
obj.Shape = myBB
myBBid = Part.makeCylinder(BB_id / 2, 146.0, Base.Vector(793.309, 279.0, -73.0), Base.Vector(0, 0, 1))
obj = App.ActiveDocument.addObject('Part::Feature', 'BBid')
obj.Shape = myBBid
App.activeDocument().addObject("Part::Cut", "BB")
App.ActiveDocument.ActiveObject.Base = App.activeDocument().BBGearBoxCut
App.ActiveDocument.ActiveObject.Tool = App.activeDocument().BBid

# --- seatpost -----------------------------------------------------------------

profile = Part.makeCircle(15.8, Base.Vector(0, 0, 0), Base.Vector(1, 0, 0))
profile = Part.Wire(profile)
profile = Part.Face(profile)
profile = profile.extrude(Base.Vector(-350.0, 0, 0))
profile.rotate(Base.Vector(0, 0, 0), Base.Vector(0, 0, 1), 106.8)
profile.translate(Base.Vector(606.621, 897.341, 0.0))
obj = App.ActiveDocument.addObject("Part::Feature", "SPost_extrude")
obj.Shape = profile

# --- seatpost clamp -----------------------------------------------------------

App.ActiveDocument.addObject("Part::Cylinder", "STPinchBossHole")
App.ActiveDocument.STPinchBossHole.Radius = 5.0
App.ActiveDocument.STPinchBossHole.Height = 5
App.ActiveDocument.STPinchBossHole.Placement = Base.Placement(Base.Vector(632.483, 745.946, Pinch_boss_length / 2 - 4), Base.Rotation(0, 0, 0))
App.ActiveDocument.addObject("Part::Cylinder", "STPinchBossThruHole")
App.ActiveDocument.STPinchBossThruHole.Radius = 3
App.ActiveDocument.STPinchBossThruHole.Height = Pinch_boss_length * 2
App.ActiveDocument.STPinchBossThruHole.Placement = Base.Placement(Base.Vector(632.483, 745.946, -Pinch_boss_length), Base.Rotation(0, 0, 0))
obj = App.ActiveDocument.addObject('Part::Feature', 'STslot')
obj.Shape = Part.makeBox(ST_slot_depth + 5, 34.0, ST_slot_width, Base.Vector(-ST_slot_depth - 5, 0.0, 0))
App.ActiveDocument.STslot.Placement = Base.Placement(Base.Vector(647.348, 762.446, -ST_slot_width / 2), Base.Rotation(106.8, 0, 0))
App.ActiveDocument.addObject("Part::Cylinder", "STslotHole")
App.ActiveDocument.STslotHole.Radius = ST_slot_hole_dia / 2
App.ActiveDocument.STslotHole.Height = 34.0
App.ActiveDocument.STslotHole.Placement = Base.Placement(Base.Vector(647.348 - (ST_slot_depth + 5) * -0.289, 762.446 - (ST_slot_depth + 5) * 0.957, 0), Base.Rotation(16.8, -90, 0))
profileSTclampTop1 = Part.makeCircle(18.0, Base.Vector(652.84, 744.257, 0.0), Base.Vector(-0.2890318, 0.9573195, 0))
profileSTclampTop1 = Part.Face(Part.Wire([profileSTclampTop1]))
STclampTop = profileSTclampTop1.extrude(Base.Vector(-4.335476954167072, 14.359792462981009, 0))
obj = App.ActiveDocument.addObject('Part::Feature', 'SeatpostClampTop')
obj.Shape = STclampTop

bez0 = Part.BezierCurve()
bez0.setPoles([Base.Vector(632.581, 738.385, 0.0), Base.Vector(630.218, 738.385, 0.0), Base.Vector(628.035, 739.919, 0.0), Base.Vector(627.317, 742.297, 0.0)])
bez1 = Part.BezierCurve()
bez1.setPoles([Base.Vector(626.161, 746.126, 0.0), Base.Vector(625.283, 749.034, 0.0), Base.Vector(626.929, 752.103, 0.0), Base.Vector(629.837, 752.981, 0.0)])
bez2 = Part.BezierCurve()
bez2.setPoles([Base.Vector(643.239, 757.027, 0.0), Base.Vector(643.769, 757.187, 0.0), Base.Vector(644.305, 757.264, 0.0), Base.Vector(644.831, 757.264, 0.0)])
bez3 = Part.BezierCurve()
bez3.setPoles([Base.Vector(644.831, 757.264, 0.0), Base.Vector(647.193, 757.264, 0.0), Base.Vector(649.376, 755.73, 0.0), Base.Vector(650.094, 753.352, 0.0)])
bez4 = Part.BezierCurve()
bez4.setPoles([Base.Vector(651.25, 749.523, 0.0), Base.Vector(652.128, 746.615, 0.0), Base.Vector(650.483, 743.546, 0.0), Base.Vector(647.575, 742.668, 0.0)])
bez5 = Part.BezierCurve()
bez5.setPoles([Base.Vector(634.172, 738.621, 0.0), Base.Vector(633.642, 738.461, 0.0), Base.Vector(633.107, 738.385, 0.0), Base.Vector(632.581, 738.385, 0.0)])
PinchBoss0 = Part.Wire([
    bez0.toShape(),
    Part.makeLine((627.317, 742.297, 0), (626.161, 746.126, 0)),
    bez1.toShape(),
    Part.makeLine((629.837, 752.981, 0), (643.239, 757.027, 0)),
    bez2.toShape(),
    bez3.toShape(),
    Part.makeLine((650.094, 753.352, 0), (651.25, 749.523, 0)),
    bez4.toShape(),
    Part.makeLine((647.575, 742.668, 0), (634.172, 738.621, 0)),
    bez5.toShape(),
])

PinchBoss = Part.Face([PinchBoss0, ])
PinchBoss.translate(Base.Vector(0, 0, -Pinch_boss_length / 2))
PinchBoss = PinchBoss.extrude(Base.Vector(0, 0, Pinch_boss_length))
obj = App.ActiveDocument.addObject('Part::Feature', 'STPinchBoss')
obj.Shape = PinchBoss

App.ActiveDocument.addObject("Part::Fuse", "SPC")
App.ActiveDocument.SPC.Base = App.activeDocument().SeatpostClampTop
App.ActiveDocument.SPC.Tool = App.ActiveDocument.STPinchBoss
Gui.ActiveDocument.hide("SeatpostClampTop")
Gui.ActiveDocument.hide("STPinchBoss")
App.ActiveDocument.addObject('Part::Extrusion', 'SPCcut')
f = App.ActiveDocument.getObject('SPCcut')
f.Base = App.ActiveDocument.getObject('ST_XSec3')
f.DirMode = "Custom"
f.Dir = App.Vector(0.289, -0.957, 0.0)
f.DirLink = None
f.LengthFwd = 15.0
f.LengthRev = 0.0
f.Solid = True
f.Reversed = False
f.Symmetric = False
f.TaperAngle = 0.0
f.TaperAngleRev = 0.0
App.ActiveDocument.addObject("Part::Cut", "SeatptClamp")
App.ActiveDocument.SeatptClamp.Base = App.ActiveDocument.SPC
App.ActiveDocument.SeatptClamp.Tool = App.ActiveDocument.STslot
Gui.ActiveDocument.SPC.Visibility = False
Gui.ActiveDocument.STslot.Visibility = False
App.ActiveDocument.addObject("Part::Cut", "SeatpstClamp")
App.ActiveDocument.SeatpstClamp.Base = App.ActiveDocument.SeatptClamp
App.ActiveDocument.SeatpstClamp.Tool = App.ActiveDocument.SPCcut
Gui.ActiveDocument.SeatptClamp.Visibility = False
Gui.ActiveDocument.SPCcut.Visibility = False
App.ActiveDocument.addObject("Part::Cut", "SeatpostClamp")
App.ActiveDocument.SeatpostClamp.Base = App.ActiveDocument.SeatpstClamp
App.ActiveDocument.SeatpostClamp.Tool = App.ActiveDocument.SPost_extrude
Gui.ActiveDocument.SeatpstClamp.Visibility = False
Gui.ActiveDocument.SPost_extrude.Visibility = False
App.activeDocument().addObject("Part::MultiFuse", "SPCCuts")
App.activeDocument().SPCCuts.Shapes = [App.activeDocument().STPinchBossHole,
                                       App.activeDocument().STPinchBossThruHole]
App.activeDocument().addObject("Part::Cut", "Seatpost_clamp_finished")
App.ActiveDocument.ActiveObject.Base = App.activeDocument().SeatpostClamp
App.ActiveDocument.ActiveObject.Tool = App.activeDocument().SPCCuts
App.ActiveDocument.recompute()

# --- water bottle bosses: seat tube -------------------------------------------

App.ActiveDocument.addObject("Part::Cylinder", "WBbossSEATTUBEm00")
App.ActiveDocument.WBbossSEATTUBEm00.Radius = 4.5
App.ActiveDocument.WBbossSEATTUBEm00.Height = 2.0
App.ActiveDocument.addObject("Part::Cylinder", "WBbossSEATTUBEmp00")
App.ActiveDocument.WBbossSEATTUBEmp00.Radius = Waterbottle_boss_dia / 2
App.ActiveDocument.WBbossSEATTUBEmp00.Height = Waterbottle_boss_length - 2.0
App.ActiveDocument.WBbossSEATTUBEmp00.Placement = Base.Placement(Base.Vector(0, 0, 2.0 - Waterbottle_boss_length), Base.Rotation(0, 0, 0))
App.ActiveDocument.addObject("Part::Cylinder", "WBbossHSEATTUBEmh00")
App.ActiveDocument.WBbossHSEATTUBEmh00.Radius = Waterbottle_boss_hole_dia / 2
App.ActiveDocument.WBbossHSEATTUBEmh00.Height = Waterbottle_boss_length + 1
App.ActiveDocument.WBbossHSEATTUBEmh00.Placement = Base.Placement(Base.Vector(0, 0, 2.0 - Waterbottle_boss_length), Base.Rotation(0, 0, 0))
App.ActiveDocument.addObject("Part::Cylinder", "WBbossSEATTUBEm10")
App.ActiveDocument.WBbossSEATTUBEm10.Radius = 4.5
App.ActiveDocument.WBbossSEATTUBEm10.Height = 2.0
App.ActiveDocument.WBbossSEATTUBEm10.Placement = Base.Placement(Base.Vector(64.0, 0, 0), Base.Rotation(0, 0, 0))
App.ActiveDocument.addObject("Part::Cylinder", "WBbossSEATTUBEmp10")
App.ActiveDocument.WBbossSEATTUBEmp10.Radius = Waterbottle_boss_dia / 2
App.ActiveDocument.WBbossSEATTUBEmp10.Height = Waterbottle_boss_length - 2.0
App.ActiveDocument.WBbossSEATTUBEmp10.Placement = Base.Placement(Base.Vector(64.0, 0, 2.0 - Waterbottle_boss_length), Base.Rotation(0, 0, 0))
App.ActiveDocument.addObject("Part::Cylinder", "WBbossHSEATTUBEmh10")
App.ActiveDocument.WBbossHSEATTUBEmh10.Radius = Waterbottle_boss_hole_dia / 2
App.ActiveDocument.WBbossHSEATTUBEmh10.Height = Waterbottle_boss_length + 1
App.ActiveDocument.WBbossHSEATTUBEmh10.Placement = Base.Placement(Base.Vector(64.0, 0, 2.0 - Waterbottle_boss_length), Base.Rotation(0, 0, 0))
App.activeDocument().addObject("Part::MultiFuse", "WBbossSEATTUBEm0")
App.activeDocument().WBbossSEATTUBEm0.Shapes = [App.activeDocument().WBbossSEATTUBEm00,
                                                App.activeDocument().WBbossSEATTUBEmp00,
                                                App.activeDocument().WBbossSEATTUBEm10,
                                                App.activeDocument().WBbossSEATTUBEmp10]
App.ActiveDocument.WBbossSEATTUBEm0.Placement = Base.Placement(Base.Vector(766.696, 417.206, 0.0), Base.Rotation(106.731, 0, 90))
App.activeDocument().addObject("Part::MultiFuse", "WBbossHolesSEATTUBEm0")
App.activeDocument().WBbossHolesSEATTUBEm0.Shapes = [App.activeDocument().WBbossHSEATTUBEmh00,
                                                     App.activeDocument().WBbossHSEATTUBEmh10]
App.ActiveDocument.WBbossHolesSEATTUBEm0.Placement = Base.Placement(Base.Vector(766.696, 417.206, 0.0), Base.Rotation(106.731, 0, 90))
App.activeDocument().addObject("Part::Cut", "WBbossDrilledSEATTUBEm0")
App.ActiveDocument.ActiveObject.Base = App.activeDocument().WBbossSEATTUBEm0
App.ActiveDocument.ActiveObject.Tool = App.activeDocument().WBbossHolesSEATTUBEm0
App.ActiveDocument.recompute()

# --- water bottle bosses: down tube -------------------------------------------

App.ActiveDocument.addObject("Part::Cylinder", "WBbossDOWNTUBEm00")
App.ActiveDocument.WBbossDOWNTUBEm00.Radius = 4.5
App.ActiveDocument.WBbossDOWNTUBEm00.Height = 2.0
App.ActiveDocument.addObject("Part::Cylinder", "WBbossDOWNTUBEmp00")
App.ActiveDocument.WBbossDOWNTUBEmp00.Radius = Waterbottle_boss_dia / 2
App.ActiveDocument.WBbossDOWNTUBEmp00.Height = Waterbottle_boss_length - 2.0
App.ActiveDocument.WBbossDOWNTUBEmp00.Placement = Base.Placement(Base.Vector(0, 0, 2.0 - Waterbottle_boss_length), Base.Rotation(0, 0, 0))
App.ActiveDocument.addObject("Part::Cylinder", "WBbossHDOWNTUBEmh00")
App.ActiveDocument.WBbossHDOWNTUBEmh00.Radius = Waterbottle_boss_hole_dia / 2
App.ActiveDocument.WBbossHDOWNTUBEmh00.Height = Waterbottle_boss_length + 1
App.ActiveDocument.WBbossHDOWNTUBEmh00.Placement = Base.Placement(Base.Vector(0, 0, 2.0 - Waterbottle_boss_length), Base.Rotation(0, 0, 0))
App.ActiveDocument.addObject("Part::Cylinder", "WBbossDOWNTUBEm10")
App.ActiveDocument.WBbossDOWNTUBEm10.Radius = 4.5
App.ActiveDocument.WBbossDOWNTUBEm10.Height = 2.0
App.ActiveDocument.WBbossDOWNTUBEm10.Placement = Base.Placement(Base.Vector(64.0, 0, 0), Base.Rotation(0, 0, 0))
App.ActiveDocument.addObject("Part::Cylinder", "WBbossDOWNTUBEmp10")
App.ActiveDocument.WBbossDOWNTUBEmp10.Radius = Waterbottle_boss_dia / 2
App.ActiveDocument.WBbossDOWNTUBEmp10.Height = Waterbottle_boss_length - 2.0
App.ActiveDocument.WBbossDOWNTUBEmp10.Placement = Base.Placement(Base.Vector(64.0, 0, 2.0 - Waterbottle_boss_length), Base.Rotation(0, 0, 0))
App.ActiveDocument.addObject("Part::Cylinder", "WBbossHDOWNTUBEmh10")
App.ActiveDocument.WBbossHDOWNTUBEmh10.Radius = Waterbottle_boss_hole_dia / 2
App.ActiveDocument.WBbossHDOWNTUBEmh10.Height = Waterbottle_boss_length + 1
App.ActiveDocument.WBbossHDOWNTUBEmh10.Placement = Base.Placement(Base.Vector(64.0, 0, 2.0 - Waterbottle_boss_length), Base.Rotation(0, 0, 0))
App.activeDocument().addObject("Part::MultiFuse", "WBbossDOWNTUBEm0")
App.activeDocument().WBbossDOWNTUBEm0.Shapes = [App.activeDocument().WBbossDOWNTUBEm00,
                                                App.activeDocument().WBbossDOWNTUBEmp00,
                                                App.activeDocument().WBbossDOWNTUBEm10,
                                                App.activeDocument().WBbossDOWNTUBEmp10]
App.ActiveDocument.WBbossDOWNTUBEm0.Placement = Base.Placement(Base.Vector(940.872, 481.563, 0.0), Base.Rotation(49.923, 0, -90))
App.activeDocument().addObject("Part::MultiFuse", "WBbossHolesDOWNTUBEm0")
App.activeDocument().WBbossHolesDOWNTUBEm0.Shapes = [App.activeDocument().WBbossHDOWNTUBEmh00,
                                                     App.activeDocument().WBbossHDOWNTUBEmh10]
App.ActiveDocument.WBbossHolesDOWNTUBEm0.Placement = Base.Placement(Base.Vector(940.872, 481.563, 0.0), Base.Rotation(49.923, 0, -90))
App.activeDocument().addObject("Part::Cut", "WBbossDrilledDOWNTUBEm0")
App.ActiveDocument.ActiveObject.Base = App.activeDocument().WBbossDOWNTUBEm0
App.ActiveDocument.ActiveObject.Tool = App.activeDocument().WBbossHolesDOWNTUBEm0
App.ActiveDocument.recompute()

# --- mitres / trims -----------------------------------------------------------

App.ActiveDocument.recompute()
App.activeDocument().addObject("Part::MultiFuse", "STCuts")
App.activeDocument().STCuts.Shapes = [App.activeDocument().SPost_extrude,
                                      App.activeDocument().BBGearBoxCut,
                                      App.ActiveDocument.WBbossHolesSEATTUBEm0,
                                      App.activeDocument().STslot,
                                      App.activeDocument().STslotHole,
                                      App.activeDocument().DT_tube]
App.activeDocument().addObject("Part::Cut", "ST_tube_trimmed")
App.ActiveDocument.ActiveObject.Base = App.activeDocument().ST_tube
App.ActiveDocument.ActiveObject.Tool = App.activeDocument().STCuts
App.ActiveDocument.recompute()

App.activeDocument().addObject("Part::MultiFuse", "DTCuts")
App.activeDocument().DTCuts.Shapes = [App.activeDocument().HT_tube,
                                      App.activeDocument().BBGearBoxCut,
                                      App.ActiveDocument.WBbossHolesDOWNTUBEm0]
App.activeDocument().addObject("Part::Cut", "DT_tube_trimmed")
App.activeDocument().DT_tube_trimmed.Base = App.activeDocument().DT_tube
App.activeDocument().DT_tube_trimmed.Tool = App.activeDocument().DTCuts
Gui.activeDocument().DT_tube.Visibility = False
App.ActiveDocument.recompute()

App.activeDocument().addObject("Part::MultiFuse", "TTCuts")
App.activeDocument().TTCuts.Shapes = [App.activeDocument().HT_tube,
                                      App.activeDocument().ST_tube]
App.activeDocument().addObject("Part::Cut", "TT_tube_trimmed")
App.activeDocument().TT_tube_trimmed.Base = App.activeDocument().TT_tube
App.activeDocument().TT_tube_trimmed.Tool = App.activeDocument().TTCuts
Gui.activeDocument().TT_tube.Visibility = False
App.ActiveDocument.recompute()

App.activeDocument().addObject("Part::Cut", "dSS_tube_trimmed")
App.activeDocument().dSS_tube_trimmed.Base = App.activeDocument().dSS_tube
App.activeDocument().dSS_tube_trimmed.Tool = App.activeDocument().ST_tube
Gui.activeDocument().dSS_tube.Visibility = False
App.activeDocument().addObject("Part::Cut", "nSS_tube_trimmed")
App.activeDocument().nSS_tube_trimmed.Base = App.activeDocument().nSS_tube
App.activeDocument().nSS_tube_trimmed.Tool = App.activeDocument().ST_tube
Gui.activeDocument().nSS_tube.Visibility = False
App.ActiveDocument.recompute()

App.ActiveDocument.addObject("Part::Box", "nCSChop")
App.ActiveDocument.nCSChop.Length = 50.00
App.ActiveDocument.nCSChop.Width = 100.00
App.ActiveDocument.nCSChop.Height = 200.00
App.ActiveDocument.nCSChop.Placement = Base.Placement(Base.Vector(786.538, 229.461, -100.0), Base.Rotation(-7.7839794056483305, 0, 0))
App.activeDocument().addObject("Part::MultiFuse", "nCSCut")
App.activeDocument().nCSCut.Shapes = [App.activeDocument().BBGearBoxCut,
                                      App.activeDocument().nCSChop,
                                      App.activeDocument().ST_tube]
App.ActiveDocument.addObject("Part::Box", "dCSChop")
App.ActiveDocument.dCSChop.Length = 50.00
App.ActiveDocument.dCSChop.Width = 100.00
App.ActiveDocument.dCSChop.Height = 200.00
App.ActiveDocument.dCSChop.Placement = Base.Placement(Base.Vector(786.538, 229.461, -100.0), Base.Rotation(-7.7839794056483305, 0, 0))
App.activeDocument().addObject("Part::MultiFuse", "dCSCut")
App.activeDocument().dCSCut.Shapes = [App.activeDocument().BBGearBoxCut,
                                      App.activeDocument().dCSChop,
                                      App.activeDocument().ST_tube]
App.activeDocument().addObject("Part::Cut", "dCS_tube_trimmed")
App.activeDocument().dCS_tube_trimmed.Base = App.activeDocument().dCS_tube
App.activeDocument().dCS_tube_trimmed.Tool = App.activeDocument().dCSCut
Gui.activeDocument().dCS_tube.Visibility = False
App.activeDocument().addObject("Part::Cut", "nCS_tube_trimmed")
App.activeDocument().nCS_tube_trimmed.Base = App.activeDocument().nCS_tube
App.activeDocument().nCS_tube_trimmed.Tool = App.activeDocument().nCSCut
Gui.activeDocument().nCS_tube.Visibility = False
App.ActiveDocument.recompute()

# --- rear wheel ---------------------------------------------------------------

bez0 = Part.BezierCurve()
bez0.setPoles([Base.Vector(0.0, 0.0, 0.0), Base.Vector(20.0, 0.0, 0.0), Base.Vector(20.0, 27.0, 0.0)])
bez1 = Part.BezierCurve()
bez1.setPoles([Base.Vector(20.0, 27.0, 0.0), Base.Vector(20.0, 32.5, 0.0), Base.Vector(9.0, 38.0, 0.0)])
bez2 = Part.BezierCurve()
bez2.setPoles([Base.Vector(-9.0, 38.0, 0.0), Base.Vector(-20.0, 32.5, 0.0), Base.Vector(-20.0, 27.0, 0.0)])
bez3 = Part.BezierCurve()
bez3.setPoles([Base.Vector(-20.0, 27.0, 0.0), Base.Vector(-20.0, 0.0, 0.0), Base.Vector(0.0, 0.0, 0.0)])
TireRProf0 = Part.Wire([bez0.toShape(), bez1.toShape(),
                        Part.makeLine((9.0, 38.0, 0), (-9.0, 38.0, 0)),
                        bez2.toShape(), bez3.toShape()])
TireRProf = Part.Face([TireRProf0, ])

App.ActiveDocument.addObject("Part::Revolution", "TireR")
obj = App.ActiveDocument.addObject('Part::Feature', 'TireR_profile')
obj.Shape = TireRProf0
App.ActiveDocument.TireR.Source = App.ActiveDocument.TireR_profile
App.ActiveDocument.TireR.Axis = (1, 0, 0)
App.ActiveDocument.TireR.Base = (365.0, 355.0, 0.0)
App.ActiveDocument.TireR.Angle = 360.0
App.ActiveDocument.TireR.Solid = True
App.ActiveDocument.TireR.Symmetric = False
App.ActiveDocument.TireR_profile.Visibility = False
App.ActiveDocument.TireR.Placement = Base.Placement(Base.Vector(365.0, 0, 0), Base.Rotation(0, 90, 0))
App.ActiveDocument.recompute()

RIMSWRProf0 = Part.Wire([Part.makeLine((-9.0, 38.0, 0), (-9.0, 48.0, 0)),
                         Part.makeLine((-9.0, 48.0, 0), (9.0, 48.0, 0)),
                         Part.makeLine((9.0, 48.0, 0), (9.0, 38.0, 0)),
                         Part.makeLine((9.0, 38.0, 0), (-9.0, 38.0, 0.0))])
RIMSWRProf = Part.Face([RIMSWRProf0, ])

App.ActiveDocument.addObject("Part::Revolution", "RIMSWR")
obj = App.ActiveDocument.addObject('Part::Feature', 'RIMSWR_profile')
obj.Shape = RIMSWRProf0
App.ActiveDocument.RIMSWR.Source = App.ActiveDocument.RIMSWR_profile
App.ActiveDocument.RIMSWR.Axis = (1, 0, 0)
App.ActiveDocument.RIMSWR.Base = (365.0, 355.0, 0.0)
App.ActiveDocument.RIMSWR.Angle = 360.0
App.ActiveDocument.RIMSWR.Solid = True
App.ActiveDocument.RIMSWR.Symmetric = False
App.ActiveDocument.RIMSWR_profile.Visibility = False
App.ActiveDocument.RIMSWR.Placement = Base.Placement(Base.Vector(365.0, 0, 0), Base.Rotation(0, 90, 0))
App.ActiveDocument.recompute()

bez0 = Part.BezierCurve()
bez0.setPoles([Base.Vector(9.0, 48.0, 0.0), Base.Vector(9.0, 58.0, 0.0), Base.Vector(0.0, 58.0, 0.0)])
bez1 = Part.BezierCurve()
bez1.setPoles([Base.Vector(0.0, 58.0, 0.0), Base.Vector(-9.0, 58.0, 0.0), Base.Vector(-9.0, 48.0, 0.0)])
RIMRProf0 = Part.Wire([bez0.toShape(), bez1.toShape(),
                       Part.makeLine((-9.0, 48.0, 0), (9.0, 48.0, 0.0))])
RIMRProf = Part.Face([RIMRProf0, ])

App.ActiveDocument.addObject("Part::Revolution", "RIMR")
obj = App.ActiveDocument.addObject('Part::Feature', 'RIMR_profile')
obj.Shape = RIMRProf0
App.ActiveDocument.RIMR.Source = App.ActiveDocument.RIMR_profile
App.ActiveDocument.RIMR.Axis = (1, 0, 0)
App.ActiveDocument.RIMR.Base = (365.0, 355.0, 0.0)
App.ActiveDocument.RIMR.Angle = 360.0
App.ActiveDocument.RIMR.Solid = True
App.ActiveDocument.RIMR.Symmetric = False
App.ActiveDocument.RIMR_profile.Visibility = False
App.ActiveDocument.RIMR.Placement = Base.Placement(Base.Vector(365.0, 0, 0), Base.Rotation(0, 90, 0))
App.ActiveDocument.recompute()

App.ActiveDocument.addObject("Part::Cylinder", "RCut")
App.ActiveDocument.RCut.Radius = 336.0
App.ActiveDocument.RCut.Height = 400
App.ActiveDocument.RCut.Placement = Base.Placement(Base.Vector(365.0, 355.0, -200.0), Base.Rotation(0, 0, 0))
App.activeDocument().addObject("Part::Cut", "Tire_R")
App.ActiveDocument.ActiveObject.Base = App.activeDocument().TireR
App.ActiveDocument.ActiveObject.Tool = App.activeDocument().RCut
App.activeDocument().addObject("Part::MultiCommon", "TIRESWR")
App.activeDocument().TIRESWR.Shapes = [App.activeDocument().TireR,
                                       App.activeDocument().RCut]
App.ActiveDocument.recompute()

# --- front wheel --------------------------------------------------------------

bez0 = Part.BezierCurve()
bez0.setPoles([Base.Vector(0.0, 0.0, 0.0), Base.Vector(20.0, 0.0, 0.0), Base.Vector(20.0, 27.0, 0.0)])
bez1 = Part.BezierCurve()
bez1.setPoles([Base.Vector(20.0, 27.0, 0.0), Base.Vector(20.0, 32.5, 0.0), Base.Vector(9.0, 38.0, 0.0)])
bez2 = Part.BezierCurve()
bez2.setPoles([Base.Vector(-9.0, 38.0, 0.0), Base.Vector(-20.0, 32.5, 0.0), Base.Vector(-20.0, 27.0, 0.0)])
bez3 = Part.BezierCurve()
bez3.setPoles([Base.Vector(-20.0, 27.0, 0.0), Base.Vector(-20.0, 0.0, 0.0), Base.Vector(0.0, 0.0, 0.0)])
TireFProf0 = Part.Wire([bez0.toShape(), bez1.toShape(),
                        Part.makeLine((9.0, 38.0, 0), (-9.0, 38.0, 0)),
                        bez2.toShape(), bez3.toShape()])
TireFProf = Part.Face([TireFProf0, ])

App.ActiveDocument.addObject("Part::Revolution", "TireF")
obj = App.ActiveDocument.addObject('Part::Feature', 'TireF_profile')
obj.Shape = TireFProf0
App.ActiveDocument.TireF.Source = App.ActiveDocument.TireF_profile
App.ActiveDocument.TireF.Axis = (1, 0, 0)
App.ActiveDocument.TireF.Base = (1406.417, 355.0, 0.0)
App.ActiveDocument.TireF.Angle = 360.0
App.ActiveDocument.TireF.Solid = True
App.ActiveDocument.TireF.Symmetric = False
App.ActiveDocument.TireF_profile.Visibility = False
App.ActiveDocument.TireF.Placement = Base.Placement(Base.Vector(1406.417, 0, 0), Base.Rotation(0, 90, 0))
App.ActiveDocument.recompute()

RIMSWFProf0 = Part.Wire([Part.makeLine((-9.0, 38.0, 0), (-9.0, 48.0, 0)),
                         Part.makeLine((-9.0, 48.0, 0), (9.0, 48.0, 0)),
                         Part.makeLine((9.0, 48.0, 0), (9.0, 38.0, 0)),
                         Part.makeLine((9.0, 38.0, 0), (-9.0, 38.0, 0.0))])
RIMSWFProf = Part.Face([RIMSWFProf0, ])

App.ActiveDocument.addObject("Part::Revolution", "RIMSWF")
obj = App.ActiveDocument.addObject('Part::Feature', 'RIMSWF_profile')
obj.Shape = RIMSWFProf0
App.ActiveDocument.RIMSWF.Source = App.ActiveDocument.RIMSWF_profile
App.ActiveDocument.RIMSWF.Axis = (1, 0, 0)
App.ActiveDocument.RIMSWF.Base = (1406.417, 355.0, 0.0)
App.ActiveDocument.RIMSWF.Angle = 360.0
App.ActiveDocument.RIMSWF.Solid = True
App.ActiveDocument.RIMSWF.Symmetric = False
App.ActiveDocument.RIMSWF_profile.Visibility = False
App.ActiveDocument.RIMSWF.Placement = Base.Placement(Base.Vector(1406.417, 0, 0), Base.Rotation(0, 90, 0))
App.ActiveDocument.recompute()

bez0 = Part.BezierCurve()
bez0.setPoles([Base.Vector(9.0, 48.0, 0.0), Base.Vector(9.0, 58.0, 0.0), Base.Vector(0.0, 58.0, 0.0)])
bez1 = Part.BezierCurve()
bez1.setPoles([Base.Vector(0.0, 58.0, 0.0), Base.Vector(-9.0, 58.0, 0.0), Base.Vector(-9.0, 48.0, 0.0)])
RIMFProf0 = Part.Wire([bez0.toShape(), bez1.toShape(),
                       Part.makeLine((-9.0, 48.0, 0), (9.0, 48.0, 0.0))])
RIMFProf = Part.Face([RIMFProf0, ])

App.ActiveDocument.addObject("Part::Revolution", "RIMF")
obj = App.ActiveDocument.addObject('Part::Feature', 'RIMF_profile')
obj.Shape = RIMFProf0
App.ActiveDocument.RIMF.Source = App.ActiveDocument.RIMF_profile
App.ActiveDocument.RIMF.Axis = (1, 0, 0)
App.ActiveDocument.RIMF.Base = (1406.417, 355.0, 0.0)
App.ActiveDocument.RIMF.Angle = 360.0
App.ActiveDocument.RIMF.Solid = True
App.ActiveDocument.RIMF.Symmetric = False
App.ActiveDocument.RIMF_profile.Visibility = False
App.ActiveDocument.RIMF.Placement = Base.Placement(Base.Vector(1406.417, 0, 0), Base.Rotation(0, 90, 0))
App.ActiveDocument.recompute()

App.ActiveDocument.addObject("Part::Cylinder", "FCut")
App.ActiveDocument.FCut.Radius = 336.0
App.ActiveDocument.FCut.Height = 400
App.ActiveDocument.FCut.Placement = Base.Placement(Base.Vector(1406.417, 355.0, -200.0), Base.Rotation(0, 0, 0))
App.activeDocument().addObject("Part::Cut", "Tire_F")
App.ActiveDocument.ActiveObject.Base = App.activeDocument().TireF
App.ActiveDocument.ActiveObject.Tool = App.activeDocument().FCut
App.activeDocument().addObject("Part::MultiCommon", "TIRESWF")
App.activeDocument().TIRESWF.Shapes = [App.activeDocument().TireF,
                                       App.activeDocument().FCut]
App.ActiveDocument.recompute()

# --- colours ------------------------------------------------------------------

WHITE = (1.0, 1.0, 1.0)
BLACK = (0.003921569, 0.003921569, 0.003921569)

COLOURS = [
    ("WBbossDrilledSEATTUBEm0", WHITE),
    ("WBbossDrilledDOWNTUBEm0", WHITE),
    ("HT_Finished", WHITE),
    ("ST_tube_trimmed", WHITE),
    ("DT_tube_trimmed", WHITE),
    ("TT_tube_trimmed", WHITE),
    ("dSS_tube_trimmed", WHITE),
    ("nSS_tube_trimmed", WHITE),
    ("ssBridge", WHITE),
    ("dCS_tube_trimmed", WHITE),
    ("nCS_tube_trimmed", WHITE),
    ("csBridge", WHITE),
    ("BB", WHITE),
    ("Headset", (0.8, 0.0, 0.2)),
    ("Seatpost_clamp_finished", (0.2, 0.2, 0.2)),
    ("Tire_R", (0.25882354, 0.24313726, 0.24313726)),
    ("Tire_F", (0.25882354, 0.24313726, 0.24313726)),
    ("TIRESWR", (0.15686275, 0.15294118, 0.15294118)),
    ("TIRESWF", (0.15686275, 0.15294118, 0.15294118)),
    ("RIMR", BLACK),
    ("RIMF", BLACK),
    ("RIMSWR", BLACK),
    ("RIMSWF", BLACK),
] + dropout_objs

for _name, _colour in COLOURS:
    _vo = Gui.getDocument(DOC_NAME).getObject(_name)
    if _vo is not None:
        _vo.ShapeColor = _colour
        _vo.Transparency = 0

App.ActiveDocument.recompute()

# ============================ END EXPORT BODY ================================


# ------------------ Section 3: jig orientation & measurement ------------------
#
# Reorients the model so the seat tube runs vertically (+Y) with the BB at the
# origin, matching the fixture. This is a rigid transform: no frame dimension
# or angle changes, the whole assembly is simply re-expressed in jig coords.
# The wheels therefore sit 16.8 deg off horizontal, which is what the jig sees.

BB_center = Base.Vector(793.309, 279.0, 0.0)
ST_top    = Base.Vector(648.794, 757.66, 0.0)

_st_vec   = ST_top.sub(BB_center)
ST_length = _st_vec.Length
ST_angle  = math.degrees(math.atan2(_st_vec.y, _st_vec.x))   # 106.8 deg from +X
JIG_ANGLE = 90.0 - ST_angle                                  # -16.8 deg

_offset = Base.Vector(-BB_center.x, -BB_center.y, -BB_center.z) \
    if Jig_move_BB_to_origin else Base.Vector(0, 0, 0)

JIG_XFORM = Base.Placement(
    _offset,
    Base.Rotation(Base.Vector(0, 0, 1), JIG_ANGLE),
    BB_center)

# --- move the frame into the jig container ------------------------------------
# App::Part composes on top of each child's own placement and survives recompute.
# Editing the Placement of a Part::Cut/Fuse directly does not: the next recompute
# rebuilds it from the shape and silently discards the rotation.

jig = App.ActiveDocument.addObject("App::Part", "JigOrientation")
_frame = [o for o in App.ActiveDocument.Objects
          if o is not jig
          and not o.InList
          and o.isDerivedFrom("Part::Feature")]
for _o in _frame:
    jig.addObject(_o)
jig.Placement = JIG_XFORM
App.ActiveDocument.recompute()

# --- reference points ---------------------------------------------------------
# Defined in BikeCAD coordinates and transformed, so they stay correct if the
# seat tube angle changes. Reference geometry is built outside the container,
# directly in jig coordinates.

REF_POINTS = [
    ("BB center",      Base.Vector(793.309,  279.0,   0.0)),
    ("Rear axle",      Base.Vector(365.0,    355.0,   0.0)),
    ("Front axle",     Base.Vector(1406.417, 355.0,   0.0)),
    ("ST top",         Base.Vector(648.794,  757.66,  0.0)),
    ("TT/SS junction", Base.Vector(660.355,  719.367, 0.0)),
    ("HT bottom",      Base.Vector(1233.425, 737.083, 0.0)),
    ("HT top",         Base.Vector(1192.821, 860.58,  0.0)),
    ("DT/HT junction", Base.Vector(1218.058, 783.822, 0.0)),
    ("TT/HT junction", Base.Vector(1201.848, 833.125, 0.0)),
    ("CS dropout end", Base.Vector(479.55,   321.89,  71.5)),
    ("SS dropout end", Base.Vector(384.089,  412.555, 71.5)),
]

JIG_PTS = dict((name, JIG_XFORM.multVec(p)) for name, p in REF_POINTS)

# --- dummy tubes, parallel to the seat tube -----------------------------------

DUMMIES = ["Rear axle", "HT bottom", "HT top"]

for _label in DUMMIES:
    _p = JIG_PTS[_label]
    _name = "JigDummy_" + _label.replace(" ", "_").replace("/", "_")
    _y0 = min(0.0, _p.y) - Jig_dummy_overhang
    _y1 = max(0.0, _p.y) + Jig_dummy_overhang
    _o = App.ActiveDocument.addObject("Part::Feature", _name)
    _o.Shape = Part.makeCylinder(Jig_dummy_dia / 2.0, _y1 - _y0,
                                 Base.Vector(_p.x, _y0, 0.0),
                                 Base.Vector(0, 1, 0))
    Gui.ActiveDocument.getObject(_name).ShapeColor = (0.85, 0.2, 0.1)
    Gui.ActiveDocument.getObject(_name).Transparency = 30

# --- horizontal reference line through the BB, perpendicular to the seat tube --

_xs = [JIG_PTS[k].x for k in DUMMIES] + [0.0]
_line = App.ActiveDocument.addObject("Part::Feature", "JigRef_Horizontal")
_line.Shape = Part.makeLine(
    Base.Vector(min(_xs) - Jig_dummy_overhang, 0.0, 0.0),
    Base.Vector(max(_xs) + Jig_dummy_overhang, 0.0, 0.0))

# --- intersections of the dummies with that line ------------------------------

for _label in DUMMIES:
    _p = JIG_PTS[_label]
    _name = "JigHit_" + _label.replace(" ", "_").replace("/", "_")
    _o = App.ActiveDocument.addObject("Part::Feature", _name)
    _o.Shape = Part.makeSphere(Jig_marker_dia / 2.0, Base.Vector(_p.x, 0.0, 0.0))
    Gui.ActiveDocument.getObject(_name).ShapeColor = (0.1, 0.5, 0.9)

App.ActiveDocument.recompute()

doc = App.ActiveDocument
for nm, p in [("JigHit_BB",       Base.Vector(0.0, 0.0, 0.0)),
              ("JigPt_Rear_axle", Base.Vector(-388.063, 196.550, 0.0))]:
    o = doc.addObject("Part::Feature", nm)
    o.Shape = Part.makeSphere(4.0, p)
    Gui.ActiveDocument.getObject(nm).ShapeColor = (0.9, 0.7, 0.0)
doc.recompute()

import Part
doc = App.ActiveDocument

X = {"RearAxle": -388.063, "HTbtm": 553.732, "HTtop": 550.555}

for k, x in X.items():
    nm = "MeasH_BB_" + k
    o = doc.addObject("Part::Feature", nm)
    o.Shape = Part.makeLine(Base.Vector(0, 0, 0), Base.Vector(x, 0, 0))
    Gui.ActiveDocument.getObject(nm).ShapeColor = (0.0, 0.7, 0.3)
    Gui.ActiveDocument.getObject(nm).LineWidth = 3
    print("%-20s %10.3f" % (nm, abs(x)))

doc.recompute()

import Part
doc = App.ActiveDocument

V = {"RearAxle": (-388.063, 196.550),
     "HTbtm":    ( 553.732, 311.325)}

for k, (x, y) in V.items():
    nm = "MeasV_BB_" + k
    o = doc.addObject("Part::Feature", nm)
    o.Shape = Part.makeLine(Base.Vector(x, 0, 0), Base.Vector(x, y, 0))
    Gui.ActiveDocument.getObject(nm).ShapeColor = (0.0, 0.35, 0.9)
    Gui.ActiveDocument.getObject(nm).LineWidth = 3
    print("%-20s %10.3f" % (nm, y))

doc.recompute()

import Part
doc = App.ActiveDocument

Y_TOP = 945.0
HTb   = Base.Vector(553.732, 311.325, 0.0)
HTt   = Base.Vector(550.555, 441.287, 0.0)
RA    = Base.Vector(-388.063, 196.550, 0.0)

# --- clear out the superseded / misleading objects ---
for nm in ["JigDummy_HT_bottom", "JigDummy_HT_top",
           "JigHit_HT_bottom", "JigHit_HT_top", "JigHit_BB",
           "JigHit_Rear_axle", "JigPt_Rear_axle",
           "JigRef_Horizontal_Top",
           "Meas_BB_RearAxle", "Meas_BB_HTbtm", "Meas_BB_HTtop",
           "MeasH_BB_RearAxle", "MeasH_BB_HTbtm", "MeasH_BB_HTtop",
           "MeasV_BB_RearAxle", "MeasV_BB_HTbtm",
           "MeasV_Top_HTtop", "MeasH_Top_HTtop",
           "MeasH_Top_HTaxis", "MeasHTaxis_extended", "MeasHT_axis",
           "MeasH_Btm_HTaxis"]:
    if doc.getObject(nm):
        doc.removeObject(nm)

d    = HTt.sub(HTb)
xat  = lambda y: HTb.x + d.x * (y - HTb.y) / d.y
x0, x1 = xat(0.0), xat(Y_TOP)

def add(nm, p, q, col, w=3):
    o = doc.addObject("Part::Feature", "CORRECT_" + nm)
    o.Shape = Part.makeLine(p, q)
    v = Gui.ActiveDocument.getObject(o.Name)
    v.ShapeColor = col
    v.LineWidth  = w
    print("%-28s %10.3f" % (o.Name, (q - p).Length))
    return o

GREY, ORANGE, GREEN, BLUE = (0.4,0.4,0.4), (0.9,0.4,0.0), (0.0,0.7,0.3), (0.0,0.35,0.9)

# datums
xs = [x0, x1, RA.x, 0.0]
add("Datum_Btm", Base.Vector(min(xs)-80, 0.0,   0), Base.Vector(max(xs)+80, 0.0,   0), GREY, 2)
add("Datum_Top", Base.Vector(min(xs)-80, Y_TOP, 0), Base.Vector(max(xs)+80, Y_TOP, 0), GREY, 2)

# head tube centreline, extended to both datums
add("HTaxis",        Base.Vector(x0, 0.0, 0), Base.Vector(x1, Y_TOP, 0), ORANGE)
add("HTaxis_at_Btm", Base.Vector(0, 0.0,   0), Base.Vector(x0, 0.0,   0), GREEN)
add("HTaxis_at_Top", Base.Vector(0, Y_TOP, 0), Base.Vector(x1, Y_TOP, 0), GREEN)

# rear axle
add("RearAxle_H", Base.Vector(0, 0, 0),      Base.Vector(RA.x, 0, 0),    GREEN)
add("RearAxle_V", Base.Vector(RA.x, 0, 0),   RA,                         BLUE)

doc.recompute()

import Part
doc = App.ActiveDocument

Z_DATUM = -67.5
PTS = {"RearAxle": (-388.063, 196.550),
       "BB":       (   0.000,   0.000),
       "HTbtm":    ( 553.732, 311.325)}

for k, (x, y) in PTS.items():
    nm = "CORRECT_Lat_" + k
    o = doc.addObject("Part::Feature", nm)
    o.Shape = Part.makeLine(Base.Vector(x, y, Z_DATUM), Base.Vector(x, y, 0.0))
    v = Gui.ActiveDocument.getObject(nm)
    v.ShapeColor = (0.7, 0.0, 0.7)
    v.LineWidth = 3
    print("%-24s %8.3f" % (nm, abs(Z_DATUM)))

doc.recompute()

# --- measurement report -------------------------------------------------------

SEGMENTS = [
    ("Seat tube        (BB - ST top)",   Base.Vector(793.309, 279.0, 0.0),    Base.Vector(648.794, 757.66, 0.0)),
    ("Down tube        (BB - HT)",       Base.Vector(793.309, 279.0, 0.0),    Base.Vector(1218.058, 783.822, 0.0)),
    ("Top tube         (ST - HT)",       Base.Vector(660.355, 719.367, 0.0),  Base.Vector(1201.848, 833.125, 0.0)),
    ("Head tube        (btm - top)",     Base.Vector(1233.425, 737.083, 0.0), Base.Vector(1192.821, 860.58, 0.0)),
    ("Chainstay CL     (drop - BB end)", Base.Vector(479.55, 321.89, 71.5),   Base.Vector(813.125, 276.291, 19.136)),
    ("Seatstay CL      (drop - TT jn)",  Base.Vector(384.089, 412.555, 71.5), Base.Vector(660.355, 719.367, 17.0)),
    ("Chainstay length (axle - BB)",     Base.Vector(365.0, 355.0, 0.0),      Base.Vector(793.309, 279.0, 0.0)),
    ("Wheelbase        (axle - axle)",   Base.Vector(365.0, 355.0, 0.0),      Base.Vector(1406.417, 355.0, 0.0)),
]

print("")
print("=" * 74)
print("JIG FRAME  --  BB at origin, seat tube along +Y")
print("seat tube angle %.2f deg  ->  rotation applied %.2f deg about Z"
      % (ST_angle, JIG_ANGLE))
print("=" * 74)
print("")
print("%-16s %10s %10s %10s %12s" % ("point", "x (fwd)", "y (up)", "z (lat)", "dist from BB"))
print("-" * 74)
for _label, _p in REF_POINTS:
    _q = JIG_PTS[_label]
    print("%-16s %10.3f %10.3f %10.3f %12.3f"
          % (_label, _q.x, _q.y, _q.z, _q.Length))

print("")
print("%-34s %10s %12s" % ("segment", "length", "angle*"))
print("-" * 74)
for _label, _a, _b in SEGMENTS:
    _d = _b.sub(_a)
    _da = JIG_XFORM.multVec(_b).sub(JIG_XFORM.multVec(_a))
    print("%-34s %10.3f %11.3f" % (_label, _d.Length,
                                   math.degrees(math.atan2(_da.y, _da.x))))
print("* angle measured from the jig horizontal, in the jig XY plane")

print("")
print("%-16s %12s" % ("dummy tube", "x at y=0"))
print("-" * 74)
for _label in DUMMIES:
    print("%-16s %12.3f" % (_label, JIG_PTS[_label].x))
print("HT dummy spacing at the horizontal: %.3f"
      % abs(JIG_PTS["HT top"].x - JIG_PTS["HT bottom"].x))
print("=" * 74)
print("")

Gui.SendMsgToActiveView("ViewFit")