#!/usr/bin/env python3
"""Build the self-contained map: inline Leaflet 1.9.4 + Leaflet.markercluster 1.5.3
(downloaded from the npm registry) and the attraction data into map.html / index.html,
and generate attractions.csv / attractions.json. Outputs are checked against sha256."""
import hashlib, io, json, os, tarfile, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
EXPECTED = {
    "map.html": "28d7d8ec4fdb841c34ba263a67f01c33e5440ace87d1667c542f0a3326eb817d",
    "attractions.csv": "560ec2b8a1d26d6c19489f0c94acc7587dfcf9c7ef129a79193a7349ba18cf2f",
    "attractions.json": "3579d156d2ee6ac1735ddd352419fa7805867d38c6621f6b67b41037522494a3",
}

def npm_files(url, names):
    data = urllib.request.urlopen(url, timeout=60).read()
    out = {}
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
        for n in names:
            raw = tf.extractfile("package/" + n).read().decode("utf-8")
            out[n] = raw.replace("\r\n", "\n").replace("\r", "\n")
    return out

L = npm_files("https://registry.npmjs.org/leaflet/-/leaflet-1.9.4.tgz",
              ["dist/leaflet.css", "dist/leaflet.js"])
MC = npm_files("https://registry.npmjs.org/leaflet.markercluster/-/leaflet.markercluster-1.5.3.tgz",
               ["dist/MarkerCluster.css", "dist/MarkerCluster.Default.css", "dist/leaflet.markercluster.js"])

with open(os.path.join(SRC, "attractions.src.csv"), encoding="utf-8", newline="") as f:
    csv_text = f.read()
rows = [line.split(",") for line in csv_text.rstrip("\n").split("\n")]
header, body = rows[0], rows[1:]

records = []
for r in body:
    assert len(r) == len(header), r
    records.append({
        "序号": int(r[0]), "名称": r[1], "城市": r[2], "类型": r[3], "A级": r[4],
        "门票": r[5], "简介": r[6], "纬度": float(r[7]), "经度": float(r[8]),
        "坐标系": "WGS84", "坐标来源": r[9], "坐标匹配对象": r[10],
    })
data = [{"name": x["名称"], "city": x["城市"], "type": x["类型"], "rating": x["A级"],
         "ticket": x["门票"], "intro": x["简介"], "lat": x["纬度"], "lon": x["经度"]}
        for x in records]

with open(os.path.join(SRC, "map.template.html"), encoding="utf-8", newline="") as f:
    html = f.read()
for ph, val in [("@@LEAFLET_CSS@@", L["dist/leaflet.css"]),
                ("@@LEAFLET_JS@@", L["dist/leaflet.js"]),
                ("@@MC_DEFAULT_CSS@@", MC["dist/MarkerCluster.Default.css"]),
                ("@@MC_CSS@@", MC["dist/MarkerCluster.css"]),
                ("@@MC_JS@@", MC["dist/leaflet.markercluster.js"]),
                ("@@DATA@@", json.dumps(data, ensure_ascii=False))]:
    assert html.count(ph) == 1, ph
    html = html.replace(ph, val)

outputs = {
    "map.html": html.encode("utf-8"),
    "index.html": html.encode("utf-8"),
    "attractions.csv": ("\ufeff" + csv_text.replace("\n", "\r\n")).encode("utf-8"),
    "attractions.json": json.dumps(records, ensure_ascii=False, indent=1).encode("utf-8"),
}
ok = True
for name, b in outputs.items():
    h = hashlib.sha256(b).hexdigest()
    exp = EXPECTED.get(name, EXPECTED["map.html"])
    print(name, len(b), h, "OK" if h == exp else "MISMATCH (expected %s)" % exp)
    ok &= h == exp
if not ok:
    raise SystemExit("sha256 mismatch, not writing outputs")
for name, b in outputs.items():
    with open(os.path.join(ROOT, name), "wb") as f:
        f.write(b)
print("build ok")
