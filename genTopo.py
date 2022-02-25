#!/usr/bin/env python3
#DRAFT script not ready for prod.
#works on latest AVD devel or AVD v3.3.0
#Works from root folder of AVD project
#Todo
#   - host handling (adjust ranking)
#   - work on importing both csv files
#   - integrate output handling
#   - UI prompts for outuput filetypes or folder location
#   - Graphviz doens't handle single dashes in hostnames, change to underscore or something else

import csv
import argparse
import os, fnmatch

options = argparse.ArgumentParser(description = 'Create Topology from generated CSV file')
#options.add_argument('--name',action='store_const', const=diagramName, default='Data Center Topology', help='Name of topology')
args=options.parse_args()
print(args)

def find(pattern, path):
  result = []
  for root, dirs, files in os.walk(path):
    for name in files:
      if fnmatch.fnmatch(name, pattern):
          result.append(os.path.join(root, name))
  return result



def buildTopo(name,file):
  if not os.path.exists('./documentation/diagrams/'):
    os.makedirs('./documentation/diagrams/')
  sourceFilename = file
  topotype = ('./documentation/diagrams/' + name + ".dot")
  #print(outputFilename[0])

  #prep for ouput files
  f = open(topotype,"w")
  input_file = csv.DictReader(open(sourceFilename[0]))
  #Dot file header
  f.write("graph G { rankdir=LR  \n{ \nnode [margin=0 ratio=auto fontcolor=blue fontsize=32 width=0.5 shape=square style=filled ]\n}\n")

  allnodes  =set()
  spinerank =set()
  spinerank2 = []
  leafrank  =set()
  for item in input_file:
      nodeName = item.get('Node')
      peerNodeName = item.get('Peer Node')
      headlabel = item.get('Node Interface')
      taillabel = item.get('Peer Interface')
      #print ( nodeName + " -- "+ peerNodeName +" [taillabel=\"" + taillabel + "\" headlabel=\"" + headlabel +"\"]"  ) #For interface labeling
      f.write("\""+nodeName+"\"" + " -- "+ "\""+peerNodeName+"\"" + "\n")
      if item.get('Peer Type') == "spine":
        spinerank.add(peerNodeName)
      elif item.get('Type') == "l3leaf":
        leafrank.add(nodeName)
      allnodes.add(nodeName)
  f.write("\n")
  f.write("subgraph { \n")
  f.write("{ rank=min;\n")
  for item in spinerank:
    f.write("\""+item+"\""+"\n")
  f.write("};\n")
  f.write("{ rank=max;\n")
  for item in leafrank:
    f.write("\""+item+"\""+"\n")
  f.write("};\n")
  z=allnodes.difference(leafrank)
  f.write("{ rank=same;\n")
  for item in z.difference(spinerank):
    f.write("\""+item+"\""+"\n")
  f.write("};\n")
  f.write("}\n")
  f.write("\n}")
  f.close()


def buildDiagram(name,file,exportType):
  sourceType=name
  sourceFilename = file
  outputType = exportType
  if not os.path.exists('./documentation/diagrams/'):
    os.makedirs('./documentation/diagrams/')
  #topotype = ('./documentation/diagrams/' + name + ".dot")
  #using common output types, reference https://graphviz.org/docs/outputs/
  if outputType == 'png':
    #dot -Tpng *-p2p.dot > *-p2p.png
    os.system('dot -Tpng '+ sourceFilename[0] + ' > ' + './documentation/diagrams/' + sourceType +'.png' )
  elif outputType == 'svg':
    os.system('dot -Tsvg '+ sourceFilename[0] + ' > ' + './documentation/diagrams/' + sourceType +'.svg' )
  elif outputType == 'bmp':
    os.system('dot -Tbmp '+ sourceFilename[0] + ' > ' + './documentation/diagrams/' + sourceType +'.bmp' )
  elif outputType == 'gif':
    os.system('dot -Tgif '+ sourceFilename[0] + ' > ' + './documentation/diagrams/' + sourceType +'.gif' )
  elif outputType == 'jpg':
    os.system('dot -Tjpg '+ sourceFilename[0] + ' > ' + './documentation/diagrams/' + sourceType +'.jpg' )
  elif outputType == 'json':
    os.system('dot -Tjson '+ sourceFilename[0] + ' > ' + './documentation/diagrams/' + sourceType +'.json' )
  elif outputType == 'pdf':
    os.system('dot -Tpdf '+ sourceFilename[0] + ' > ' + './documentation/diagrams/' + sourceType +'.pdf' )
  elif outputType == 'webp':
    os.system('dot -Twebp '+ sourceFilename[0] + ' > ' + './documentation/diagrams/' + sourceType +'.webp' )
  else:
    print('Output source not defined, please choose output type')

p2p = find('*-p2p-links.csv', './documentation/fabric/')
topofile = find('*-topology.csv', './documentation/fabric/')
print("Building Peer To Peer Topology source file")
buildTopo('PeerToPeer',p2p)
print("Building Fabric Topology source file")
buildTopo('FabricTopology',topofile)

p2pdiag = find('PeerToPeer.dot', './documentation/diagrams/')
buildDiagram('PeerToPeer',p2pdiag,'png')
fabricdiag = find('FabricTopology.dot', './documentation/diagrams/')
buildDiagram('FabricTopology',fabricdiag,'png')