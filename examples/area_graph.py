#!/usr/bin/env python

# This is just little test of using PyDot and Graphviz (both are required)
# to graph a modules areas, might be possible to do something fun with it.
# This probably won't run without some modifications...

from pynwn.module import Module
import pprint
import pydot

if __name__ == '__main__':
    mod = Module('test.mod')

    links = {}
    tags  = {}
    
    for area in mod.areas:
        links[area.resref] = []
        for trig in area.triggers:
            tags[trig.tag] = (area.resref, trig.position)
            if len(trig.linked_to):
                links[area.resref].append(trig.linked_to)

        for door in area.doors:
            tags[door.tag] = (area.resref, door.position)
            if len(door.linked_to):
                links[area.resref].append(door.linked_to)

        for way in area.waypoints:
            tags[way.tag] = (area.resref, way.position)
            if len(way.linked_to):
                links[area.resref].append(way.linked_to)

    graph = pydot.Dot(graph_type='digraph')

    # There is probably a better way...
    graph.set_graphviz_executables({'dot': 'C:\\Program Files (x86)\\Graphviz2.30\\bin\\dot.exe',
                                    'twopi': 'C:\\Program Files (x86)\\Graphviz2.30\\bin\\twopi.exe',
                                    'neato': 'C:\\Program Files (x86)\\Graphviz2.30\\bin\\neato.exe',
                                    'circo': 'C:\\Program Files (x86)\\Graphviz2.30\\bin\\circo\\dot.exe -Kcirco',
                                    'fdp': 'C:\\Program Files (x86)\\Graphviz2.30\\bin\\fdp.exe'})

    # Create edges
    nodes = []
    edges = set()
    for area in mod.areas:
        nodes.append(pydot.Node(area.resref))
        for tag in links[area.resref]:
            if tag in tags:
                edges.add((area.resref, tags[tag][0]))

    edges = [pydot.Edge(a1, a2) for a1, a2 in edges]

    for node in nodes:
        graph.add_node(node)

    for edge in edges:
        graph.add_edge(edge)

    graph.write_png('test_area_graph.png')
