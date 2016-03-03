#!/usr/bin/env python

import sys, json, os


os.system("/usr/bin/curl -k http://ganglia.lcg.cscs.ch/ganglia/files_cms.html > files_cms.html")
fi = open("files_cms.html")

ndict = {}

def insert_to_dict(path, size, imtime, iatime):
    toks = path.split("/")
    cdict = ndict
    for tok in toks:
        if not cdict.has_key(tok):
            cdict[tok] = {}
        cdict = cdict[tok]
    cdict["__size__"] = size
    cdict["__imtime__"] = imtime
    cdict["__iatime__"] = iatime

for line in fi.readlines():
    ldata = map(lambda x: x.strip(), line.split("|"))
    if len(ldata) != 6:
        continue
    try:
        float(ldata[0])
    except:
        continue
    size = round(float(ldata[0])/1024/1024,2)
    path = ldata[-1]
    iatime = ldata[3]
    imtime = ldata[4]
    if not "/pnfs/lcg.cscs.ch/cms/trivcat/store/" in path:
        continue
    path = path.replace("/pnfs/lcg.cscs.ch/cms/trivcat/store/", "/")
    if len(path) == 1:
        continue
    if len(path.split("/")) > 6:
        continue
    insert_to_dict(path, size, imtime, iatime)

def recurse(d, name, depth=0):
    thisret = {}
    children = []
    for k, v in d.items():
        if k == "__size__":
            thisret["size"] = v
        elif k == "__imtime__":
            thisret["imtime"] = v
        elif k == "__iatime__":
            thisret["iatime"] = v
        else:
            children += [recurse(v, k, depth+1)]
    thisret["name"] = name
    if len(children)>0:
        thisret["children"] = children
    return thisret

ret = recurse(ndict, "root")
of = open("t2.json", "w") 
of.write(json.dumps(ret["children"][0], indent=2))
of.close()
