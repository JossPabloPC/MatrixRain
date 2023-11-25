import maya.cmds as cmds
import maya.mel as mel
import random


#Generic
#Materials
shader_nodes = cmds.ls(mat=True)

# Delete each shader node
for shader_node in shader_nodes:
    if shader_node.startswith("typeBlinn"):
        # Delete the shading node
        cmds.delete(shader_node)



#Arnold
sh_name = 'TailMat'

tailMaterial = cmds.shadingNode('aiStandardSurface', asShader = True, n = sh_name)
tailsh_group = cmds.sets(renderable = True, noSurfaceShader = True, em = True, name = "%s_SG"% sh_name)

#Connect lambert to shader group
cmds.connectAttr(f"{tailMaterial}.outColor", f"{tailsh_group}.surfaceShader", force=True)
cmds.setAttr(tailMaterial + ".baseColor",0.5, 1, 0.21 , type="double3" )
cmds.setAttr(tailMaterial + ".emissionColor",0.5, 1, 0.21 , type="double3" )
cmds.setAttr(tailMaterial + ".emission", 1)


#Arnold
headsh_name = 'TailMatHead'

headMaterial = cmds.shadingNode('aiStandardSurface', asShader = True, n = headsh_name)
headsh_group = cmds.sets(renderable = True, noSurfaceShader = True, em = True, name = "%s_SG"% headsh_name)

#Connect lambert to shader group
cmds.connectAttr(f"{headMaterial}.outColor", f"{headsh_group}.surfaceShader", force=True)
cmds.setAttr(headMaterial + ".baseColor",0.7, 1, 0.5 , type="double3" )
cmds.setAttr(headMaterial + ".emissionColor",0.7, 1, 0.5 , type="double3" )
cmds.setAttr(headMaterial + ".emission", 1)


def Lerp(t, a, b):
        return ((b - a) * t) + a


#Changing letters
class TailPart:

    def __init__(self, pos, heat, extrude):
        self.pos          = pos
        self.heat         = heat
        self.obj_name     = ""
        self.material     = None
        self.extruded     = extrude
        self.createTailPart()

    def createTailPart(self):
        

        cmds.CreatePolygonType()
        self.obj_name = cmds.ls(sl=True)[0]
        type_node = cmds.listConnections(f"{self.obj_name}.message")[0]

        framesBetweenLetters = (30 * self.heat * (random.random() + 0.5))
        if(framesBetweenLetters < 1):
            framesBetweenLetters = 1

        cmds.setAttr(self.obj_name + ".translateX", self.pos[0])
        cmds.setAttr(self.obj_name + ".translateY", self.pos[1])
        cmds.setAttr(self.obj_name + ".translateZ", self.pos[2])



        cmds.setAttr("%s.generator" %type_node, 6)
        cmds.setAttr("%s.length" %type_node, 1)
        cmds.setAttr("%s.changeRate" %type_node, framesBetweenLetters)
        cmds.setAttr("%s.randomSeed" %type_node, random.randint(0, 100))
        cmds.setAttr("%s.fontSize" %type_node, 1)
        
        extrudename = type_node[:4] + "Extrude" + type_node[4:]
        cmds.setAttr("%s.extrudeDistance" %extrudename, 0.4)
        cmds.setAttr("%s.extrudeDivisions" %extrudename, 1)

        cmds.setAttr("%s.enableExtrusion" %extrudename, self.extruded)

        cmds.hyperShade(a=sh_name)
        

#Lead letter of each drop    
class TailHead:
    katakana_and_latin = [
    'ア', 'イ', 'ウ', 'エ', 'オ',
    'カ', 'キ', 'ク', 'ケ', 'コ',
    'サ', 'シ', 'ス', 'セ', 'ソ',
    'タ', 'チ', 'ツ', 'テ', 'ト',
    'ナ', 'ニ', 'ヌ', 'ネ', 'ノ',
    'ハ', 'ヒ', 'フ', 'ヘ', 'ホ',
    'マ', 'ミ', 'ム', 'メ', 'モ',
    'ヤ', 'ユ', 'ヨ',
    'ラ', 'リ', 'ル', 'レ', 'ロ',
    'ワ', 'ヲ', 'ン',
    'ガ', 'ギ', 'グ', 'ゲ', 'ゴ',
    'ザ', 'ジ', 'ズ', 'ゼ', 'ゾ',
    'ダ', 'ヂ', 'ヅ', 'デ', 'ド',
    'バ', 'ビ', 'ブ', 'ベ', 'ボ',
    'パ', 'ピ', 'プ', 'ペ', 'ポ']


    
    def __init__(self, pos, extrude):
        self.pos = pos

        cmds.CreatePolygonType()
        self.obj_name = cmds.ls(sl=True)[0]
        type_node = cmds.listConnections("%s.message"%self.obj_name)[0]
        
        cmds.setAttr(self.obj_name + ".translateX", self.pos[0])
        cmds.setAttr(self.obj_name + ".translateY", self.pos[1])
        cmds.setAttr(self.obj_name + ".translateZ", self.pos[2])
        
                  
        randLetterIdx = random.randint(0, len(self.katakana_and_latin)-1)

        self.letter = hex(ord(self.katakana_and_latin[randLetterIdx]))[2:]

        cmds.setAttr("%s.textInput" %type_node, self.letter , type = "string")
        cmds.setAttr("%s.fontSize" %type_node, 1)
        
        extrudename = type_node[:4] + "Extrude" + type_node[4:]
        cmds.setAttr("%s.extrudeDistance" %extrudename, 0.4)
        cmds.setAttr("%s.extrudeDivisions" %extrudename, 1)

        cmds.setAttr("%s.enableExtrusion" %extrudename, extrude)
        cmds.hyperShade(a=headMaterial)


class MatrixTool:

    ventana        = None
    gravity        = 5
    rate           = 10
    letterAmount   = 6
    lifeTime       = 6
    headletters    = []
    traiLetters    = []
    particlesName  = ""
    trailHeat      = 1
    trailRate      = 5
    trailLifeSpan  = 1
    extrudeLetters = 0
    trailVariety   = 1

    def Lerp(self, t, a, b):
        return ((b - a) * t) + a
    
    def onChangeExtrudeValue(self, value):
        self.extrudeLetters = int(value)
        

    def onCreateMatrixRain(self, value):
        self.GenerateRandomLetter()
        self.AnimateLetters()
        
    def onGravityChange(self, value):
        self.gravity = float(value)

    
    def onlifeTimeChange(self, value):
        self.lifeTime = int(value)

    
    def onRateChange(self, value):
        self.rate = int(value)

    def onLetterAmountChange(self, value):
        self.letterAmount = int(value)
    
    def onTrailRateChange(self, value):
        self.trailRate = float(value)

    def onTrailHeatChange(self, value):
        self.trailHeat = float(value)

        
    def onTrailLifeSpanChange(self, value):
        self.trailLifeSpan = float(value)

                
    def onVarietyChange(self, value):
        self.trailVariety = float(value)

    def onDrawCurve(self, value):
        mel.eval("EPCurveTool;")

    def CreateLetters(self):
        for i in range(self.letterAmount):
            a = TailHead([0,0,100], self.extrudeLetters)
            self.headletters.append(a)

    def onChangeHeadColor(self, value):
        result = cmds.colorEditor()
        buffer = result.split()
        if '1' == buffer[3]:
            values = cmds.colorEditor(query=True, rgb=True)

            cmds.setAttr(headMaterial + ".baseColor",values[0], values[1], values[2] , type="double3" )
            cmds.setAttr(headMaterial + ".emissionColor",values[0], values[1], values[2], type="double3" )
            cmds.setAttr(headMaterial + ".emission", 1)

        else:
            cmds.setAttr(headsh_name + ".baseColor",0.7, 1, 0.5 , type="double3" )
            cmds.setAttr(headsh_name + ".emissionColor",0.7, 1, 0.5 , type="double3" )
            cmds.setAttr(headsh_name + ".emission", 1)

    def onChangeTrailColor(self, value):
        result = cmds.colorEditor()
        buffer = result.split()
        if '1' == buffer[3]:
            values = cmds.colorEditor(query=True, rgb=True)
            print ('RGB = ' + str(values))
            cmds.setAttr(sh_name + ".baseColor",values[0], values[1], values[2], type="double3" )
            cmds.setAttr(sh_name + ".emissionColor",values[0], values[1], values[2], type="double3" )
            cmds.setAttr(sh_name + ".emission", 1)

        else:
            cmds.setAttr(sh_name + ".baseColor",0.7, 1, 0.5 , type="double3" )
            cmds.setAttr(sh_name + ".emissionColor",0.7, 1, 0.5 , type="double3" )
            cmds.setAttr(sh_name + ".emission", 1)

    def CreateTrails(self):
        for i in range(int(self.trailVariety)):
            a = TailPart([0,0,100], self.trailHeat, self.extrudeLetters)
            self.traiLetters.append(a)

    def CreateParticleHead(self):
        #Tail head
        curve = cmds.ls(selection=True)
        cmds.emitter(curve,sro = 0, nuv = 0, rnd = 1 , dx =  0, dy =  -1, dz =  0, nsp = 0, spd = self.gravity, sp = 0,  n='myEmitter', typ ="curve", r = self.rate)
        self.particlesName = 'emittedParticles'
        cmds.particle( n=self.particlesName )
        cmds.connectDynamic( self.particlesName, em='myEmitter' )
        curve = cmds.ls(self.particlesName)
        cmds.setAttr("emittedParticlesShape.lifespanMode", 1)
        cmds.setAttr("emittedParticlesShape.lifespan", self.lifeTime)
        
        #Add atribute to particle
        mel.eval("  addAttr -ln \"indexPP0\"  -dt doubleArray  emittedParticlesShape; addAttr -ln \"indexPP\"  -dt doubleArray  emittedParticlesShape; setAttr -e-keyable true emittedParticlesShape.indexPP;")


        self.CreateLetters()

        letternames = []
        for i in range(self.letterAmount):
            letternames.append(self.headletters[i].obj_name)
            cmds.select(self.headletters[i].obj_name, add= True)

        #Set expression
        mel.eval("dynExpression -s \"indexPP = id%" + str(self.letterAmount) +  "\" -c %sShape;" %self.particlesName)



        cmds.particleInstancer( '%sShape'%self.particlesName, addObject=True, object=letternames, cycle='None', cycleStep=1, cycleStepUnits='Frames', levelOfDetail='Geometry', rotationUnits='Degrees', rotationOrder='XYZ', position='worldPosition', age='age' , oi = "indexPP")
        cmds.particleInstancer( self.particlesName, q=True, name=True )
        cmds.particleInstancer( self.particlesName, name='instancer1', q=True, position=True )
    
    def onPrepareCurve(self, value):
        #Trail Head#

        self.CreateParticleHead()

        ###Tail trail###

        emitedParticles = cmds.ls(self.particlesName)
        cmds.select(emitedParticles)

        cmds.emitter(emitedParticles, sro = 0, nuv = 0, rnd = 1 , dx =  0, dy =  0, dz =  0, nsp = 0, spd = 0, sp = 0,  n='myTrailEmitter', typ ="omni", r = self.trailRate)
        trailParticlesName = 'emittedTrailParticles'
        cmds.particle( n=trailParticlesName )
        cmds.connectDynamic( trailParticlesName, em='myTrailEmitter' )
        curve = cmds.ls(trailParticlesName)
        cmds.setAttr("emittedTrailParticlesShape.lifespanMode", 1)
        cmds.setAttr("emittedTrailParticlesShape.lifespan", self.trailLifeSpan)

        #Add atribute to particle
        mel.eval("  addAttr -ln \"indexPP0\"  -dt doubleArray  %sShape; addAttr -ln \"indexPP\"  -dt doubleArray  %sShape; setAttr -e-keyable true %sShape.indexPP;" %(trailParticlesName,trailParticlesName,trailParticlesName))

        #Letter trail object
        self.CreateTrails()

        trailnames = []
        for i in range(len(self.traiLetters)):
            trailnames.append(self.traiLetters[i].obj_name)
            cmds.select(self.traiLetters[i].obj_name, add= True)

        #Set expression
        mel.eval("dynExpression -s \"indexPP = id%" + str(len(self.traiLetters)) +  "\" -c %sShape;" %trailParticlesName)
    

        cmds.particleInstancer( '%sShape'%trailParticlesName, addObject=True, object=trailnames, cycle='None', cycleStep=1, cycleStepUnits='Frames', levelOfDetail='Geometry', rotationUnits='Degrees', rotationOrder='XYZ', position='worldPosition', age='age' , oi = "indexPP")
        cmds.particleInstancer( trailParticlesName, q=True, name=True )
        cmds.particleInstancer( trailParticlesName, name='instancer2', q=True, position=True )

   

    def __init__(self):
        name = "Matrix Tool"

        if cmds.window(name, ex=True):
            cmds.deleteUI(name, window=True)

        self.ventana = cmds.window(name, title=name, widthHeight=(100,100))

        cmds.columnLayout( adjustableColumn=True )
        cmds.setParent( '..' )
        cmds.rowColumnLayout( numberOfColumns = 1)

        cmds.text( label='1.- Draw a Nurb Curve' )
        cmds.button(label='Draw Curve', command=self.onDrawCurve )
        cmds.separator()
        
        cmds.text( label ='Rain parameters')
        cmds.textFieldGrp( label='Rate'    ,        text='10', cc =self.onRateChange)
        cmds.textFieldGrp( label='Speed' ,          text='5', cc = self.onGravityChange)
        cmds.textFieldGrp( label='Lifetime',        text='6', cc = self.onlifeTimeChange)
        cmds.textFieldGrp( label='LetterAmount',    text='6', cc = self.onLetterAmountChange)
        cmds.textFieldGrp( label='Trail rate',    text='5', cc = self.onTrailRateChange)
        cmds.textFieldGrp( label='Trail heat',        text='1', cc = self.onTrailHeatChange)
        cmds.textFieldGrp( label='Trail lifetime',    text='1', cc = self.onTrailLifeSpanChange)
        cmds.textFieldGrp( label='Trail variety',    text='1', cc = self.onVarietyChange)
        cmds.button(label='Change head color', command = self.onChangeHeadColor )
        cmds.button(label='Change trail color', command = self.onChangeTrailColor )

        cmds.checkBox(label='Extrude letters', cc = self.onChangeExtrudeValue)
        

        
        cmds.separator()


        cmds.text( label ='Create Rain')
        cmds.button(label='Prepare selected curve', command = self.onPrepareCurve )
        
    def showUI(self):
        cmds.showWindow(self.ventana)


tool = MatrixTool()
tool.showUI()