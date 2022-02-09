#!/usr/bin/env python3
#DRAFT script not ready for prod.
#works on latest AVD devel or AVD v3.3.0
#Todo
#   - host handling (adjust ranking)
#   - work on importing both csv files
#   - integrate output handling
#   - UI prompts for filetypes or folder location

import csv

diagramName = "Data Center Topology"
outputFilename = "Data Center Topology"
fileType = "png" #png|jpg|svg|pdf

input_file = csv.DictReader(open('./documentation/fabric/*-p2p-link.csv')) #p2p links file
#input_file = csv.DictReader(open('./documentation/fabric/*-topology.csv')) #topology file

allnodes  =set()
spinerank =set()
spinerank2 = []
leafrank  =set()

#    print (item.get(' Node')) #extra space
print ("graph G { \n{ \nnode [margin=0 fontcolor=blue fontsize=32 width=0.5 shape=square style=filled ]\n}")

for item in input_file:
    nodeName = item.get('Node')
    peerNodeName = item.get('Peer Node')
    headlabel = item.get('Node Interface')
    taillabel = item.get('Peer Interface')
    #print ( nodeName + " -- "+ peerNodeName +" [taillabel=\"" + taillabel + "\" headlabel=\"" + headlabel +"\"]"  ) #To generate Link labelling
    print ( nodeName + " -- "+ peerNodeName )
    if item.get('Peer Type') == "spine":
      spinerank.add(peerNodeName)
    elif item.get('Type') == "l3leaf":
      leafrank.add(nodeName)
    allnodes.add(nodeName)
print ("\n")
print ("subgraph { \n")
print ("{ rank=same;")
for item in spinerank:
    print (item)
print("};")
print ("{ rank=same;")
for item in leafrank:
    print (item)
print("};")
z=allnodes.difference(leafrank)
print ("{ rank=same;")
for item in z.difference(spinerank):
    print (item)
print("};")
print ("}")
print ("\n}")