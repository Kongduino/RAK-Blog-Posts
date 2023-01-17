import secrets, sys

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
f.write("var points = [];\n")
for i in range(888):
  x = secrets.randbelow(1000)
  x /= -100000
  y = secrets.randbelow(int(1e3))
  if secrets.randbelow(2) == 1:
    y *= -1
  y /= 100000
  x = cx + x
  y = cy + y
  z = secrets.randbelow(60)
  f.write(f'points.push([{x},{y},{z}]);\n')
px = 22.459059
py = 114.002805
f.write(f'var px = {cx};')
f.write(f'var py = {cy};')

f.close()
