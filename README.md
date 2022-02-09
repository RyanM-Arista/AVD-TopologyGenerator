# AVD-TopologyGenerator
Generate Topology Diagrams using data generated from AVD

Inputs CSV files from
- documentation/fabric/*-p2p-link.csv
- documentation/fabric/*-topology-link.csv

# Note to self
Run script to output in dot file format
./genTopo.py > SOURCE-p2p.dot

# Usage
- PNG Output - dot -Tpng SOURCE-p2p.dot > SOURCE-p2p.png
- SVG Output - dot -Tsvg SOURCE-p2p.dot > SOURCE-p2p.svg

# Documentation
GraphViz
https://graphviz.org/documentation/
https://graphviz.org/pdf/dot.1.pdf
# Version
DRAFT script not ready for production
# Compatibility
Latest AVD Devel or AVD v3.3.0