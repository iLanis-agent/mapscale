// Map Scale Math engine - map length to ground distance, ground distance to map length, and the scale between them.
// Mirrored by oracle.py; keep the op order identical.
// Lengths are typed with up to 3 decimals, from 0.001 to 1000000. Scales are whole numbers from 1 to 100000000.
// Arithmetic is exact in nanometres (big integers) with these exact unit sizes:
// 1 in = 25.4 mm, 1 ft = 0.3048 m, 1 mi = 1609.344 m. Figures are rounded to 2 decimals, half up.

var MAP_NM = { mm: 1000000n, cm: 10000000n, "in": 25400000n };
var REAL_NM = { m: 1000000000n, km: 1000000000000n, ft: 304800000n, mi: 1609344000000n };

function _scale(d) {
  if (typeof d !== "number" || !isFinite(d) || Math.floor(d) !== d || d < 1 || d > 100000000) {
    throw new Error("scale must be a whole number from 1 to 100000000");
  }
  return BigInt(d);
}

// A typed length as thousandths of its unit.
function _len(text, label) {
  var t = typeof text === "string" ? text.trim() : "";
  var m = /^([0-9]+)(?:\.([0-9]{1,3}))?$/.exec(t);
  if (!m) throw new Error(label + " must be a positive number with at most 3 decimals, up to 1000000");
  var v = BigInt(m[1]) * 1000n + BigInt((m[2] || "") + "000".slice((m[2] || "").length));
  if (v < 1n || v > 1000000000n) throw new Error(label + " must be a positive number with at most 3 decimals, up to 1000000");
  return { text: t, thousandths: v };
}

function _unit(table, u, label) {
  if (!Object.prototype.hasOwnProperty.call(table, u)) throw new Error(label + " unit must be one of " + Object.keys(table).join(", "));
  return table[u];
}

// num/den rounded to 2 decimals, half up, trailing zeros dropped.
function _f2(num, den) {
  var s = (2n * num * 100n + den) / (2n * den);
  if (s === 0n) return "under 0.01";
  var frac = String(s % 100n);
  while (frac.length < 2) frac = "0" + frac;
  while (frac.length > 0 && frac.charAt(frac.length - 1) === "0") frac = frac.slice(0, -1);
  return (s / 100n) + (frac ? "." + frac : "");
}

// The real truth: a length measured on the map, as ground distance.
function realTruth(scale, length, unit) {
  var d = _scale(scale), l = _len(length, "map length"), f = _unit(MAP_NM, unit, "map length");
  var nm = l.thousandths * f / 1000n * d;
  return l.text + " " + unit + " on a 1:" + scale + " map is " + _f2(nm, REAL_NM.m) + " m on the ground, which is " +
    _f2(nm, REAL_NM.km) + " km or " + _f2(nm, REAL_NM.mi) + " mi (each figure rounded to 2 decimal places).";
}

// The map truth: a ground distance, as a length on the map.
function mapTruth(scale, distance, unit) {
  var d = _scale(scale), l = _len(distance, "ground distance"), f = _unit(REAL_NM, unit, "ground distance");
  var real = l.thousandths * f / 1000n;
  var nm = (2n * real + d) / (2n * d);
  return l.text + " " + unit + " on the ground is " + _f2(nm, MAP_NM.mm) + " mm on a 1:" + scale + " map, which is " +
    _f2(nm, MAP_NM.cm) + " cm or " + _f2(nm, MAP_NM["in"]) + " in (each figure rounded to 2 decimal places).";
}

// The scale truth: the scale between a map length and the ground distance it stands for.
function scaleTruth(mapLength, mapUnit, distance, realUnit) {
  var a = _len(mapLength, "map length"), fa = _unit(MAP_NM, mapUnit, "map length");
  var b = _len(distance, "ground distance"), fb = _unit(REAL_NM, realUnit, "ground distance");
  var mapNm = a.thousandths * fa / 1000n, realNm = b.thousandths * fb / 1000n;
  var head = a.text + " " + mapUnit + " on the map for " + b.text + " " + realUnit + " on the ground is ";
  if (realNm >= mapNm) {
    var d = (2n * realNm + mapNm) / (2n * mapNm);
    var exact = realNm % mapNm === 0n;
    return head + "a scale of " + (exact ? "exactly" : "about") + " 1:" + d + ".";
  }
  var n = (2n * mapNm + realNm) / (2n * realNm);
  var ex = mapNm % realNm === 0n;
  return head + "an enlargement of " + (ex ? "exactly" : "about") + " " + n + ":1.";
}
