#!/usr/bin/env python

# project file replacement tool
#  written by Yosuke Matsusaka
#
#  distributed under same license as rtmros_choreonoid

# sample configuration file (yaml structure under each robot and
# sensor items are the same as the official cnoid file)
#
#robot:
#  - 
#    name: "MIDJAXON"
#    plugin: Body
#    class: BodyItem
#    data: 
#      modelFile: "../../jvrc_models/JAXON_JVRC/MIDJAXON.wrl"
#    children: 
#      - 
#        name: "BodyRTC"
#        plugin: OpenRTM
#        class: BodyRTCItem
#        data: 
#          isImmediateMode: true
#          moduleName: "PDcontroller"
#          confFileName: "MIDJAXON.PD.conf"
#sensors:
#  - 
#    name: "GLVisionSimulator"
#    plugin: Body
#    class: GLVisionSimulatorItem
#    data: 
#      enabled: true
#      targetBodies: [ MIDJAXON ]
#      targetSensors: [ HEAD_CAMERA ]

import sys
import os
import yaml
import glob


def traverse(item):
    global numitems
    item['id'] = numitems
    numitems = numitems + 1
    children = item.get('children')
    if children:
        for c in children:
            traverse(c)


if len(sys.argv) != 2:
    print 'Usage: %s config.yml' % sys.argv[0]
    exit()

# this has to be CLoader because of the original JVRC project file
conf = yaml.load(file(sys.argv[1], 'r'), Loader=yaml.CLoader)

for f in glob.glob('jaxon*.cnoid'):
    d = yaml.load(file(f, 'r'), Loader=yaml.CLoader)
    items = d['items']['children'][0]['children']
    nitems = [conf['robot'][0]]
    for i in items:
        if i['name'] == 'JAXON_JVRC':
            continue
        if i['class'] == 'AISTSimulatorItem':
            newc = []
            for c in i['children']:
                if c['class'] != 'GLVisionSimulatorItem':
                    newc.append(c)
            newc.extend(conf['sensors'])
            i['children'] = newc
        nitems.append(i)
    d['items']['children'][0]['children'] = nitems
    numitems = 0
    traverse(d['items'])
    for v in d['views']:
        if v['class'] == 'ItemTreeView':
            v['state']['checked'] = range(0, numitems)
    of = file(f.replace('jaxon', conf['robot'][0]['name'].lower()), 'w')
    of.write(yaml.dump(d))
