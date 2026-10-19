# Map Scale Math

Map and model scale arithmetic. On a 1:24000 map, 2.5 cm is 600 m of real ground.

## What it computes

- **The real truth** - a length measured on the map, as ground distance in m, km and mi.
- **The map truth** - a ground distance, as a length on the map in mm, cm and in.
- **The scale truth** - the scale between a map length and the ground distance it stands for, marked "exactly" or "about"; a ground distance shorter than the map length is reported as an enlargement.

Map lengths are in mm, cm or in; ground distances in m, km, ft or mi. Lengths can have up to 3 decimals, from 0.001 to 1000000. Scales are whole numbers from 1 to 100000000. Arithmetic is exact in nanometres with big integers, using exact unit sizes (1 in = 25.4 mm, 1 ft = 0.3048 m, 1 mi = 1609.344 m). Figures are rounded to 2 decimal places, half up.

## Boundary

Arithmetic only. It assumes the map is drawn true to its stated scale. Map Scale Math does not know distortion, paper stretch or what a map actually shows. Check those where they apply.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic.
- `oracle.py` - the Python mirror that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (45 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/mapscale/
Repo: https://github.com/iLanis-agent/mapscale
