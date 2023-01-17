import secrets, math, sys

argv = sys.argv
n = len(argv)
if n != 3:
  print("Syntax: python3 demo_Heat.py centerX centerY")
  sys.exit()
try:
  cx = float(argv[1])
except:
  print(f'Invalid centerX value: {argv[1]}')
  sys.exit()
try:
  cy = float(argv[2])
except:
  print(f'Invalid centerY value: {argv[2]}')
  sys.exit()

f = open("samples.js", "w")
f.write("var points = []\n")
for i in range(2222):
  theta = secrets.randbelow(360) * math.pi / 180.0
  radiusX = secrets.randbelow(777) # m
  radiusY = secrets.randbelow(1111) # m
  dx = radiusX * math.cos(theta)
  dy = radiusY * math.sin(theta)
  lat = cx + (180/math.pi)*(dy/6378137)
  lon = cy + (180/math.pi)*(dx/6378137)/math.cos(cx)
  z = secrets.randbelow(60) * .7
  f.write(f'points.push([{lat},{lon},{z}]);\n')
f.write(f'var px = {cx};')
f.write(f'var py = {cy};')
f.close()
