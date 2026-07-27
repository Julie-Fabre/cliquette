Head_Tube_id=45.0
Head_Tube_top_id=45.0
Head_Tube_mid_id=42.6

Pinch_boss_length=20.0
ST_slot_width=2.0
ST_slot_depth=35.0
ST_slot_hole_dia=4.0
Waterbottle_boss_dia=6.35
Waterbottle_boss_hole_dia=4.2
Waterbottle_boss_length=8.0

LogoThickness1=0.25
LogoThickness2=0.35
DOurl="https://www.bikecad.ca/fcad/do/"
DOName='PD000'
BoltsExtra=''
DOInsertR='PA445'
DOInsertL='PA426'

Bridge_hole_diameter=6.0

BB_id=44.8


#########################################

import Part, math
import requests
import tempfile
from FreeCAD import Base

App.newDocument("bike_v4")
App.setActiveDocument("bike_v4")
os.chdir(os.path.dirname(__file__))

yokeTool = False
dropTool = False

url = DOurl + DOName + 'L.step'
r = requests.get(url)
if r.status_code == 200:
   dropL = True
   with open(DOName + 'L.step', 'wb') as f:
       f.write(r.content)
   shape=Part.Shape()
   shape.read(DOName + 'L.step')
   if os.path.exists(DOName + 'L.step'):
       os.remove(DOName + 'L.step')
   obj=App.ActiveDocument.addObject("Part::Feature","DropoutL")
   obj.Shape=shape
   App.ActiveDocument.DropoutL.Placement = Base.Placement(Base.Vector(365.0,355.0, -67.5),Base.Rotation(-5.0,0,0))

else:
   dropL = False
   print(DOName + 'L.step not found')

url = DOurl + DOName + 'R.step'
r = requests.get(url)
if r.status_code == 200:
   dropR = True
   with open(DOName + 'R.step', 'wb') as f:
       f.write(r.content)
   shape=Part.Shape()
   shape.read(DOName + 'R.step')
   if os.path.exists(DOName + 'R.step'):
       os.remove(DOName + 'R.step')
   obj=App.ActiveDocument.addObject("Part::Feature","DropoutR")
   obj.Shape=shape
   App.ActiveDocument.DropoutR.Placement = Base.Placement(Base.Vector(365.0,355.0, 67.5),Base.Rotation(-5.0,0,0))

else:
   dropR = False
   print(DOName + 'R.step not found')

url = DOurl + DOInsertR + '.step'
r = requests.get(url)
if r.status_code == 200:
   insertDropR = True
   with open(DOInsertR + '.step', 'wb') as f:
       f.write(r.content)
   shape=Part.Shape()
   shape.read(DOInsertR + '.step')
   if os.path.exists(DOInsertR + '.step'):
       os.remove(DOInsertR + '.step')
   obj=App.ActiveDocument.addObject("Part::Feature","DropoutInsertR")
   obj.Shape=shape
   App.ActiveDocument.DropoutInsertR.Placement = Base.Placement(Base.Vector(365.0,355.0, 67.5),Base.Rotation(-5.0,0,0))
else:
   insertDropR = False
   print(DOInsertR + '.step not found')

url = DOurl + DOInsertL + '.step'
r = requests.get(url)
if r.status_code == 200:
   insertDropL = True
   with open(DOInsertL + '.step', 'wb') as f:
       f.write(r.content)
   shape=Part.Shape()
   shape.read(DOInsertL + '.step')
   if os.path.exists(DOInsertL + '.step'):
       os.remove(DOInsertL + '.step')
   obj=App.ActiveDocument.addObject("Part::Feature","DropoutInsertL")
   obj.Shape=shape
   App.ActiveDocument.DropoutInsertL.Placement = Base.Placement(Base.Vector(365.0,355.0, -67.5),Base.Rotation(-5.0,0,0))
else:
   insertDropL = False
   print(DOInsertL + '.step not found')

url = DOurl + DOName + BoltsExtra + 'BoltsR.step'
r = requests.get(url)
if r.status_code == 200:
   boltsRDrop = True
   with open(DOName + BoltsExtra + 'BoltsR.step', 'wb') as f:
       f.write(r.content)
   shape=Part.Shape()
   shape.read(DOName + BoltsExtra + 'BoltsR.step')
   if os.path.exists(DOName + BoltsExtra + 'BoltsR.step'):
       os.remove(DOName + BoltsExtra + 'BoltsR.step')
   obj=App.ActiveDocument.addObject("Part::Feature","DropoutBoltsR")
   obj.Shape=shape
   App.ActiveDocument.DropoutBoltsR.Placement = Base.Placement(Base.Vector(365.0,355.0, 67.5),Base.Rotation(-5.0,0,0))
else:
   boltsRDrop = False
   print(DOName + 'BoltsR.step not found')
url = DOurl + DOName + 'BoltsL.step'
r = requests.get(url)
if r.status_code == 200:
   boltsLDrop = True
   with open(DOName + 'BoltsL.step', 'wb') as f:
       f.write(r.content)
   shape=Part.Shape()
   shape.read(DOName + 'BoltsL.step')
   if os.path.exists(DOName + 'BoltsL.step'):
       os.remove(DOName + 'BoltsL.step')
   obj=App.ActiveDocument.addObject("Part::Feature","DropoutBoltsL")
   obj.Shape=shape
   App.ActiveDocument.DropoutBoltsL.Placement = Base.Placement(Base.Vector(365.0,355.0, -67.5),Base.Rotation(-5.0,0,0))
else:
   boltsLDrop = False
   print(DOName + 'BoltsL.step not found')

App.ActiveDocument.addObject("Part::Revolution","Headset")

bez0 = Part.BezierCurve()
bez0.setPoles([Base.Vector(25.0,0.0,0.0), Base.Vector(30.5,0.0,0.0), Base.Vector(30.5,-6.0,0.0)])
bez1 = Part.BezierCurve()
bez1.setPoles([Base.Vector(30.5,-6.0,0.0), Base.Vector(30.5,-12.0,0.0), Base.Vector(25.0,-12.0,0.0)])
headsetProfileWire0=Part.Wire([Part.makeLine((22.5,0.0,0),(25.0,0.0,0)),bez0.toShape(),bez1.toShape(),Part.makeLine((25.0,-12.0,0),(22.5,-12.0,0)),Part.makeLine((22.5,-12.0,0),(22.5,0.0,0.0) )])


obj=App.ActiveDocument.addObject('Part::Feature','HS_profile')
obj.Shape=headsetProfileWire0
App.ActiveDocument.Headset.Source = App.ActiveDocument.HS_profile
App.ActiveDocument.Headset.Axis = (0,1,0)
App.ActiveDocument.Headset.Base = (0,0,0)
App.ActiveDocument.Headset.Angle = 360.0
App.ActiveDocument.Headset.Solid = True
App.ActiveDocument.Headset.Symmetric = False
App.ActiveDocument.Headset.Placement = Base.Placement(Base.Vector(1233.425,737.083,0),Base.Rotation(18.2,0,0))
App.ActiveDocument.HS_profile.Visibility = False
App.ActiveDocument.addObject("Part::Revolution","HT_tube")

htbackProfileWire0=Part.Wire([Part.makeLine((1233.425,737.083,0),(1209.675,729.275,0)),Part.makeLine((1209.675,729.275,0),(1208.114,734.025,0)),Part.makeLine((1208.114,734.025,0),(1206.849,741.714,0)),Part.makeLine((1206.849,741.714,0),(1174.178,841.081,0)),Part.makeLine((1174.178,841.081,0),(1170.633,848.021,0)),Part.makeLine((1170.633,848.021,0),(1169.072,852.771,0)),Part.makeLine((1169.072,852.771,0),(1192.821,860.58,0)),Part.makeLine((1192.821,860.58,0),(1233.425,737.083,0.0) )])


obj=App.ActiveDocument.addObject('Part::Feature','HT_profile')
obj.Shape=htbackProfileWire0
App.ActiveDocument.HT_tube.Source = App.ActiveDocument.HT_profile
App.ActiveDocument.HT_tube.Axis = (-40.604,123.497,0.0)
App.ActiveDocument.HT_tube.Base = (1233.425,737.083, 0.0)
App.ActiveDocument.HT_tube.Angle = 360.0
App.ActiveDocument.HT_tube.Solid = True
App.ActiveDocument.HT_tube.Symmetric = False
App.ActiveDocument.HT_profile.Visibility = False
App.ActiveDocument.addObject("Part::Cylinder","HT_cut1")
App.ActiveDocument.HT_cut1.Radius = Head_Tube_id/2
App.ActiveDocument.HT_cut1.Height = 6.0
App.ActiveDocument.HT_cut1.Placement = Base.Placement(Base.Vector(1233.737,736.133, 0.0),Base.Rotation(108.2,90,0))
App.ActiveDocument.addObject("Part::Cylinder","HT_cut2")
App.ActiveDocument.HT_cut2.Radius = Head_Tube_top_id/2
App.ActiveDocument.HT_cut2.Height = 10.0
App.ActiveDocument.HT_cut2.Placement = Base.Placement(Base.Vector(1194.383,855.83, 0.0),Base.Rotation(108.2,90,0))
App.ActiveDocument.addObject("Part::Cylinder","HT_cut3")
App.ActiveDocument.HT_cut3.Radius = min(Head_Tube_id, Head_Tube_mid_id, Head_Tube_top_id)/2
App.ActiveDocument.HT_cut3.Height = 130.0
App.ActiveDocument.HT_cut3.Placement = Base.Placement(Base.Vector(1233.425,737.083, 0.0),Base.Rotation(108.2,90,0))
App.activeDocument().addObject("Part::MultiFuse","HT_cut")
App.activeDocument().HT_cut.Shapes = [App.activeDocument().HT_cut1,App.activeDocument().HT_cut2,App.activeDocument().HT_cut3]
App.activeDocument().addObject("Part::Cut","HT_Finished")
App.ActiveDocument.ActiveObject.Base=App.activeDocument().HT_tube
App.ActiveDocument.ActiveObject.Tool=App.activeDocument().HT_cut
obj=App.ActiveDocument.addObject("Part::Feature","dCS3D_CL")
WireCLdCS=Part.makeLine((479.55,321.89, 71.5), (813.125,276.291, 19.136))
obj.Shape=WireCLdCS
profiledCS1=App.ActiveDocument.addObject("Part::Feature","dCS_XSec1")
profiledCS1.Shape=Part.makeCircle(6.25, Base.Vector(479.55,321.89, 71.5), Base.Vector(0.991, -0.135, -0.166))
profiledCS2=App.ActiveDocument.addObject("Part::Feature","dCS_XSec2")
profiledCS2.Shape=Part.Ellipse(Base.Vector(709.463,305.601, 32.808), Base.Vector(708.758,290.739,40.697), Base.Vector(707.431,290.739, 32.808)).toShape()
profiledCS3=App.ActiveDocument.addObject("Part::Feature","dCS_XSec3")
profiledCS3.Shape=Part.Ellipse(Base.Vector(770.175,297.302, 22.5), Base.Vector(769.471,282.44,30.389), Base.Vector(768.144,282.44, 22.5)).toShape()
profiledCS4=App.ActiveDocument.addObject("Part::Feature","dCS_XSec4")
profiledCS4.Shape=Part.Ellipse(Base.Vector(795.682,293.815, 18.169), Base.Vector(794.977,278.953,26.058), Base.Vector(793.65,278.953, 18.169)).toShape()
if dropTool:
   sweepdCS=App.ActiveDocument.addObject('Part::Sweep','dCS_tube1')
else:
   sweepdCS=App.ActiveDocument.addObject('Part::Sweep','dCS_tube')
sweepdCS.Sections=[profiledCS1,profiledCS2, profiledCS3]
sweepdCS.Spine=App.ActiveDocument.getObject('dCS3D_CL')
sweepdCS.Solid=True
sweepdCS.Frenet=False
sweepdCS.Transition=2

App.ActiveDocument.recompute()
App.activeDocument().dCS3D_CL.Visibility = False
App.activeDocument().dCS_XSec1.Visibility = False
if dropTool:
   App.activeDocument().addObject("Part::Cut",'dCS_tube')
   App.ActiveDocument.ActiveObject.Base=App.activeDocument().dCS_tube1
   App.ActiveDocument.ActiveObject.Tool=App.activeDocument().DropoutTOOL
   App.ActiveDocument.recompute()
App.activeDocument().dCS_XSec2.Visibility = False
App.activeDocument().dCS_XSec3.Visibility = False
App.activeDocument().dCS_XSec4.Visibility = False
obj=App.ActiveDocument.addObject("Part::Feature","dSS3D_CL")
WireCLdSS=Part.makeLine((384.089,412.555, 71.5), (660.355,719.367, 17.0))
obj.Shape=WireCLdSS
profiledSS1=App.ActiveDocument.addObject("Part::Feature","dSS_XSec1")
profiledSS1.Shape=Part.makeCircle(6.25, Base.Vector(384.089,412.555, 71.5), Base.Vector(0.669, 0.743, -0.131))
profiledSS2=App.ActiveDocument.addObject("Part::Feature","dSS_XSec2")
profiledSS2.Shape=Part.makeCircle(8.0, Base.Vector(551.375,598.338, 38.499), Base.Vector(0.669, 0.743, -0.131))
profiledSS3=App.ActiveDocument.addObject("Part::Feature","dSS_XSec3")
profiledSS3.Shape=Part.makeCircle(8.0, Base.Vector(660.355,719.367, 17.0), Base.Vector(0.669, 0.743, -0.131))
profiledSS4=App.ActiveDocument.addObject("Part::Feature","dSS_XSec4")
profiledSS4.Shape=Part.makeCircle(8.0, Base.Vector(660.355,719.367, 17.0), Base.Vector(0.669, 0.743, -0.131))
if dropTool:
   sweepdSS=App.ActiveDocument.addObject('Part::Sweep','dSS_tube1')
else:
   sweepdSS=App.ActiveDocument.addObject('Part::Sweep','dSS_tube')
sweepdSS.Sections=[profiledSS1,profiledSS2, profiledSS3]
sweepdSS.Spine=App.ActiveDocument.getObject('dSS3D_CL')
sweepdSS.Solid=True
sweepdSS.Frenet=False
sweepdSS.Transition=2

App.ActiveDocument.recompute()
App.activeDocument().dSS3D_CL.Visibility = False
App.activeDocument().dSS_XSec1.Visibility = False
if dropTool:
   App.activeDocument().addObject("Part::Cut",'dSS_tube')
   App.ActiveDocument.ActiveObject.Base=App.activeDocument().dSS_tube1
   App.ActiveDocument.ActiveObject.Tool=App.activeDocument().DropoutTOOL
   App.ActiveDocument.recompute()
App.activeDocument().dSS_XSec2.Visibility = False
App.activeDocument().dSS_XSec3.Visibility = False
App.activeDocument().dSS_XSec4.Visibility = False
obj=App.ActiveDocument.addObject("Part::Feature","nCS3D_CL")
WireCLnCS=Part.makeLine((479.55,321.89, -71.5), (813.125,276.291, -19.136))
obj.Shape=WireCLnCS
profilenCS1=App.ActiveDocument.addObject("Part::Feature","nCS_XSec1")
profilenCS1.Shape=Part.makeCircle(6.25, Base.Vector(479.55,321.89, -71.5), Base.Vector(0.991, -0.135, 0.166))
profilenCS2=App.ActiveDocument.addObject("Part::Feature","nCS_XSec2")
profilenCS2.Shape=Part.Ellipse(Base.Vector(709.463,305.601, -32.808), Base.Vector(706.104,290.739,-24.919), Base.Vector(707.431,290.739, -32.808)).toShape()
profilenCS3=App.ActiveDocument.addObject("Part::Feature","nCS_XSec3")
profilenCS3.Shape=Part.Ellipse(Base.Vector(770.175,297.302, -22.5), Base.Vector(766.816,282.44,-14.611), Base.Vector(768.144,282.44, -22.5)).toShape()
profilenCS4=App.ActiveDocument.addObject("Part::Feature","nCS_XSec4")
profilenCS4.Shape=Part.Ellipse(Base.Vector(795.682,293.815, -18.169), Base.Vector(792.323,278.953,-10.28), Base.Vector(793.65,278.953, -18.169)).toShape()
if dropTool:
   sweepnCS=App.ActiveDocument.addObject('Part::Sweep','nCS_tube1')
else:
   sweepnCS=App.ActiveDocument.addObject('Part::Sweep','nCS_tube')
sweepnCS.Sections=[profilenCS1,profilenCS2, profilenCS3]
sweepnCS.Spine=App.ActiveDocument.getObject('nCS3D_CL')
sweepnCS.Solid=True
sweepnCS.Frenet=False
sweepnCS.Transition=2

App.ActiveDocument.recompute()
App.activeDocument().nCS3D_CL.Visibility = False
App.activeDocument().nCS_XSec1.Visibility = False
if dropTool:
   App.activeDocument().addObject("Part::Cut",'nCS_tube')
   App.ActiveDocument.ActiveObject.Base=App.activeDocument().nCS_tube1
   App.ActiveDocument.ActiveObject.Tool=App.activeDocument().DropoutTOOL
   App.ActiveDocument.recompute()
App.activeDocument().nCS_XSec2.Visibility = False
App.activeDocument().nCS_XSec3.Visibility = False
App.activeDocument().nCS_XSec4.Visibility = False
obj=App.ActiveDocument.addObject("Part::Feature","nSS3D_CL")
WireCLnSS=Part.makeLine((384.089,412.555, -71.5), (660.355,719.367, -17.0))
obj.Shape=WireCLnSS
profilenSS1=App.ActiveDocument.addObject("Part::Feature","nSS_XSec1")
profilenSS1.Shape=Part.makeCircle(6.25, Base.Vector(384.089,412.555, -71.5), Base.Vector(0.669, 0.743, 0.131))
profilenSS2=App.ActiveDocument.addObject("Part::Feature","nSS_XSec2")
profilenSS2.Shape=Part.makeCircle(8.0, Base.Vector(551.375,598.338, -38.499), Base.Vector(0.669, 0.743, 0.131))
profilenSS3=App.ActiveDocument.addObject("Part::Feature","nSS_XSec3")
profilenSS3.Shape=Part.makeCircle(8.0, Base.Vector(660.355,719.367, -17.0), Base.Vector(0.669, 0.743, 0.131))
profilenSS4=App.ActiveDocument.addObject("Part::Feature","nSS_XSec4")
profilenSS4.Shape=Part.makeCircle(8.0, Base.Vector(660.355,719.367, -17.0), Base.Vector(0.669, 0.743, 0.131))
if dropTool:
   sweepnSS=App.ActiveDocument.addObject('Part::Sweep','nSS_tube1')
else:
   sweepnSS=App.ActiveDocument.addObject('Part::Sweep','nSS_tube')
sweepnSS.Sections=[profilenSS1,profilenSS2, profilenSS3]
sweepnSS.Spine=App.ActiveDocument.getObject('nSS3D_CL')
sweepnSS.Solid=True
sweepnSS.Frenet=False
sweepnSS.Transition=2

App.ActiveDocument.recompute()
App.activeDocument().nSS3D_CL.Visibility = False
App.activeDocument().nSS_XSec1.Visibility = False
if dropTool:
   App.activeDocument().addObject("Part::Cut",'nSS_tube')
   App.ActiveDocument.ActiveObject.Base=App.activeDocument().nSS_tube1
   App.ActiveDocument.ActiveObject.Tool=App.activeDocument().DropoutTOOL
   App.ActiveDocument.recompute()
App.activeDocument().nSS_XSec2.Visibility = False
App.activeDocument().nSS_XSec3.Visibility = False
App.activeDocument().nSS_XSec4.Visibility = False
myssB = Part.makeCylinder(8.0, 58.869, Base.Vector(597.323,649.366,29.435), Base.Vector(0.0,0.0,-58.869))
obj=App.ActiveDocument.addObject('Part::Feature','ssBridge')
obj.Shape=myssB
mycsB = Part.makeCylinder(9.0, 56.66, Base.Vector(733.808,287.134,28.33), Base.Vector(0.0,0.0,-56.66))
obj=App.ActiveDocument.addObject('Part::Feature','csBridge')
obj.Shape=mycsB
profileDT1=App.ActiveDocument.addObject("Part::Feature","DT_XSec1")
profileDT1.Shape=Part.makeCircle(17.5, Base.Vector(793.309,279.0, 0.0), Base.Vector(0.64381206, 0.7651837, 0))
WireCLDT=Part.makeLine((793.309,279.0, 0.0), (1218.058,783.822, 0.0))
spineDT=App.ActiveDocument.addObject("Part::Feature","DT_CLine")
spineDT.Shape=WireCLDT
sweepDT=App.ActiveDocument.addObject('Part::Sweep','DT_tube')
sweepDT.Sections=[profileDT1]
sweepDT.Spine=spineDT
sweepDT.Solid=True
sweepDT.Frenet=False
sweepDT.Transition=2
App.ActiveDocument.recompute()
App.activeDocument().DT_CLine.Visibility = False
App.activeDocument().DT_XSec1.Visibility = False

profileST1=App.ActiveDocument.addObject("Part::Feature","ST_XSec1")
profileST1.Shape=Part.makeCircle(14.3, Base.Vector(793.309,279.0, 0.0), Base.Vector(-0.2890318, 0.9573195, 0))
WireCLST=Part.makeLine((793.309,279.0, 0.0), (648.794,757.66, 0.0))
profileST3=App.ActiveDocument.addObject("Part::Feature","ST_XSec3")
profileST3.Shape=Part.makeCircle(14.9, Base.Vector(648.794,757.66, 0.0), Base.Vector(-0.2890318, 0.9573195, 0))

spineST=App.ActiveDocument.addObject("Part::Feature","ST_CLine")
spineST.Shape=WireCLST
sweepST=App.ActiveDocument.addObject('Part::Sweep','ST_tube')
sweepST.Sections=[profileST1, profileST3]
sweepST.Spine=spineST
sweepST.Solid=True
sweepST.Frenet=False
sweepST.Transition=2
App.ActiveDocument.recompute()
App.activeDocument().ST_CLine.Visibility = False
App.activeDocument().ST_XSec1.Visibility = False
App.activeDocument().ST_XSec3.Visibility = False

profileTT1=App.ActiveDocument.addObject("Part::Feature","TT_XSec1")
profileTT1.Shape=Part.makeCircle(14.3, Base.Vector(660.355,719.367, 0.0), Base.Vector(0.97863716, 0.20559515, 0))
WireCLTT=Part.makeLine((660.355,719.367, 0.0), (1201.848,833.125, 0.0))
spineTT=App.ActiveDocument.addObject("Part::Feature","TT_CLine")
spineTT.Shape=WireCLTT
sweepTT=App.ActiveDocument.addObject('Part::Sweep','TT_tube')
sweepTT.Sections=[profileTT1]
sweepTT.Spine=spineTT
sweepTT.Solid=True
sweepTT.Frenet=False
sweepTT.Transition=2
App.ActiveDocument.recompute()
App.activeDocument().TT_CLine.Visibility = False
App.activeDocument().TT_XSec1.Visibility = False

GBox = False
myBB = Part.makeCylinder(25.4, 73.0, Base.Vector(793.309,279.0, -36.5), Base.Vector(0, 0, 1))
obj=App.ActiveDocument.addObject('Part::Feature','BBGearBoxCut')
obj.Shape=myBB
myBBid = Part.makeCylinder(BB_id/2, 146.0, Base.Vector(793.309,279.0, -73.0), Base.Vector(0, 0, 1))
obj=App.ActiveDocument.addObject('Part::Feature','BBid')
obj.Shape=myBBid
App.activeDocument().addObject("Part::Cut","BB")
App.ActiveDocument.ActiveObject.Base=App.activeDocument().BBGearBoxCut
App.ActiveDocument.ActiveObject.Tool=App.activeDocument().BBid
profile=Part.makeCircle(15.8, Base.Vector(0,0,0), Base.Vector(1,0,0))
profile = Part.Wire(profile)
profile = Part.Face(profile)
profile = profile.extrude(Base.Vector(-350.0,0,0))
profile.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1),106.8)
profile.translate(Base.Vector(606.621,897.341, 0.0))
obj=App.ActiveDocument.addObject("Part::Feature","SPost_extrude")
obj.Shape=profile

App.ActiveDocument.addObject("Part::Cylinder","STPinchBossHole")
App.ActiveDocument.STPinchBossHole.Radius = 5.0
App.ActiveDocument.STPinchBossHole.Height = 5
App.ActiveDocument.STPinchBossHole.Placement = Base.Placement(Base.Vector(632.483,745.946,Pinch_boss_length/2-4),Base.Rotation(0,0,0))
App.ActiveDocument.addObject("Part::Cylinder","STPinchBossThruHole")
App.ActiveDocument.STPinchBossThruHole.Radius = 3
App.ActiveDocument.STPinchBossThruHole.Height = Pinch_boss_length*2
App.ActiveDocument.STPinchBossThruHole.Placement = Base.Placement(Base.Vector(632.483,745.946,-Pinch_boss_length),Base.Rotation(0,0,0))
obj=App.ActiveDocument.addObject('Part::Feature','STslot')
obj.Shape = Part.makeBox(ST_slot_depth+5, 34.0, ST_slot_width, Base.Vector(-ST_slot_depth-5,0.0,0))
App.ActiveDocument.STslot.Placement = Base.Placement(Base.Vector(647.348,762.446,-ST_slot_width/2),Base.Rotation(106.8,0,0))
App.ActiveDocument.addObject("Part::Cylinder","STslotHole")
App.ActiveDocument.STslotHole.Radius = ST_slot_hole_dia/2
App.ActiveDocument.STslotHole.Height = 34.0
App.ActiveDocument.STslotHole.Placement = Base.Placement(Base.Vector(647.348-(ST_slot_depth+5)*-0.289,762.446-(ST_slot_depth+5)*0.957,0),Base.Rotation(16.8,-90,0))
profileSTclampTop1=Part.makeCircle(18.0, Base.Vector(652.84,744.257, 0.0), Base.Vector(-0.2890318, 0.9573195, 0))
profileSTclampTop1 = Part.Face(Part.Wire([profileSTclampTop1]))
STclampTop = profileSTclampTop1.extrude(Base.Vector(-4.335476954167072,14.359792462981009,0))
obj=App.ActiveDocument.addObject('Part::Feature','SeatpostClampTop')
obj.Shape = STclampTop


bez0 = Part.BezierCurve()
bez0.setPoles([Base.Vector(632.581,738.385,0.0), Base.Vector(630.218,738.385,0.0), Base.Vector(628.035,739.919,0.0), Base.Vector(627.317,742.297,0.0)])
bez1 = Part.BezierCurve()
bez1.setPoles([Base.Vector(626.161,746.126,0.0), Base.Vector(625.283,749.034,0.0), Base.Vector(626.929,752.103,0.0), Base.Vector(629.837,752.981,0.0)])
bez2 = Part.BezierCurve()
bez2.setPoles([Base.Vector(643.239,757.027,0.0), Base.Vector(643.769,757.187,0.0), Base.Vector(644.305,757.264,0.0), Base.Vector(644.831,757.264,0.0)])
bez3 = Part.BezierCurve()
bez3.setPoles([Base.Vector(644.831,757.264,0.0), Base.Vector(647.193,757.264,0.0), Base.Vector(649.376,755.73,0.0), Base.Vector(650.094,753.352,0.0)])
bez4 = Part.BezierCurve()
bez4.setPoles([Base.Vector(651.25,749.523,0.0), Base.Vector(652.128,746.615,0.0), Base.Vector(650.483,743.546,0.0), Base.Vector(647.575,742.668,0.0)])
bez5 = Part.BezierCurve()
bez5.setPoles([Base.Vector(634.172,738.621,0.0), Base.Vector(633.642,738.461,0.0), Base.Vector(633.107,738.385,0.0), Base.Vector(632.581,738.385,0.0)])
PinchBoss0=Part.Wire([bez0.toShape(),Part.makeLine((627.317,742.297,0),(626.161,746.126,0)),bez1.toShape(),Part.makeLine((629.837,752.981,0),(643.239,757.027,0)),bez2.toShape(),bez3.toShape(),Part.makeLine((650.094,753.352,0),(651.25,749.523,0)),bez4.toShape(),Part.makeLine((647.575,742.668,0),(634.172,738.621,0)),bez5.toShape(),])

PinchBoss=Part.Face([PinchBoss0,])

PinchBoss.translate(Base.Vector(0,0,-Pinch_boss_length/2))
PinchBoss = PinchBoss.extrude(Base.Vector(0,0,Pinch_boss_length))
obj=App.ActiveDocument.addObject('Part::Feature','STPinchBoss')
obj.Shape = PinchBoss
App.ActiveDocument.addObject("Part::Fuse","SPC")
App.ActiveDocument.SPC.Base = App.activeDocument().SeatpostClampTop
App.ActiveDocument.SPC.Tool = App.ActiveDocument.STPinchBoss
Gui.ActiveDocument.hide("SeatpostClampTop")
Gui.ActiveDocument.hide("STPinchBoss")
App.ActiveDocument.addObject('Part::Extrusion','SPCcut')
f = App.ActiveDocument.getObject('SPCcut')
f.Base = App.ActiveDocument.getObject('ST_XSec3')
f.DirMode = "Custom"
f.Dir = App.Vector(0.289,-0.957, 0.0)
f.DirLink = None
f.LengthFwd = 15.0
f.LengthRev = 0.0
f.Solid = True
f.Reversed = False
f.Symmetric = False
f.TaperAngle = 0.0
f.TaperAngleRev = 0.0
App.ActiveDocument.addObject("Part::Cut","SeatptClamp")
App.ActiveDocument.SeatptClamp.Base = App.ActiveDocument.SPC
App.ActiveDocument.SeatptClamp.Tool = App.ActiveDocument.STslot
Gui.ActiveDocument.SPC.Visibility=False
Gui.ActiveDocument.STslot.Visibility=False
App.ActiveDocument.addObject("Part::Cut","SeatpstClamp")
App.ActiveDocument.SeatpstClamp.Base = App.ActiveDocument.SeatptClamp
App.ActiveDocument.SeatpstClamp.Tool = App.ActiveDocument.SPCcut
Gui.ActiveDocument.SeatptClamp.Visibility=False
Gui.ActiveDocument.SPCcut.Visibility=False
App.ActiveDocument.addObject("Part::Cut","SeatpostClamp")
App.ActiveDocument.SeatpostClamp.Base = App.ActiveDocument.SeatpstClamp
App.ActiveDocument.SeatpostClamp.Tool = App.ActiveDocument.SPost_extrude
Gui.ActiveDocument.SeatpstClamp.Visibility=False
Gui.ActiveDocument.SPost_extrude.Visibility=False
App.activeDocument().addObject("Part::MultiFuse","SPCCuts")
App.activeDocument().SPCCuts.Shapes = [App.activeDocument().STPinchBossHole,App.activeDocument().STPinchBossThruHole]
App.activeDocument().addObject("Part::Cut","Seatpost_clamp_finished")
App.ActiveDocument.ActiveObject.Base=App.activeDocument().SeatpostClamp
App.ActiveDocument.ActiveObject.Tool=App.activeDocument().SPCCuts
App.ActiveDocument.recompute()


App.ActiveDocument.addObject("Part::Cylinder","WBbossSEATTUBEm00")
App.ActiveDocument.WBbossSEATTUBEm00.Radius = 4.5
App.ActiveDocument.WBbossSEATTUBEm00.Height = 2.0
App.ActiveDocument.addObject("Part::Cylinder","WBbossSEATTUBEmp00")
App.ActiveDocument.WBbossSEATTUBEmp00.Radius = Waterbottle_boss_dia/2
App.ActiveDocument.WBbossSEATTUBEmp00.Height = Waterbottle_boss_length-2.0
App.ActiveDocument.WBbossSEATTUBEmp00.Placement = Base.Placement(Base.Vector(0,0,2.0-Waterbottle_boss_length),Base.Rotation(0,0,0))
App.ActiveDocument.addObject("Part::Cylinder","WBbossHSEATTUBEmh00")
App.ActiveDocument.WBbossHSEATTUBEmh00.Radius = Waterbottle_boss_hole_dia/2
App.ActiveDocument.WBbossHSEATTUBEmh00.Height = Waterbottle_boss_length+1
App.ActiveDocument.WBbossHSEATTUBEmh00.Placement = Base.Placement(Base.Vector(0,0,2.0-Waterbottle_boss_length),Base.Rotation(0,0,0))
App.ActiveDocument.addObject("Part::Cylinder","WBbossSEATTUBEm10")
App.ActiveDocument.WBbossSEATTUBEm10.Radius = 4.5
App.ActiveDocument.WBbossSEATTUBEm10.Height = 2.0
App.ActiveDocument.WBbossSEATTUBEm10.Placement = Base.Placement(Base.Vector(64.0,0,0),Base.Rotation(0,0,0))
App.ActiveDocument.addObject("Part::Cylinder","WBbossSEATTUBEmp10")
App.ActiveDocument.WBbossSEATTUBEmp10.Radius = Waterbottle_boss_dia/2
App.ActiveDocument.WBbossSEATTUBEmp10.Height = Waterbottle_boss_length-2.0
App.ActiveDocument.WBbossSEATTUBEmp10.Placement = Base.Placement(Base.Vector(64.0,0,2.0-Waterbottle_boss_length),Base.Rotation(0,0,0))
App.ActiveDocument.addObject("Part::Cylinder","WBbossHSEATTUBEmh10")
App.ActiveDocument.WBbossHSEATTUBEmh10.Radius = Waterbottle_boss_hole_dia/2
App.ActiveDocument.WBbossHSEATTUBEmh10.Height = Waterbottle_boss_length+1
App.ActiveDocument.WBbossHSEATTUBEmh10.Placement = Base.Placement(Base.Vector(64.0,0,2.0-Waterbottle_boss_length),Base.Rotation(0,0,0))
App.activeDocument().addObject("Part::MultiFuse","WBbossSEATTUBEm0")
App.activeDocument().WBbossSEATTUBEm0.Shapes = [App.activeDocument().WBbossSEATTUBEm00,App.activeDocument().WBbossSEATTUBEmp00,App.activeDocument().WBbossSEATTUBEm10,App.activeDocument().WBbossSEATTUBEmp10]
App.ActiveDocument.WBbossSEATTUBEm0.Placement = Base.Placement(Base.Vector(766.696,417.206, 0.0),Base.Rotation(106.731,0,90))
App.activeDocument().addObject("Part::MultiFuse","WBbossHolesSEATTUBEm0")
App.activeDocument().WBbossHolesSEATTUBEm0.Shapes = [App.activeDocument().WBbossHSEATTUBEmh00,App.activeDocument().WBbossHSEATTUBEmh10]
App.ActiveDocument.WBbossHolesSEATTUBEm0.Placement = Base.Placement(Base.Vector(766.696,417.206, 0.0),Base.Rotation(106.731,0,90))
App.activeDocument().addObject("Part::Cut","WBbossDrilledSEATTUBEm0")
App.ActiveDocument.ActiveObject.Base=App.activeDocument().WBbossSEATTUBEm0
App.ActiveDocument.ActiveObject.Tool=App.activeDocument().WBbossHolesSEATTUBEm0
App.ActiveDocument.recompute()
App.ActiveDocument.addObject("Part::Cylinder","WBbossDOWNTUBEm00")
App.ActiveDocument.WBbossDOWNTUBEm00.Radius = 4.5
App.ActiveDocument.WBbossDOWNTUBEm00.Height = 2.0
App.ActiveDocument.addObject("Part::Cylinder","WBbossDOWNTUBEmp00")
App.ActiveDocument.WBbossDOWNTUBEmp00.Radius = Waterbottle_boss_dia/2
App.ActiveDocument.WBbossDOWNTUBEmp00.Height = Waterbottle_boss_length-2.0
App.ActiveDocument.WBbossDOWNTUBEmp00.Placement = Base.Placement(Base.Vector(0,0,2.0-Waterbottle_boss_length),Base.Rotation(0,0,0))
App.ActiveDocument.addObject("Part::Cylinder","WBbossHDOWNTUBEmh00")
App.ActiveDocument.WBbossHDOWNTUBEmh00.Radius = Waterbottle_boss_hole_dia/2
App.ActiveDocument.WBbossHDOWNTUBEmh00.Height = Waterbottle_boss_length+1
App.ActiveDocument.WBbossHDOWNTUBEmh00.Placement = Base.Placement(Base.Vector(0,0,2.0-Waterbottle_boss_length),Base.Rotation(0,0,0))
App.ActiveDocument.addObject("Part::Cylinder","WBbossDOWNTUBEm10")
App.ActiveDocument.WBbossDOWNTUBEm10.Radius = 4.5
App.ActiveDocument.WBbossDOWNTUBEm10.Height = 2.0
App.ActiveDocument.WBbossDOWNTUBEm10.Placement = Base.Placement(Base.Vector(64.0,0,0),Base.Rotation(0,0,0))
App.ActiveDocument.addObject("Part::Cylinder","WBbossDOWNTUBEmp10")
App.ActiveDocument.WBbossDOWNTUBEmp10.Radius = Waterbottle_boss_dia/2
App.ActiveDocument.WBbossDOWNTUBEmp10.Height = Waterbottle_boss_length-2.0
App.ActiveDocument.WBbossDOWNTUBEmp10.Placement = Base.Placement(Base.Vector(64.0,0,2.0-Waterbottle_boss_length),Base.Rotation(0,0,0))
App.ActiveDocument.addObject("Part::Cylinder","WBbossHDOWNTUBEmh10")
App.ActiveDocument.WBbossHDOWNTUBEmh10.Radius = Waterbottle_boss_hole_dia/2
App.ActiveDocument.WBbossHDOWNTUBEmh10.Height = Waterbottle_boss_length+1
App.ActiveDocument.WBbossHDOWNTUBEmh10.Placement = Base.Placement(Base.Vector(64.0,0,2.0-Waterbottle_boss_length),Base.Rotation(0,0,0))
App.activeDocument().addObject("Part::MultiFuse","WBbossDOWNTUBEm0")
App.activeDocument().WBbossDOWNTUBEm0.Shapes = [App.activeDocument().WBbossDOWNTUBEm00,App.activeDocument().WBbossDOWNTUBEmp00,App.activeDocument().WBbossDOWNTUBEm10,App.activeDocument().WBbossDOWNTUBEmp10]
App.ActiveDocument.WBbossDOWNTUBEm0.Placement = Base.Placement(Base.Vector(940.872,481.563, 0.0),Base.Rotation(49.923,0,-90))
App.activeDocument().addObject("Part::MultiFuse","WBbossHolesDOWNTUBEm0")
App.activeDocument().WBbossHolesDOWNTUBEm0.Shapes = [App.activeDocument().WBbossHDOWNTUBEmh00,App.activeDocument().WBbossHDOWNTUBEmh10]
App.ActiveDocument.WBbossHolesDOWNTUBEm0.Placement = Base.Placement(Base.Vector(940.872,481.563, 0.0),Base.Rotation(49.923,0,-90))
App.activeDocument().addObject("Part::Cut","WBbossDrilledDOWNTUBEm0")
App.ActiveDocument.ActiveObject.Base=App.activeDocument().WBbossDOWNTUBEm0
App.ActiveDocument.ActiveObject.Tool=App.activeDocument().WBbossHolesDOWNTUBEm0
App.ActiveDocument.recompute()
App.ActiveDocument.recompute()
App.activeDocument().addObject("Part::MultiFuse","STCuts")
App.activeDocument().STCuts.Shapes = [App.activeDocument().SPost_extrude, App.activeDocument().BBGearBoxCut,App.ActiveDocument.WBbossHolesSEATTUBEm0,App.activeDocument().STslot,App.activeDocument().STslotHole,App.activeDocument().DT_tube]
App.activeDocument().addObject("Part::Cut","ST_tube_trimmed")
App.ActiveDocument.ActiveObject.Base=App.activeDocument().ST_tube
App.ActiveDocument.ActiveObject.Tool=App.activeDocument().STCuts
App.ActiveDocument.recompute()
App.activeDocument().addObject("Part::MultiFuse","DTCuts")
App.activeDocument().DTCuts.Shapes = [App.activeDocument().HT_tube,App.activeDocument().BBGearBoxCut,App.ActiveDocument.WBbossHolesDOWNTUBEm0]
App.activeDocument().addObject("Part::Cut","DT_tube_trimmed")
App.activeDocument().DT_tube_trimmed.Base = App.activeDocument().DT_tube
App.activeDocument().DT_tube_trimmed.Tool = App.activeDocument().DTCuts
Gui.activeDocument().DT_tube.Visibility=False
App.ActiveDocument.recompute()
App.activeDocument().addObject("Part::MultiFuse","TTCuts")
App.activeDocument().TTCuts.Shapes = [App.activeDocument().HT_tube,App.activeDocument().ST_tube]
App.activeDocument().addObject("Part::Cut","TT_tube_trimmed")
App.activeDocument().TT_tube_trimmed.Base = App.activeDocument().TT_tube
App.activeDocument().TT_tube_trimmed.Tool = App.activeDocument().TTCuts
Gui.activeDocument().TT_tube.Visibility=False
App.ActiveDocument.recompute()
App.activeDocument().addObject("Part::Cut","dSS_tube_trimmed")
App.activeDocument().dSS_tube_trimmed.Base = App.activeDocument().dSS_tube
App.activeDocument().dSS_tube_trimmed.Tool = App.activeDocument().ST_tube
Gui.activeDocument().dSS_tube.Visibility=False
App.activeDocument().addObject("Part::Cut","nSS_tube_trimmed")
App.activeDocument().nSS_tube_trimmed.Base = App.activeDocument().nSS_tube
App.activeDocument().nSS_tube_trimmed.Tool = App.activeDocument().ST_tube
Gui.activeDocument().nSS_tube.Visibility=False
App.ActiveDocument.recompute()
App.ActiveDocument.addObject("Part::Box","nCSChop")
App.ActiveDocument.nCSChop.Length=50.00
App.ActiveDocument.nCSChop.Width=100.00
App.ActiveDocument.nCSChop.Height=200.00
App.ActiveDocument.nCSChop.Placement = Base.Placement(Base.Vector(786.538,229.461, -100.0),Base.Rotation(-7.7839794056483305,0,0))
App.activeDocument().addObject("Part::MultiFuse","nCSCut")
App.activeDocument().nCSCut.Shapes = [App.activeDocument().BBGearBoxCut,App.activeDocument().nCSChop,App.activeDocument().ST_tube]
App.ActiveDocument.addObject("Part::Box","dCSChop")
App.ActiveDocument.dCSChop.Length=50.00
App.ActiveDocument.dCSChop.Width=100.00
App.ActiveDocument.dCSChop.Height=200.00
App.ActiveDocument.dCSChop.Placement = Base.Placement(Base.Vector(786.538,229.461, -100.0),Base.Rotation(-7.7839794056483305,0,0))
App.activeDocument().addObject("Part::MultiFuse","dCSCut")
App.activeDocument().dCSCut.Shapes = [App.activeDocument().BBGearBoxCut,App.activeDocument().dCSChop,App.activeDocument().ST_tube]
App.activeDocument().addObject("Part::Cut","dCS_tube_trimmed")
App.activeDocument().dCS_tube_trimmed.Base = App.activeDocument().dCS_tube
App.activeDocument().dCS_tube_trimmed.Tool = App.activeDocument().dCSCut
Gui.activeDocument().dCS_tube.Visibility=False
App.activeDocument().addObject("Part::Cut","nCS_tube_trimmed")
App.activeDocument().nCS_tube_trimmed.Base = App.activeDocument().nCS_tube
App.activeDocument().nCS_tube_trimmed.Tool = App.activeDocument().nCSCut
Gui.activeDocument().nCS_tube.Visibility=False
App.ActiveDocument.recompute()

bez0 = Part.BezierCurve()
bez0.setPoles([Base.Vector(0.0,0.0,0.0), Base.Vector(20.0,0.0,0.0), Base.Vector(20.0,27.0,0.0)])
bez1 = Part.BezierCurve()
bez1.setPoles([Base.Vector(20.0,27.0,0.0), Base.Vector(20.0,32.5,0.0), Base.Vector(9.0,38.0,0.0)])
bez2 = Part.BezierCurve()
bez2.setPoles([Base.Vector(-9.0,38.0,0.0), Base.Vector(-20.0,32.5,0.0), Base.Vector(-20.0,27.0,0.0)])
bez3 = Part.BezierCurve()
bez3.setPoles([Base.Vector(-20.0,27.0,0.0), Base.Vector(-20.0,0.0,0.0), Base.Vector(0.0,0.0,0.0)])
TireRProf0=Part.Wire([bez0.toShape(),bez1.toShape(),Part.makeLine((9.0,38.0,0),(-9.0,38.0,0)),bez2.toShape(),bez3.toShape(),])

TireRProf=Part.Face([TireRProf0,])

App.ActiveDocument.addObject("Part::Revolution","TireR")
obj=App.ActiveDocument.addObject('Part::Feature','TireR_profile')
obj.Shape=TireRProf0
App.ActiveDocument.TireR.Source = App.ActiveDocument.TireR_profile
App.ActiveDocument.TireR.Axis = (1,0,0)
App.ActiveDocument.TireR.Base = (365.0,355.0, 0.0)
App.ActiveDocument.TireR.Angle = 360.0
App.ActiveDocument.TireR.Solid = True
App.ActiveDocument.TireR.Symmetric = False
App.ActiveDocument.TireR_profile.Visibility = False
App.ActiveDocument.TireR.Placement = Base.Placement(Base.Vector(365.0,0,0),Base.Rotation(0,90,0))
App.ActiveDocument.recompute()

RIMSWRProf0=Part.Wire([Part.makeLine((-9.0,38.0,0),(-9.0,48.0,0)),Part.makeLine((-9.0,48.0,0),(9.0,48.0,0)),Part.makeLine((9.0,48.0,0),(9.0,38.0,0)),Part.makeLine((9.0,38.0,0),(-9.0,38.0,0.0) )])

RIMSWRProf=Part.Face([RIMSWRProf0,])

App.ActiveDocument.addObject("Part::Revolution","RIMSWR")
obj=App.ActiveDocument.addObject('Part::Feature','RIMSWR_profile')
obj.Shape=RIMSWRProf0
App.ActiveDocument.RIMSWR.Source = App.ActiveDocument.RIMSWR_profile
App.ActiveDocument.RIMSWR.Axis = (1,0,0)
App.ActiveDocument.RIMSWR.Base = (365.0,355.0, 0.0)
App.ActiveDocument.RIMSWR.Angle = 360.0
App.ActiveDocument.RIMSWR.Solid = True
App.ActiveDocument.RIMSWR.Symmetric = False
App.ActiveDocument.RIMSWR_profile.Visibility = False
App.ActiveDocument.RIMSWR.Placement = Base.Placement(Base.Vector(365.0,0,0),Base.Rotation(0,90,0))
App.ActiveDocument.recompute()

bez0 = Part.BezierCurve()
bez0.setPoles([Base.Vector(9.0,48.0,0.0), Base.Vector(9.0,58.0,0.0), Base.Vector(0.0,58.0,0.0)])
bez1 = Part.BezierCurve()
bez1.setPoles([Base.Vector(0.0,58.0,0.0), Base.Vector(-9.0,58.0,0.0), Base.Vector(-9.0,48.0,0.0)])
RIMRProf0=Part.Wire([bez0.toShape(),bez1.toShape(),Part.makeLine((-9.0,48.0,0),(9.0,48.0,0.0) )])

RIMRProf=Part.Face([RIMRProf0,])

App.ActiveDocument.addObject("Part::Revolution","RIMR")
obj=App.ActiveDocument.addObject('Part::Feature','RIMR_profile')
obj.Shape=RIMRProf0
App.ActiveDocument.RIMR.Source = App.ActiveDocument.RIMR_profile
App.ActiveDocument.RIMR.Axis = (1,0,0)
App.ActiveDocument.RIMR.Base = (365.0,355.0, 0.0)
App.ActiveDocument.RIMR.Angle = 360.0
App.ActiveDocument.RIMR.Solid = True
App.ActiveDocument.RIMR.Symmetric = False
App.ActiveDocument.RIMR_profile.Visibility = False
App.ActiveDocument.RIMR.Placement = Base.Placement(Base.Vector(365.0,0,0),Base.Rotation(0,90,0))
App.ActiveDocument.recompute()
App.ActiveDocument.addObject("Part::Cylinder","RCut")
App.ActiveDocument.RCut.Radius = 336.0
App.ActiveDocument.RCut.Height = 400
App.ActiveDocument.RCut.Placement = Base.Placement(Base.Vector(365.0,355.0, -200.0),Base.Rotation(0,0,0))
App.activeDocument().addObject("Part::Cut","Tire_R")
App.ActiveDocument.ActiveObject.Base=App.activeDocument().TireR
App.ActiveDocument.ActiveObject.Tool=App.activeDocument().RCut
App.activeDocument().addObject("Part::MultiCommon","TIRESWR")
App.activeDocument().TIRESWR.Shapes = [App.activeDocument().TireR,App.activeDocument().RCut]
App.ActiveDocument.recompute()

bez0 = Part.BezierCurve()
bez0.setPoles([Base.Vector(0.0,0.0,0.0), Base.Vector(20.0,0.0,0.0), Base.Vector(20.0,27.0,0.0)])
bez1 = Part.BezierCurve()
bez1.setPoles([Base.Vector(20.0,27.0,0.0), Base.Vector(20.0,32.5,0.0), Base.Vector(9.0,38.0,0.0)])
bez2 = Part.BezierCurve()
bez2.setPoles([Base.Vector(-9.0,38.0,0.0), Base.Vector(-20.0,32.5,0.0), Base.Vector(-20.0,27.0,0.0)])
bez3 = Part.BezierCurve()
bez3.setPoles([Base.Vector(-20.0,27.0,0.0), Base.Vector(-20.0,0.0,0.0), Base.Vector(0.0,0.0,0.0)])
TireFProf0=Part.Wire([bez0.toShape(),bez1.toShape(),Part.makeLine((9.0,38.0,0),(-9.0,38.0,0)),bez2.toShape(),bez3.toShape(),])

TireFProf=Part.Face([TireFProf0,])

App.ActiveDocument.addObject("Part::Revolution","TireF")
obj=App.ActiveDocument.addObject('Part::Feature','TireF_profile')
obj.Shape=TireFProf0
App.ActiveDocument.TireF.Source = App.ActiveDocument.TireF_profile
App.ActiveDocument.TireF.Axis = (1,0,0)
App.ActiveDocument.TireF.Base = (1406.417,355.0, 0.0)
App.ActiveDocument.TireF.Angle = 360.0
App.ActiveDocument.TireF.Solid = True
App.ActiveDocument.TireF.Symmetric = False
App.ActiveDocument.TireF_profile.Visibility = False
App.ActiveDocument.TireF.Placement = Base.Placement(Base.Vector(1406.417,0,0),Base.Rotation(0,90,0))
App.ActiveDocument.recompute()

RIMSWFProf0=Part.Wire([Part.makeLine((-9.0,38.0,0),(-9.0,48.0,0)),Part.makeLine((-9.0,48.0,0),(9.0,48.0,0)),Part.makeLine((9.0,48.0,0),(9.0,38.0,0)),Part.makeLine((9.0,38.0,0),(-9.0,38.0,0.0) )])

RIMSWFProf=Part.Face([RIMSWFProf0,])

App.ActiveDocument.addObject("Part::Revolution","RIMSWF")
obj=App.ActiveDocument.addObject('Part::Feature','RIMSWF_profile')
obj.Shape=RIMSWFProf0
App.ActiveDocument.RIMSWF.Source = App.ActiveDocument.RIMSWF_profile
App.ActiveDocument.RIMSWF.Axis = (1,0,0)
App.ActiveDocument.RIMSWF.Base = (1406.417,355.0, 0.0)
App.ActiveDocument.RIMSWF.Angle = 360.0
App.ActiveDocument.RIMSWF.Solid = True
App.ActiveDocument.RIMSWF.Symmetric = False
App.ActiveDocument.RIMSWF_profile.Visibility = False
App.ActiveDocument.RIMSWF.Placement = Base.Placement(Base.Vector(1406.417,0,0),Base.Rotation(0,90,0))
App.ActiveDocument.recompute()

bez0 = Part.BezierCurve()
bez0.setPoles([Base.Vector(9.0,48.0,0.0), Base.Vector(9.0,58.0,0.0), Base.Vector(0.0,58.0,0.0)])
bez1 = Part.BezierCurve()
bez1.setPoles([Base.Vector(0.0,58.0,0.0), Base.Vector(-9.0,58.0,0.0), Base.Vector(-9.0,48.0,0.0)])
RIMFProf0=Part.Wire([bez0.toShape(),bez1.toShape(),Part.makeLine((-9.0,48.0,0),(9.0,48.0,0.0) )])

RIMFProf=Part.Face([RIMFProf0,])

App.ActiveDocument.addObject("Part::Revolution","RIMF")
obj=App.ActiveDocument.addObject('Part::Feature','RIMF_profile')
obj.Shape=RIMFProf0
App.ActiveDocument.RIMF.Source = App.ActiveDocument.RIMF_profile
App.ActiveDocument.RIMF.Axis = (1,0,0)
App.ActiveDocument.RIMF.Base = (1406.417,355.0, 0.0)
App.ActiveDocument.RIMF.Angle = 360.0
App.ActiveDocument.RIMF.Solid = True
App.ActiveDocument.RIMF.Symmetric = False
App.ActiveDocument.RIMF_profile.Visibility = False
App.ActiveDocument.RIMF.Placement = Base.Placement(Base.Vector(1406.417,0,0),Base.Rotation(0,90,0))
App.ActiveDocument.recompute()
App.ActiveDocument.addObject("Part::Cylinder","FCut")
App.ActiveDocument.FCut.Radius = 336.0
App.ActiveDocument.FCut.Height = 400
App.ActiveDocument.FCut.Placement = Base.Placement(Base.Vector(1406.417,355.0, -200.0),Base.Rotation(0,0,0))
App.activeDocument().addObject("Part::Cut","Tire_F")
App.ActiveDocument.ActiveObject.Base=App.activeDocument().TireF
App.ActiveDocument.ActiveObject.Tool=App.activeDocument().FCut
App.activeDocument().addObject("Part::MultiCommon","TIRESWF")
App.activeDocument().TIRESWF.Shapes = [App.activeDocument().TireF,App.activeDocument().FCut]
App.ActiveDocument.recompute()
Gui.getDocument('bike_v4').getObject('WBbossDrilledSEATTUBEm0').ShapeColor=(1.0,1.0,1.0)
Gui.getDocument('bike_v4').getObject('WBbossDrilledSEATTUBEm0').Transparency=0
Gui.getDocument('bike_v4').getObject('WBbossDrilledDOWNTUBEm0').ShapeColor=(1.0,1.0,1.0)
Gui.getDocument('bike_v4').getObject('WBbossDrilledDOWNTUBEm0').Transparency=0
Gui.getDocument('bike_v4').getObject('HT_Finished').ShapeColor=(1.0,1.0,1.0)
Gui.getDocument('bike_v4').getObject('HT_Finished').Transparency=0
Gui.getDocument('bike_v4').getObject('ST_tube_trimmed').ShapeColor=(1.0,1.0,1.0)
Gui.getDocument('bike_v4').getObject('ST_tube_trimmed').Transparency=0
Gui.getDocument('bike_v4').getObject('DT_tube_trimmed').ShapeColor=(1.0,1.0,1.0)
Gui.getDocument('bike_v4').getObject('DT_tube_trimmed').Transparency=0
Gui.getDocument('bike_v4').getObject('TT_tube_trimmed').ShapeColor=(1.0,1.0,1.0)
Gui.getDocument('bike_v4').getObject('TT_tube_trimmed').Transparency=0
Gui.getDocument('bike_v4').getObject('dSS_tube_trimmed').ShapeColor=(1.0,1.0,1.0)
Gui.getDocument('bike_v4').getObject('dSS_tube_trimmed').Transparency=0
Gui.getDocument('bike_v4').getObject('nSS_tube_trimmed').ShapeColor=(1.0,1.0,1.0)
Gui.getDocument('bike_v4').getObject('nSS_tube_trimmed').Transparency=0
Gui.getDocument('bike_v4').getObject('ssBridge').ShapeColor=(1.0,1.0,1.0)
Gui.getDocument('bike_v4').getObject('ssBridge').Transparency=0
Gui.getDocument('bike_v4').getObject('dCS_tube_trimmed').ShapeColor=(1.0,1.0,1.0)
Gui.getDocument('bike_v4').getObject('dCS_tube_trimmed').Transparency=0
Gui.getDocument('bike_v4').getObject('nCS_tube_trimmed').ShapeColor=(1.0,1.0,1.0)
Gui.getDocument('bike_v4').getObject('nCS_tube_trimmed').Transparency=0
Gui.getDocument('bike_v4').getObject('csBridge').ShapeColor=(1.0,1.0,1.0)
Gui.getDocument('bike_v4').getObject('csBridge').Transparency=0
Gui.getDocument('bike_v4').getObject('BB').ShapeColor=(1.0,1.0,1.0)
Gui.getDocument('bike_v4').getObject('BB').Transparency=0
Gui.getDocument('bike_v4').getObject('Headset').ShapeColor=(0.8,0.0,0.2)
Gui.getDocument('bike_v4').getObject('Headset').Transparency=0
if dropR:
   Gui.getDocument('bike_v4').getObject('DropoutR').ShapeColor=(1.0,1.0,1.0)
   Gui.getDocument('bike_v4').getObject('DropoutR').Transparency=0
if dropL:
   Gui.getDocument('bike_v4').getObject('DropoutL').ShapeColor=(1.0,1.0,1.0)
   Gui.getDocument('bike_v4').getObject('DropoutL').Transparency=0
if insertDropR:
   Gui.getDocument('bike_v4').getObject('DropoutInsertR').ShapeColor=(0.003921569,0.003921569,0.003921569)
   Gui.getDocument('bike_v4').getObject('DropoutInsertR').Transparency=0
if insertDropL:
   Gui.getDocument('bike_v4').getObject('DropoutInsertL').ShapeColor=(0.003921569,0.003921569,0.003921569)
   Gui.getDocument('bike_v4').getObject('DropoutInsertL').Transparency=0
if boltsLDrop:
   Gui.getDocument('bike_v4').getObject('DropoutBoltsL').ShapeColor=(0.6,0.6,0.6)
   Gui.getDocument('bike_v4').getObject('DropoutBoltsL').Transparency=0
if boltsRDrop:
   Gui.getDocument('bike_v4').getObject('DropoutBoltsR').ShapeColor=(0.6,0.6,0.6)
   Gui.getDocument('bike_v4').getObject('DropoutBoltsR').Transparency=0
Gui.getDocument('bike_v4').getObject('Seatpost_clamp_finished').ShapeColor=(0.2,0.2,0.2)
Gui.getDocument('bike_v4').getObject('Seatpost_clamp_finished').Transparency=0
Gui.getDocument('bike_v4').getObject('Tire_R').ShapeColor=(0.25882354,0.24313726,0.24313726)
Gui.getDocument('bike_v4').getObject('Tire_R').Transparency=0
Gui.getDocument('bike_v4').getObject('Tire_F').ShapeColor=(0.25882354,0.24313726,0.24313726)
Gui.getDocument('bike_v4').getObject('Tire_F').Transparency=0
Gui.getDocument('bike_v4').getObject('TIRESWR').ShapeColor=(0.15686275,0.15294118,0.15294118)
Gui.getDocument('bike_v4').getObject('TIRESWR').Transparency=0
Gui.getDocument('bike_v4').getObject('TIRESWF').ShapeColor=(0.15686275,0.15294118,0.15294118)
Gui.getDocument('bike_v4').getObject('TIRESWF').Transparency=0
Gui.getDocument('bike_v4').getObject('RIMR').ShapeColor=(0.003921569,0.003921569,0.003921569)
Gui.getDocument('bike_v4').getObject('RIMR').Transparency=0
Gui.getDocument('bike_v4').getObject('RIMF').ShapeColor=(0.003921569,0.003921569,0.003921569)
Gui.getDocument('bike_v4').getObject('RIMF').Transparency=0
Gui.getDocument('bike_v4').getObject('RIMSWR').ShapeColor=(0.003921569,0.003921569,0.003921569)
Gui.getDocument('bike_v4').getObject('RIMSWR').Transparency=0
Gui.getDocument('bike_v4').getObject('RIMSWF').ShapeColor=(0.003921569,0.003921569,0.003921569)
Gui.getDocument('bike_v4').getObject('RIMSWF').Transparency=0
Gui.SendMsgToActiveView("ViewFit")

# --- jig reference tubes, parallel to seat tube ---
ST_dir = Base.Vector(-0.2890318, 0.9573195, 0.0)
DummyDia = 6.0
DummyLen = 500.0

refs = {
    "JigRef_RearAxle": Base.Vector(365.0,    355.0,   0.0),
    "JigRef_HT_btm":   Base.Vector(1233.425, 737.083, 0.0),
    "JigRef_HT_top":   Base.Vector(1192.821, 860.58,  0.0),
}

for name, pt in refs.items():
    start = pt - ST_dir * (DummyLen / 2.0)
    o = App.ActiveDocument.addObject("Part::Feature", name)
    o.Shape = Part.makeCylinder(DummyDia/2.0, DummyLen, start, ST_dir)
    Gui.ActiveDocument.getObject(name).ShapeColor = (0.9, 0.25, 0.1)
    Gui.ActiveDocument.getObject(name).Transparency = 30

App.ActiveDocument.recompute()


doc = App.ActiveDocument
doc.recompute()

jig = doc.addObject("App::Part", "JigOrientation")
for o in [x for x in doc.Objects if not x.InList and x is not jig]:
    jig.addObject(o)

BB = Base.Vector(793.309, 279.0, 0.0)
jig.Placement = App.Placement(
    Base.Vector(0, 0, 0),                          # or -BB to put BB at origin
    Base.Rotation(Base.Vector(0, 0, 1), -16.8),
    BB                                             # rotate about this point
)
doc.recompute()


import Part
doc = App.ActiveDocument

BB  = Base.Vector(793.309, 279.0, 0.0)
ROT = Base.Rotation(Base.Vector(0, 0, 1), -16.8)

refs = {
    "RearAxle": Base.Vector(365.0,    355.0,   0.0),
    "HT_btm":   Base.Vector(1233.425, 737.083, 0.0),
    "HT_top":   Base.Vector(1192.821, 860.58,  0.0),
}

hits = {}
for name, p in refs.items():
    q = ROT.multVec(p - BB)
    hits[name] = Base.Vector(q.x, 0.0, 0.0)
    print("%-9s  pt (%9.3f, %9.3f)   hit x = %9.3f" % (name, q.x, q.y, q.x))

xs = [v.x for v in hits.values()]
ln = doc.addObject("Part::Feature", "JigRef_Horizontal")
ln.Shape = Part.makeLine(Base.Vector(min(xs)-60, 0, 0), Base.Vector(max(xs)+60, 0, 0))

for name, v in hits.items():
    m = doc.addObject("Part::Feature", "JigHit_" + name)
    m.Shape = Part.makeSphere(4.0, v)
    Gui.ActiveDocument.getObject(m.Name).ShapeColor = (0.1, 0.5, 0.9)

doc.recompute()
Gui.SendMsgToActiveView("ViewFit")