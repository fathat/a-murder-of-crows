#!/usr/bin/env python
#
# WARNING: HERE THERE BE DRAGONS!!!!
#
# PREPARE FOR MAGIC NUMBERS!!!
#
# (Seriously this is the scariest part of the code. It's based on
# the box2D ragdoll example but severely hacked up, because we needed
# cool ragdolls in a day. Dont base anything on this ever.)
#
# Here's all you need to know about this file; to make a ragdoll
# you do this:
#
# RagdollDef().CreateBodiesOn(object_you_want_to_store_ragdoll_bits, world, position)
#

import Box2D as box2d
import settings
import random

k_scale = settings.person_size
count = 0

class CColors:
    pass

class DrawData(object):
    def __init__(self, color):
        self.displayList = None
        self.color = color

class RagdollDef(object):
     
    def __init__(self):
        global count
        # BodyDefs
        self.LFootDef=box2d.b2BodyDef()
        self.RFootDef=box2d.b2BodyDef()
        self.LCalfDef=box2d.b2BodyDef()
        self.RCalfDef=box2d.b2BodyDef()
        self.LThighDef=box2d.b2BodyDef()
        self.RThighDef=box2d.b2BodyDef()
        
        self.PelvisDef=box2d.b2BodyDef()
        self.StomachDef=box2d.b2BodyDef()
        self.ChestDef=box2d.b2BodyDef()
        self.NeckDef=box2d.b2BodyDef()
        self.HeadDef=box2d.b2BodyDef()
        
        self.LUpperArmDef=box2d.b2BodyDef()
        self.RUpperArmDef=box2d.b2BodyDef()
        self.LForearmDef=box2d.b2BodyDef()
        self.RForearmDef=box2d.b2BodyDef()
        self.LHandDef=box2d.b2BodyDef()
        self.RHandDef=box2d.b2BodyDef()
       
        # Polygons
        self.LFootPoly=box2d.b2PolygonDef()
        self.RFootPoly=box2d.b2PolygonDef()
        self.LCalfPoly=box2d.b2PolygonDef()
        self.RCalfPoly=box2d.b2PolygonDef()
        self.LThighPoly=box2d.b2PolygonDef()
        self.RThighPoly=box2d.b2PolygonDef()
        self.LFootPoly.friction = 0.7
        self.RFootPoly.friction = 0.7
       
        self.PelvisPoly=box2d.b2PolygonDef()
        self.StomachPoly=box2d.b2PolygonDef()
        self.ChestPoly=box2d.b2PolygonDef()
        self.NeckPoly=box2d.b2PolygonDef()
       
        self.LUpperArmPoly=box2d.b2PolygonDef()
        self.RUpperArmPoly=box2d.b2PolygonDef()
        self.LForearmPoly=box2d.b2PolygonDef()
        self.RForearmPoly=box2d.b2PolygonDef()
        self.LHandPoly=box2d.b2PolygonDef()
        self.RHandPoly=box2d.b2PolygonDef()
        
        # Circles
        self.HeadCirc=box2d.b2CircleDef()
        
        # Revolute Joints
        self.LAnkleDef=box2d.b2RevoluteJointDef()
        self.RAnkleDef=box2d.b2RevoluteJointDef()
        self.LKneeDef=box2d.b2RevoluteJointDef()
        self.RKneeDef=box2d.b2RevoluteJointDef()
        self.LHipDef=box2d.b2RevoluteJointDef()
        self.RHipDef=box2d.b2RevoluteJointDef()
        
        self.LowerAbsDef=box2d.b2RevoluteJointDef()
        self.UpperAbsDef=box2d.b2RevoluteJointDef()
        self.LowerNeckDef=box2d.b2RevoluteJointDef()
        self.UpperNeckDef=box2d.b2RevoluteJointDef()
       
        self.LShoulderDef=box2d.b2RevoluteJointDef()
        self.RShoulderDef=box2d.b2RevoluteJointDef()
        self.LElbowDef=box2d.b2RevoluteJointDef()
        self.RElbowDef=box2d.b2RevoluteJointDef()
        self.LWristDef=box2d.b2RevoluteJointDef()
        self.RWristDef=box2d.b2RevoluteJointDef()
        
        self.iter_polys = ( self.LFootPoly, self.RFootPoly, self.LCalfPoly, self.RCalfPoly, self.LThighPoly, self.RThighPoly,
                self.PelvisPoly, self.StomachPoly, self.ChestPoly, self.NeckPoly,
                self.LUpperArmPoly, self.RUpperArmPoly, self.LForearmPoly, self.RForearmPoly, self.LHandPoly, self.RHandPoly ,
                self.HeadCirc )
        self.iter_defs = ( self.LFootDef, self.RFootDef, self.LCalfDef, self.RCalfDef, self.LThighDef, self.RThighDef,
                self.PelvisDef, self.StomachDef, self.ChestDef, self.NeckDef, self.HeadDef,
                self.LUpperArmDef, self.RUpperArmDef, self.LForearmDef, self.RForearmDef, self.LHandDef, self.RHandDef )
        self.iter_joints=( self.LAnkleDef, self.RAnkleDef, self.LKneeDef, self.RKneeDef, self.LHipDef, self.RHipDef,
                self.LowerAbsDef, self.UpperAbsDef, self.LowerNeckDef, self.UpperNeckDef,
                self.LShoulderDef, self.RShoulderDef, self.LElbowDef, self.RElbowDef, self.LWristDef, self.RWristDef )

        self.SetMotorTorque(2.0)
        self.SetMotorSpeed(0.0)
        self.SetDensity(1.0)
        self.SetRestitution(0.0)
        self.SetLinearDamping(0.0)
        self.SetAngularDamping(0.005)
        count -= 1
        self.SetGroupIndex(count)
        self.EnableMotor()
        self.EnableLimit()

        self.DefaultVertices()
        self.DefaultPositions()
        self.DefaultJoints()

        self.LFootPoly.friction = self.RFootPoly.friction = 1.85

    def CreateBodiesOn(self, person, world, position):
        
        if person.speed > 4 and random.random() > 0.9 :
            Colors = CColors()
            Colors.skin = (0.75, 0.6, 0.5, 1)#(0.9, 0.6, 0.5, 1)
            Colors.shirt = Colors.skin
            Colors.jeans = Colors.skin
            Colors.shoes = (0.65, 0.64, 0.4, 1)
        else:
            Colors = CColors()
            Colors.skin = (0.6, 0.5, 0.75, 1)#(0.75, 0.6, 0.5, 1)
            Colors.shirt = (random.random()*0.25, random.random()*0.05, random.random()*0.4, 1)
            Colors.jeans = (random.random()*0.25, random.random()*0.05, random.random()*0.4, 1)
            Colors.shoes = Colors.skin#(0.0, 0.0, 0.0, 1)
            
        # create body parts
        bdef = self
        bd = bdef.LFootDef
        bd.position += position
        person.LFoot = world.CreateBody(bd)
        person.LFoot.CreateShape(bdef.LFootPoly)
        person.LFoot.SetMassFromShapes()
        person.LFoot.GetShapeList()[0].userData = DrawData(Colors.shoes)
        person.bodies["LFoot"] = person.LFoot

        bd = bdef.RFootDef
        bd.position += position
        person.RFoot = world.CreateBody(bd)
        person.RFoot.CreateShape(bdef.RFootPoly)
        person.RFoot.SetMassFromShapes()
        person.RFoot.GetShapeList()[0].userData = DrawData(Colors.shoes)
        person.bodies["RFoot"] = person.RFoot

        bd = bdef.LCalfDef
        bd.position += position
        person.LCalf = world.CreateBody(bd)
        person.LCalf.CreateShape(bdef.LCalfPoly)
        person.LCalf.SetMassFromShapes()
        person.LCalf.GetShapeList()[0].userData = DrawData(Colors.skin)
        person.bodies["LCalf"] = person.LCalf

        bd = bdef.RCalfDef
        bd.position += position
        person.RCalf = world.CreateBody(bd)
        person.RCalf.CreateShape(bdef.RCalfPoly)
        person.RCalf.SetMassFromShapes()
        person.RCalf.GetShapeList()[0].userData = DrawData(Colors.skin)
        person.bodies["RCalf"] = person.RCalf

        bd = bdef.LThighDef
        bd.position += position
        person.LThigh = world.CreateBody(bd)
        person.LThigh.CreateShape(bdef.LThighPoly)
        person.LThigh.SetMassFromShapes()
        person.LThigh.GetShapeList()[0].userData = DrawData(Colors.jeans)
        person.bodies["LThigh"] = person.LThigh

        bd = bdef.RThighDef
        bd.position += position
        person.RThigh = world.CreateBody(bd)
        person.RThigh.CreateShape(bdef.RThighPoly)
        person.RThigh.SetMassFromShapes()
        person.RThigh.GetShapeList()[0].userData = DrawData(Colors.jeans)
        person.bodies["RThigh"] = person.RThigh

        bd = bdef.PelvisDef
        bd.position += position
        person.Pelvis = world.CreateBody(bd)
        person.Pelvis.CreateShape(bdef.PelvisPoly)
        person.Pelvis.SetMassFromShapes()
        person.Pelvis.GetShapeList()[0].userData = DrawData(Colors.jeans)
        person.bodies["Pelvis"] = person.Pelvis

        bd = bdef.StomachDef
        bd.position += position
        person.Stomach = world.CreateBody(bd)
        person.Stomach.CreateShape(bdef.StomachPoly)
        person.Stomach.SetMassFromShapes()
        person.Stomach.GetShapeList()[0].userData = DrawData(Colors.shirt)
        person.bodies["Stomach"] = person.Stomach

        bd = bdef.ChestDef
        bd.position += position
        person.Chest = world.CreateBody(bd)
        person.Chest.CreateShape(bdef.ChestPoly)
        person.Chest.SetMassFromShapes()
        person.Chest.GetShapeList()[0].userData = DrawData(Colors.shirt)
        person.bodies["Chest"] = person.Chest

        bd = bdef.NeckDef
        bd.position += position
        person.Neck = world.CreateBody(bd)
        person.Neck.CreateShape(bdef.NeckPoly)
        person.Neck.SetMassFromShapes()
        person.Neck.GetShapeList()[0].userData = DrawData(Colors.skin)
        person.bodies["Neck"] = person.Neck

        bd = bdef.HeadDef
        bd.position += position
        person.Head = world.CreateBody(bd)
        person.Head.CreateShape(bdef.HeadCirc)
        person.Head.SetMassFromShapes()
        person.Head.GetShapeList()[0].userData = DrawData(Colors.skin)
        person.bodies["Head"] = person.Head

        bd = bdef.LUpperArmDef
        bd.position += position
        person.LUpperArm = world.CreateBody(bd)
        person.LUpperArm.CreateShape(bdef.LUpperArmPoly)
        person.LUpperArm.SetMassFromShapes()
        person.LUpperArm.GetShapeList()[0].userData = DrawData(Colors.shirt)
        person.bodies["LUpperArm"] = person.LUpperArm

        bd = bdef.RUpperArmDef
        bd.position += position
        person.RUpperArm = world.CreateBody(bd)
        person.RUpperArm.CreateShape(bdef.RUpperArmPoly)
        person.RUpperArm.SetMassFromShapes()
        person.RUpperArm.GetShapeList()[0].userData = DrawData(Colors.shirt)
        person.bodies["RUpperArm"] = person.RUpperArm

        bd = bdef.LForearmDef
        bd.position += position
        person.LForearm = world.CreateBody(bd)
        person.LForearm.CreateShape(bdef.LForearmPoly)
        person.LForearm.SetMassFromShapes()
        person.LForearm.GetShapeList()[0].userData = DrawData(Colors.skin)
        person.bodies["LForearm"] = person.LForearm

        bd = bdef.RForearmDef
        bd.position += position
        person.RForearm = world.CreateBody(bd)
        person.RForearm.CreateShape(bdef.RForearmPoly)
        person.RForearm.SetMassFromShapes()
        person.RForearm.GetShapeList()[0].userData = DrawData(Colors.skin)
        person.bodies["RForearm"] = person.RForearm

        bd = bdef.LHandDef
        bd.position += position
        person.LHand = world.CreateBody(bd)
        person.LHand.CreateShape(bdef.LHandPoly)
        person.LHand.SetMassFromShapes()
        person.LHand.GetShapeList()[0].userData = DrawData(Colors.skin)
        person.bodies["LHand"] = person.LHand

        bd = bdef.RHandDef
        bd.position += position
        person.RHand = world.CreateBody(bd)
        person.RHand.CreateShape(bdef.RHandPoly)
        person.RHand.SetMassFromShapes()
        person.RHand.GetShapeList()[0].userData = DrawData(Colors.skin)
        person.bodies["RHand"] = person.RHand

        # link body parts
        bdef.LAnkleDef.body1	= person.LFoot
        bdef.LAnkleDef.body2	= person.LCalf
        bdef.RAnkleDef.body1	= person.RFoot
        bdef.RAnkleDef.body2	= person.RCalf
        bdef.LKneeDef.body1		= person.LCalf
        bdef.LKneeDef.body2		= person.LThigh
        bdef.RKneeDef.body1		= person.RCalf
        bdef.RKneeDef.body2		= person.RThigh
        bdef.LHipDef.body1		= person.LThigh
        bdef.LHipDef.body2		= person.Pelvis
        bdef.RHipDef.body1		= person.RThigh
        bdef.RHipDef.body2		= person.Pelvis
        bdef.LowerAbsDef.body1	= person.Pelvis
        bdef.LowerAbsDef.body2	= person.Stomach
        bdef.UpperAbsDef.body1	= person.Stomach
        bdef.UpperAbsDef.body2	= person.Chest
        bdef.LowerNeckDef.body1	= person.Chest
        bdef.LowerNeckDef.body2	= person.Neck
        bdef.UpperNeckDef.body1	= person.Chest
        bdef.UpperNeckDef.body2	= person.Head
        bdef.LShoulderDef.body1	= person.Chest
        bdef.LShoulderDef.body2	= person.LUpperArm
        bdef.RShoulderDef.body1	= person.Chest
        bdef.RShoulderDef.body2	= person.RUpperArm
        bdef.LElbowDef.body1	= person.LForearm
        bdef.LElbowDef.body2	= person.LUpperArm
        bdef.RElbowDef.body1	= person.RForearm
        bdef.RElbowDef.body2	= person.RUpperArm
        bdef.LWristDef.body1	= person.LHand
        bdef.LWristDef.body2	= person.LForearm
        bdef.RWristDef.body1	= person.RHand
        bdef.RWristDef.body2	= person.RForearm

        # create joints
        person.LAnkle		= world.CreateJoint(bdef.LAnkleDef).getAsType()
        person.RAnkle		= world.CreateJoint(bdef.RAnkleDef).getAsType()
        person.LKnee		= world.CreateJoint(bdef.LKneeDef).getAsType()
        person.RKnee		= world.CreateJoint(bdef.RKneeDef).getAsType()
        person.LHip		= world.CreateJoint(bdef.LHipDef).getAsType()
        person.RHip		= world.CreateJoint(bdef.RHipDef).getAsType()
        person.LowerAbs	= world.CreateJoint(bdef.LowerAbsDef).getAsType()
        person.UpperAbs	= world.CreateJoint(bdef.UpperAbsDef).getAsType()
        person.LowerNeck	= world.CreateJoint(bdef.LowerNeckDef).getAsType()
        person.UpperNeck	= world.CreateJoint(bdef.UpperNeckDef).getAsType()
        person.LShoulder	= world.CreateJoint(bdef.LShoulderDef).getAsType()
        person.RShoulder	= world.CreateJoint(bdef.RShoulderDef).getAsType()
        person.LElbow		= world.CreateJoint(bdef.LElbowDef).getAsType()
        person.RElbow		= world.CreateJoint(bdef.RElbowDef).getAsType()
        person.LWrist		= world.CreateJoint(bdef.LWristDef).getAsType()
        person.RWrist		= world.CreateJoint(bdef.RWristDef).getAsType()
        person.joints = [
            person.LowerAbs,
            person.UpperAbs,
            person.LHip,
            person.RHip,
            person.LKnee,
            person.RKnee,
            person.LAnkle,
            person.LShoulder,
            person.LowerNeck,
            person.UpperNeck,
            person.RShoulder,
            person.RAnkle, 
            person.LElbow,
            person.RElbow,
            person.LWrist,
            person.RWrist]

    def IsFast(self, b):
        pass

    def SetGroupIndex(self, i):
        for o in self.iter_polys:
            o.filter.groupIndex = i

    def SetLinearDamping(self, f):
        for d in self.iter_defs:
            d.linearDamping = f

    def SetAngularDamping(self, f):
        for d in self.iter_defs:
            d.angularDamping = f

    def SetMotorTorque(self, f):
        for j in self.iter_joints:
            j.maxMotorTorque = f

    def SetMotorSpeed(self,  f):
        for j in self.iter_joints:
            j.motorSpeed = f

    def SetDensity(self,  f):
        for o in self.iter_polys:
            o.density = f

    def SetRestitution(self, f):
        for o in self.iter_polys:
            o.restitution = f

    def EnableLimit(self):
        self.SetLimit(True)

    def DisableLimit(self):
        self.SetLimit(False)

    def SetLimit(self, b):
        for j in self.iter_joints:
            j.enableLimit = b

    def EnableMotor(self):
        self.SetMotor(True)

    def DisableMotor(self):
        self.SetMotor(False)

    def SetMotor(self, b):
        for j in self.iter_joints:
            j.enableMotor = b

    def DefaultVertices(self):
        global k_scale
        # feet
        for poly in (self.LFootPoly, self.RFootPoly):
            poly.setVertices([
                k_scale * box2d.b2Vec2(.033,.143),
                k_scale * box2d.b2Vec2(.023,.033),
                k_scale * box2d.b2Vec2(.267,.035),
                k_scale * box2d.b2Vec2(.265,.065),
                k_scale * box2d.b2Vec2(.117,.143)])
        # calves
        for poly in (self.LCalfPoly, self.RCalfPoly):
            poly.setVertices([
                k_scale * box2d.b2Vec2(.089,.016),
                k_scale * box2d.b2Vec2(.178,.016),
                k_scale * box2d.b2Vec2(.205,.417),
                k_scale * box2d.b2Vec2(.095,.417)])
        # thighs
        for poly in (self.LThighPoly, self.RThighPoly):
            poly.setVertices([
                k_scale * box2d.b2Vec2(.137,.032),
                k_scale * box2d.b2Vec2(.243,.032),
                k_scale * box2d.b2Vec2(.318,.343),
                k_scale * box2d.b2Vec2(.142,.343)])
        # pelvis
        self.PelvisPoly.setVertices([
            k_scale * box2d.b2Vec2(.105,.051),
            k_scale * box2d.b2Vec2(.277,.053),
            k_scale * box2d.b2Vec2(.320,.233),
            k_scale * box2d.b2Vec2(.112,.233),
            k_scale * box2d.b2Vec2(.067,.152)])
        # stomach
        self.StomachPoly.setVertices([
            k_scale * box2d.b2Vec2(.088,.043),
            k_scale * box2d.b2Vec2(.284,.043),
            k_scale * box2d.b2Vec2(.295,.231),
            k_scale * box2d.b2Vec2(.100,.231)])
        # chest
        self.ChestPoly.setVertices([
            k_scale * box2d.b2Vec2(.091,.042),
            k_scale * box2d.b2Vec2(.283,.042),
            k_scale * box2d.b2Vec2(.177,.289),
            k_scale * box2d.b2Vec2(.065,.289)])
        # head
        self.HeadCirc.radius = k_scale * .115
        # neck
        self.NeckPoly.setVertices([
            k_scale * box2d.b2Vec2(.038,.054),
            k_scale * box2d.b2Vec2(.149,.054),
            k_scale * box2d.b2Vec2(.154,.102),
            k_scale * box2d.b2Vec2(.054,.113)])
        # upper arms
        for poly in (self.LUpperArmPoly, self.RUpperArmPoly):
            poly.setVertices([
                k_scale * box2d.b2Vec2(.092,.059),
                k_scale * box2d.b2Vec2(.159,.059),
                k_scale * box2d.b2Vec2(.169,.335),
                k_scale * box2d.b2Vec2(.078,.335),
                k_scale * box2d.b2Vec2(.064,.248)])
        # forearms
        for poly in (self.LForearmPoly, self.RForearmPoly):
            poly.setVertices([
                k_scale * box2d.b2Vec2(.082,.054),
                k_scale * box2d.b2Vec2(.138,.054),
                k_scale * box2d.b2Vec2(.149,.296),
                k_scale * box2d.b2Vec2(.088,.296)])
        # hands
        for poly in (self.LHandPoly, self.RHandPoly):
            poly.setVertices([
                k_scale * box2d.b2Vec2(.066,.031),
                k_scale * box2d.b2Vec2(.123,.020),
                k_scale * box2d.b2Vec2(.160,.127),
                k_scale * box2d.b2Vec2(.127,.178),
                k_scale * box2d.b2Vec2(.074,.178)])

    def DefaultJoints(self):
        global k_scale
        #b.LAnkleDef.body1		= LFoot
        #b.LAnkleDef.body2		= LCalf
        #b.self.RAnkleDef.body1		= self.RFoot
        #b.self.RAnkleDef.body2		= self.RCalf
        # ankles
        anchor = k_scale * box2d.b2Vec2(-.045,-.75)
        self.LAnkleDef.localAnchor1		= self.RAnkleDef.localAnchor1	= anchor - self.LFootDef.position
        self.LAnkleDef.localAnchor2		= self.RAnkleDef.localAnchor2	= anchor - self.LCalfDef.position
        self.LAnkleDef.referenceAngle	= self.RAnkleDef.referenceAngle	= 0.0
        self.LAnkleDef.lowerAngle		= self.RAnkleDef.lowerAngle		= -0.523598776
        self.LAnkleDef.upperAngle		= self.RAnkleDef.upperAngle		= 0.523598776

        #b.self.LKneeDef.body1		= self.LCalf
        #b.self.LKneeDef.body2		= self.LThigh
        #b.self.RKneeDef.body1		= self.RCalf
        #b.self.RKneeDef.body2		= self.RThigh
        # knees
        anchor = k_scale * box2d.b2Vec2(-.030,-.355)
        self.LKneeDef.localAnchor1	= self.RKneeDef.localAnchor1		= anchor - self.LCalfDef.position
        self.LKneeDef.localAnchor2	= self.RKneeDef.localAnchor2		= anchor - self.LThighDef.position
        self.LKneeDef.referenceAngle	= self.RKneeDef.referenceAngle	= 0.0
        self.LKneeDef.lowerAngle		= self.RKneeDef.lowerAngle		= 0
        self.LKneeDef.upperAngle		= self.RKneeDef.upperAngle		= 2.61799388

        #b.self.LHipDef.body1			= self.LThigh
        #b.self.LHipDef.body2			= Pelvis
        #b.self.RHipDef.body1			= self.RThigh
        #b.self.RHipDef.body2			= Pelvis
        # hips
        anchor = k_scale * box2d.b2Vec2(.005,-.045)
        self.LHipDef.localAnchor1	= self.RHipDef.localAnchor1		= anchor - self.LThighDef.position
        self.LHipDef.localAnchor2	= self.RHipDef.localAnchor2		= anchor - self.PelvisDef.position
        self.LHipDef.referenceAngle	= self.RHipDef.referenceAngle	= 0.0
        self.LHipDef.lowerAngle		= self.RHipDef.lowerAngle		= -2.26892803
        self.LHipDef.upperAngle		= self.RHipDef.upperAngle		= 0

        #b.self.LowerAbsDef.body1		= Pelvis
        #b.self.LowerAbsDef.body2		= Stomach
        # lower abs
        anchor = k_scale * box2d.b2Vec2(.035,.135)
        self.LowerAbsDef.localAnchor1	= anchor - self.PelvisDef.position
        self.LowerAbsDef.localAnchor2	= anchor - self.StomachDef.position
        self.LowerAbsDef.referenceAngle	= 0.0
        self.LowerAbsDef.lowerAngle		= -0.523598776
        self.LowerAbsDef.upperAngle		= 0.523598776

        #b.UpperAbsDef.body1		= Stomach
        #b.UpperAbsDef.body2		= Chest
        # upper abs
        anchor = k_scale * box2d.b2Vec2(.045,.320)
        self.UpperAbsDef.localAnchor1	= anchor - self.StomachDef.position
        self.UpperAbsDef.localAnchor2	= anchor - self.ChestDef.position
        self.UpperAbsDef.referenceAngle	= 0.0
        self.UpperAbsDef.lowerAngle		= -0.523598776
        self.UpperAbsDef.upperAngle		= 0.174532925

        #b.self.LowerNeckDef.body1	= Chest
        #b.self.LowerNeckDef.body2	= Neck
        # lower neck
        anchor = k_scale * box2d.b2Vec2(-.015,.575)
        self.LowerNeckDef.localAnchor1	= anchor - self.ChestDef.position
        self.LowerNeckDef.localAnchor2	= anchor - self.NeckDef.position
        self.LowerNeckDef.referenceAngle	= 0.0
        self.LowerNeckDef.lowerAngle		= -0.174532925
        self.LowerNeckDef.upperAngle		= 0.174532925

        #b.self.UpperNeckDef.body1	= Chest
        #b.self.UpperNeckDef.body2	= Head
        # upper neck
        anchor = k_scale * box2d.b2Vec2(-.005,.630)
        self.UpperNeckDef.localAnchor1	= anchor - self.ChestDef.position
        self.UpperNeckDef.localAnchor2	= anchor - self.HeadDef.position
        self.UpperNeckDef.referenceAngle	= 0.0
        self.UpperNeckDef.lowerAngle		= -0.610865238
        self.UpperNeckDef.upperAngle		= 0.785398163

        #b.self.LShoulderDef.body1	= Chest
        #b.self.LShoulderDef.body2	= self.LUpperArm
        #b.self.RShoulderDef.body1	= Chest
        #b.self.RShoulderDef.body2	= self.RUpperArm
        # shoulders
        anchor = k_scale * box2d.b2Vec2(-.015,.545)
        self.LShoulderDef.localAnchor1	= self.RShoulderDef.localAnchor1		= anchor - self.ChestDef.position
        self.LShoulderDef.localAnchor2	= self.RShoulderDef.localAnchor2		= anchor - self.LUpperArmDef.position
        self.LShoulderDef.referenceAngle	= self.RShoulderDef.referenceAngle	= 0.0
        self.LShoulderDef.lowerAngle		= self.RShoulderDef.lowerAngle		= -1.04719755
        self.LShoulderDef.upperAngle		= self.RShoulderDef.upperAngle		= 3.14159265

        #b.self.LElbowDef.body1		= self.LForearm
        #b.self.LElbowDef.body2		= self.LUpperArm
        #b.self.RElbowDef.body1		= self.RForearm
        #b.self.RElbowDef.body2		= self.RUpperArm
        # elbows
        anchor = k_scale * box2d.b2Vec2(-.005,.290)
        self.LElbowDef.localAnchor1		= self.RElbowDef.localAnchor1	= anchor - self.LForearmDef.position
        self.LElbowDef.localAnchor2		= self.RElbowDef.localAnchor2	= anchor - self.LUpperArmDef.position
        self.LElbowDef.referenceAngle	= self.RElbowDef.referenceAngle	= 0.0
        self.LElbowDef.lowerAngle		= self.RElbowDef.lowerAngle		= -2.7925268
        self.LElbowDef.upperAngle		= self.RElbowDef.upperAngle		= 0

        #b.self.LWristDef.body1		= self.LHand
        #b.self.LWristDef.body2		= self.LForearm
        #b.self.RWristDef.body1		= self.RHand
        #b.self.RWristDef.body2		= self.RForearm
        # wrists
        anchor = k_scale * box2d.b2Vec2(-.010,.045)
        self.LWristDef.localAnchor1		= self.RWristDef.localAnchor1	= anchor - self.LHandDef.position
        self.LWristDef.localAnchor2		= self.RWristDef.localAnchor2	= anchor - self.LForearmDef.position
        self.LWristDef.referenceAngle	= self.RWristDef.referenceAngle	= 0.0
        self.LWristDef.lowerAngle		= self.RWristDef.lowerAngle		= -0.174532925
        self.LWristDef.upperAngle		= self.RWristDef.upperAngle		= 0.174532925

    def DefaultPositions(self):
        global k_scale
        for foot in (self.LFootDef, self.RFootDef):
            foot.position		= k_scale * box2d.b2Vec2(-.122,-.901)
        for calf in (self.LCalfDef, self.RCalfDef):
            calf.position		= k_scale * box2d.b2Vec2(-.177,-.771)
        for thigh in (self.LThighDef, self.RThighDef):
            thigh.position		= k_scale * box2d.b2Vec2(-.217,-.391)
        for upperarm in (self.LUpperArmDef, self.RUpperArmDef):
            upperarm.position	= k_scale * box2d.b2Vec2(-.127,.228)
        for forearm in (self.LForearmDef, self.RForearmDef):
            forearm.position    = k_scale * box2d.b2Vec2(-.117,-.011)
        for hand in (self.LHandDef, self.RHandDef):
            hand.position		= k_scale * box2d.b2Vec2(-.112,-.136)

        self.PelvisDef.position	= k_scale * box2d.b2Vec2(-.177,-.101)
        self.StomachDef.position= k_scale * box2d.b2Vec2(-.142,.088)
        self.ChestDef.position	= k_scale * box2d.b2Vec2(-.132,.282)
        self.NeckDef.position	= k_scale * box2d.b2Vec2(-.102,.518)
        self.HeadDef.position	= k_scale * box2d.b2Vec2(.022,.738)

