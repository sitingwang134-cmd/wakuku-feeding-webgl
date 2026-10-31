from pathlib import Path
import re
root=Path(__file__).resolve().parent
pieces=[]
for name,ns in [('three.module.js','THREE'),('BufferGeometryUtils.js','GeometryUtils'),('GLTFLoader.js','GLTFModule'),('RoomEnvironment.js','RoomModule')]:
 s=(root/name).read_text()
 def imp(m):
  names=m[1].replace(' as ',':');dep='THREE' if 'three.module' in m[2] else 'GeometryUtils'
  return 'const {'+names+'}='+dep+';'
 s=re.sub(r'import\s*\{([^}]+)\}\s*from\s*[\'"]([^\'"]+)[\'"];',imp,s)
 def exp(m):
  fields=[]
  for x in m[1].split(','):
   bits=x.strip().split(' as ');fields.append(bits[-1]+':'+bits[0] if len(bits)>1 else bits[0])
  return 'return {'+','.join(fields)+'};'
 s=re.sub(r'export\s*\{([^}]+)\}\s*;',exp,s)
 s=re.sub(r'\bexport (?=function |class |const |let |var )','',s)
 pieces.append('const '+ns+'=(()=>{\n'+s+'\n})();')
(root/'wakuku-runtime.js').write_text('(()=>{\n'+'\n'.join(pieces)+'\nwindow.WAKUKU_RUNTIME={THREE,GLTFLoader:GLTFModule.GLTFLoader,RoomEnvironment:RoomModule.RoomEnvironment};\n})();')
