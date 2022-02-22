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
  sourceFilename = file
  topotype = (name + ".dot")
  #print(outputFilename[0])

  #prep for ouput files
  f = open(topotype,"w")
  input_file = csv.DictReader(open(sourceFilename[0]))
  #Dot file header
  f.write("graph G { \n{ \nnode [margin=0 fontcolor=blue fontsize=32 width=0.5 shape=square style=filled ]\n}\n")

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
      f.write(nodeName + " -- "+ peerNodeName + "\n")
      if item.get('Peer Type') == "spine":
        spinerank.add(peerNodeName)
      elif item.get('Type') == "l3leaf":
        leafrank.add(nodeName)
      allnodes.add(nodeName)
  f.write("\n")
  f.write("subgraph { \n")
  f.write("{ rank=same;\n")
  for item in spinerank:
    f.write(item+"\n")
  f.write("};\n")
  f.write("{ rank=same;\n")
  for item in leafrank:
    f.write(item+"\n")
  f.write("};\n")
  z=allnodes.difference(leafrank)
  f.write("{ rank=same;\n")
  for item in z.difference(spinerank):
    f.write(item+"\n")
  f.write("};\n")
  f.write("}\n")
  f.write("\n}")
  f.close()


p2p = find('*-p2p-links.csv', './documentation/fabric/')
topofile = find('*-topology.csv', './documentation/fabric/')
print("Building Peer To Peer Topology source file")
buildTopo('PeerToPeer',p2p)
print("Building Fabric Topology source file")
buildTopo('FabricTopology',topofile)