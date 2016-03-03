import sys, json, os

fi = open("files_cms.html")
ic = 0

os.system("curl -k http://ganglia.lcg.cscs.ch/ganglia/files_cms.html > files_cms.html")

# data = [{
#             y: 56.33,
#             color: colors[0],
#             drilldown: {
#                 name: 'MSIE versions',
#                 categories: ['MSIE 6.0', 'MSIE 7.0', 'MSIE 8.0', 'MSIE 9.0', 'MSIE 10.0', 'MSIE 11.0'],
#                 data: [1.06, 0.5, 17.2, 8.11, 5.33, 24.13],
#                 color: colors[0]
#             }
#         }, {

ndict = {}

def insert_to_dict(path, size, time):
    toks = path.split("/")
    cdict = ndict
    for tok in toks:
        if not cdict.has_key(tok):
            cdict[tok] = {}
        cdict = cdict[tok]
    cdict["__size__"] = size
    cdict["__time__"] = time

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
    time = ldata[4]
    if not "/pnfs/lcg.cscs.ch/cms/trivcat/store/" in path:
        continue
    path = path.replace("/pnfs/lcg.cscs.ch/cms/trivcat/store/", "/")
    if len(path) == 1:
        continue
    if len(path.split("/")) > 4:
        continue
    insert_to_dict(path, size, time)
    ic += 1

def recurse(d, name, depth=0):
    thisret = {}
    children = []
    for k, v in d.items():
        if k == "__size__":
            thisret["size"] = v
        elif k == "__time__":
            thisret["time"] = v
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
