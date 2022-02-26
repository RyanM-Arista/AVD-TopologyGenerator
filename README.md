# AVD-TopologyGenerator
Generate Topology Diagrams using data generated from AVD

Inputs are CSV files from
- documentation/fabric/*-p2p-link.csv
- documentation/fabric/*-topology-link.csv

Outputs to
- documentation/diagrams/
# Usage
- chmod +x genTopo.py
- ./genTopo.py

or

- ./genTopo.py --help

for available options

# Requirements
- python3
- graphviz (https://graphviz.org/download/)

# Documentation
GraphViz

https://graphviz.org/documentation/

https://graphviz.org/pdf/dot.1.pdf
# Status
    Workable Script, Open for Comments/Feedback

# Compatibility
    Latest AVD Devel or AVD v3.3.x
    Requires ansible-avd PR #1492