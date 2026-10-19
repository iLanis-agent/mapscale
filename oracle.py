#!/usr/bin/env python3
# Map Scale Math oracle - mirrors engine.js.
import json, math, re

MAP_NM = {"mm": 1000000, "cm": 10000000, "in": 25400000}
REAL_NM = {"m": 1000000000, "km": 1000000000000, "ft": 304800000, "mi": 1609344000000}

def _scale(d):
    if isinstance(d, bool) or not isinstance(d, (int, float)) or not math.isfinite(d) or math.floor(d) != d or d < 1 or d > 100000000:
        raise ValueError("scale must be a whole number from 1 to 100000000")
    return int(d)

def _len(text, label):
    t = text.strip() if isinstance(text, str) else ""
    m = re.fullmatch(r"([0-9]+)(?:\.([0-9]{1,3}))?", t)
    err = f"{label} must be a positive number with at most 3 decimals, up to 1000000"
    if not m:
        raise ValueError(err)
    v = int(m.group(1)) * 1000 + int((m.group(2) or "").ljust(3, "0"))
    if v < 1 or v > 1000000000:
        raise ValueError(err)
    return t, v

def _unit(table, u, label):
    if u not in table:
        raise ValueError(f"{label} unit must be one of {', '.join(table.keys())}")
    return table[u]

def _f2(num, den):
    s = (2 * num * 100 + den) // (2 * den)
    if s == 0:
        return "under 0.01"
    whole, frac = divmod(s, 100)
    f = f"{frac:02d}".rstrip("0")
    return str(whole) + ("." + f if f else "")

def real_truth(scale, length, unit):
    d = _scale(scale); t, v = _len(length, "map length"); f = _unit(MAP_NM, unit, "map length")
    nm = v * f // 1000 * d
    return (f"{t} {unit} on a 1:{scale} map is {_f2(nm, REAL_NM['m'])} m on the ground, which is "
            f"{_f2(nm, REAL_NM['km'])} km or {_f2(nm, REAL_NM['mi'])} mi (each figure rounded to 2 decimal places).")

def map_truth(scale, distance, unit):
    d = _scale(scale); t, v = _len(distance, "ground distance"); f = _unit(REAL_NM, unit, "ground distance")
    real = v * f // 1000
    nm = (2 * real + d) // (2 * d)
    return (f"{t} {unit} on the ground is {_f2(nm, MAP_NM['mm'])} mm on a 1:{scale} map, which is "
            f"{_f2(nm, MAP_NM['cm'])} cm or {_f2(nm, MAP_NM['in'])} in (each figure rounded to 2 decimal places).")

def scale_truth(map_length, map_unit, distance, real_unit):
    ta, va = _len(map_length, "map length"); fa = _unit(MAP_NM, map_unit, "map length")
    tb, vb = _len(distance, "ground distance"); fb = _unit(REAL_NM, real_unit, "ground distance")
    map_nm = va * fa // 1000; real_nm = vb * fb // 1000
    head = f"{ta} {map_unit} on the map for {tb} {real_unit} on the ground is "
    if real_nm >= map_nm:
        d = (2 * real_nm + map_nm) // (2 * map_nm)
        return head + f"a scale of {'exactly' if real_nm % map_nm == 0 else 'about'} 1:{d}."
    n = (2 * map_nm + real_nm) // (2 * real_nm)
    return head + f"an enlargement of {'exactly' if map_nm % real_nm == 0 else 'about'} {n}:1."

FNS = {"realTruth": real_truth, "mapTruth": map_truth, "scaleTruth": scale_truth}
CASES = [
    ("realTruth", [24000, "2.5", "cm"]), ("realTruth", [24000, "1", "in"]), ("realTruth", [50000, "10", "mm"]), ("realTruth", [1, "1", "mm"]),
    ("realTruth", [100000000, "1000000", "in"]), ("realTruth", [250000, "0.001", "mm"]), ("realTruth", [63360, "1", "in"]), ("realTruth", [25000, " 4 ", "cm"]),
    ("realTruth", [24000, "2.5", "ft"]), ("realTruth", [24000, "0", "cm"]), ("realTruth", [24000, "2.5555", "cm"]), ("realTruth", [24000, "-2", "cm"]),
    ("realTruth", [24000, "1e3", "cm"]), ("realTruth", [0, "2", "cm"]), ("realTruth", [100000001, "2", "cm"]), ("realTruth", [24000.5, "2", "cm"]), ("realTruth", [24000, "1000001", "cm"]),
    ("mapTruth", [24000, "600", "m"]), ("mapTruth", [24000, "1", "mi"]), ("mapTruth", [50000, "5", "km"]), ("mapTruth", [1, "1", "m"]),
    ("mapTruth", [100000000, "1", "m"]), ("mapTruth", [24000, "100", "ft"]), ("mapTruth", [250000, "0.001", "m"]), ("mapTruth", [24000, "0.001", "km"]),
    ("mapTruth", [63360, "1", "mi"]), ("mapTruth", [24000, "1000000", "mi"]),
    ("mapTruth", [24000, "600", "cm"]), ("mapTruth", [24000, "0", "m"]), ("mapTruth", [0, "5", "m"]), ("mapTruth", [24000, "abc", "m"]),
    ("scaleTruth", ["2.5", "cm", "600", "m"]), ("scaleTruth", ["1", "in", "1", "mi"]), ("scaleTruth", ["1", "in", "1", "km"]), ("scaleTruth", ["1", "mm", "1", "m"]),
    ("scaleTruth", ["3", "cm", "1", "m"]), ("scaleTruth", ["10", "cm", "1", "ft"]), ("scaleTruth", ["1", "cm", "1", "cm"]) ,
    ("scaleTruth", ["2", "cm", "1", "ft"]), ("scaleTruth", ["1", "mm", "0.001", "m"]), ("scaleTruth", ["1000000", "in", "0.001", "ft"]),
    ("scaleTruth", ["0", "cm", "1", "m"]), ("scaleTruth", ["1", "cm", "0", "m"]), ("scaleTruth", ["1", "yd", "1", "m"]), ("scaleTruth", ["1", "cm", "1", "yd"]),
]

out = []
for fn, args in CASES:
    try:
        exp = FNS[fn](*args)
    except ValueError as e:
        exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(len(out), "cases")
