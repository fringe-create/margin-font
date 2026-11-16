"""Build Margin 1.000 from the bundled OFL-licensed Source Code Pro masters.
Requires Python 3, fonttools[woff], and brotli. Run: python source/build.py
"""
from pathlib import Path
import copy
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.varLib import build
from fontTools.designspaceLib import DesignSpaceDocument, AxisDescriptor, SourceDescriptor, InstanceDescriptor
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
from fontTools.otlLib.builder import buildStatTable

ROOT=Path(__file__).resolve().parents[1]
WEIGHTS={200:'ExtraLight',300:'Light',400:'Regular',500:'Medium',600:'SemiBold',700:'Bold',800:'ExtraBold',900:'Black'}

def names(f, weight, italic, variable=False):
    label=WEIGHTS[weight]+(' Italic' if italic else '')
    if weight==400 and italic: label='Italic'
    legacy='Margin' if weight in (400,700) or variable else 'Margin '+WEIGHTS[weight]
    sub=('Bold' if weight==700 else '')+(' Italic' if italic else '')
    sub=sub.strip() or 'Regular'
    if variable: sub='Italic' if italic else 'Regular'
    ps='Margin-'+('Italic' if italic else 'Regular') if variable else 'Margin-'+label.replace(' ','')
    for nid in (1,2,3,4,5,6,16,17,18,21,22,25):
        f['name'].removeNames(nameID=nid)
    entries={1:legacy,2:sub,3:'1.000;MARG;'+ps,4:'Margin '+label,5:'Version 1.000',6:ps,16:'Margin',17:label,
      7:'Margin is a modified font derived from Source Code Pro.',
      9:'Original: Paul D. Hunt / Adobe. Margin modifications: OpenAI for Margin contributors.',
      10:'A narrower monospaced family with chamfered punctuation and a refined R leg. Derived from Source Code Pro under the SIL Open Font License 1.1.'}
    if variable:
        entries[4]='Margin Italic' if italic else 'Margin Regular'
        entries[25]='MarginItalic' if italic else 'MarginRoman'
    for nid,value in entries.items():
        f['name'].setName(value,nid,3,1,0x409)
        f['name'].setName(value,nid,1,0,0)
    f['head'].fontRevision=1.0
    f['OS/2'].usWeightClass=weight
    f['OS/2'].achVendID='MARG'
    f['OS/2'].fsSelection &= ~((1<<0)|(1<<5)|(1<<6))
    f['OS/2'].fsSelection |= ((1<<0) if italic else 0)|((1<<5) if weight==700 else 0)|((1<<6) if weight==400 and not italic else 0)
    f['head'].macStyle=((1 if weight==700 else 0)|(2 if italic else 0))
    f['post'].isFixedPitch=1

def customize(f):
    glyf=f['glyf']
    # 600 to 564 units. Transform outlines and component offsets together.
    for gn in f.getGlyphOrder():
        g=glyf[gn]
        if g.isComposite():
            for c in g.components:
                if hasattr(c,'x'): c.x=round(c.x*.94)
        elif g.numberOfContours>0:
            g.coordinates=GlyphCoordinates([(round(x*.94),y) for x,y in g.coordinates])
        if hasattr(g,'program'): g.program.fromBytecode([])
        aw,lsb=f['hmtx'][gn]
        f['hmtx'][gn]=(round(aw*.94),round(lsb*.94))
    # A small outward kick on the lower R leg, shared by accented composites.
    r=glyf['R']
    r.coordinates=GlyphCoordinates([(round(x+10*max(0,1-y/300)) if x>325 and y<300 else x,y) for x,y in r.coordinates])
    # Chamfered dot. Colon and other composites inherit the same detail.
    dot=glyf['period'];dot.recalcBounds(glyf)
    half=(dot.xMax-dot.xMin)*.44
    cx=(dot.xMax+dot.xMin)/2;cy=(dot.yMax+dot.yMin)/2
    chamfer=half*.22
    pts=[(cx-half+chamfer,cy-half),(cx+half-chamfer,cy-half),(cx+half,cy-half+chamfer),(cx+half,cy+half-chamfer),(cx+half-chamfer,cy+half),(cx-half+chamfer,cy+half),(cx-half,cy+half-chamfer),(cx-half,cy-half+chamfer)]
    pen=TTGlyphPen(None);pen.moveTo(tuple(round(v) for v in pts[0]))
    for p in pts[1:]: pen.lineTo(tuple(round(v) for v in p))
    pen.closePath();glyf['period']=pen.glyph()
    for gn in f.getGlyphOrder():
        g=glyf[gn];g.recalcBounds(glyf)
        aw,_=f['hmtx'][gn]
        f['hmtx'][gn]=(aw,g.xMin if hasattr(g,'xMin') else 0)
    f['OS/2'].xAvgCharWidth=564
    for tag in ['DSIG','prep','fpgm','cvt ','STAT']:
        if tag in f: del f[tag]

def main():
    (ROOT/'fonts/static').mkdir(parents=True,exist_ok=True)
    (ROOT/'fonts/variable').mkdir(parents=True,exist_ok=True)
    for italic in (False,True):
        src=ROOT/'source/upstream'/('SourceCodePro-Italic.ttf' if italic else 'SourceCodePro-Regular.ttf')
        original=TTFont(src)
        doc=DesignSpaceDocument();axis=AxisDescriptor()
        axis.name='Weight';axis.tag='wght';axis.minimum=200;axis.default=400;axis.maximum=900;doc.addAxis(axis)
        for weight,label in WEIGHTS.items():
            f=instantiateVariableFont(original,{'wght':weight},inplace=False)
            customize(f);names(f,weight,italic)
            suffix=label+('Italic' if italic else '')
            if italic and weight==400:suffix='Italic'
            path=ROOT/'fonts/static'/('Margin-'+suffix+'.ttf');f.save(path)
            sd=SourceDescriptor();sd.path=str(path);sd.name=suffix;sd.familyName='Margin';sd.styleName=suffix;sd.location={'Weight':weight}
            if weight==400:sd.copyInfo=True;sd.copyLib=True;sd.copyFeatures=True
            doc.addSource(sd)
            instance=InstanceDescriptor();instance.name=suffix;instance.familyName='Margin';instance.styleName=label+(' Italic' if italic else '');instance.location={'Weight':weight}
            doc.addInstance(instance)
        vf,_,_=build(doc)
        names(vf,400,italic,True)
        for inst in vf['fvar'].instances:
            w=int(inst.coordinates['wght']);label=WEIGHTS[w]+(' Italic' if italic else '')
            if italic and w==400:label='Italic'
            inst.subfamilyNameID=vf['name'].addName(label)
            inst.postscriptNameID=vf['name'].addName('Margin-'+label.replace(' ',''))
        buildStatTable(vf,[{'tag':'wght','name':'Weight','values':[{'value':w,'name':n,'flags':2 if w==400 else 0} for w,n in WEIGHTS.items()]},{'tag':'ital','name':'Italic','values':[{'value':1 if italic else 0,'name':'Italic' if italic else 'Roman','flags':0 if italic else 2}]}])
        basename='Margin-Italic' if italic else 'Margin-Roman'
        vf.save(ROOT/'fonts/variable'/(basename+'.ttf'))
        vf.flavor='woff2';vf.save(ROOT/'web'/(basename+'.woff2'))
    print('Built 16 static TTFs, 2 variable TTFs, and 2 variable WOFF2 files.')

if __name__=='__main__':main()
