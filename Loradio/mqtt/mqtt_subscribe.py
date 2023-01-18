import paho.mqtt.subscribe as subscribe
import json, base64, struct, math
import sqlite3, sys, datetime

# create database and tables:
# CREATE TABLE gateways (id INTEGER PRIMARY KEY AUTOINCREMENT, EUI TEXT NOT NULL) WITHOUT ROWID;
# CREATE TABLE logs (id INTEGER PRIMARY KEY, gw INTEGER DEFAULT 1, TS TEXT NOT NULL, longitude REAL, latitude REAL, loraRSSI INTEGER, loraSNR INTEGER, radioRSSI INTEGER) WITHOUT ROWID;

def chk_conn(conn):
  try:
    conn.cursor()
    return True
  except Exception as ex:
    return False

con = sqlite3.connect('loradio.db')
if chk_conn(con)==False:
  print("!sqlite con is False!")
  sys.exit()
cur = con.cursor()
cur.execute('select * from gateways;')
rows = cur.fetchall()
print("Known Gateways:")
gws = {}
gwsn = {}
for x in rows:
  n,g = x
  gws[g]=n
  gwsn[n]=g
  print(f"Gateway #{n}: {g}")
cur.execute('SELECT Max(id)+1 from logs;')
rows = cur.fetchall()
nextRow = rows[0][0]
if nextRow == None:
  nextRow = 1

# Variables used to decide whether to send an update
# And calculate the center
lastLat = 0.0
lastLong = 0.0
logs = {}
minLat = 360.0
minLong = 360.0
maxLat = -360.0
maxLong = -360.0

# Calculate distance between 2 GPS coords with Haversine
def toRad(x):
  return x * 3.141592653 / 180

def haversine(lat1, lon1, lat2, lon2):
  R = 6371
  x1 = lat2-lat1
  dLat = toRad(x1)
  x2 = lon2-lon1
  dLon = toRad(x2)
  a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(toRad(lat1)) * math.cos(toRad(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
  d = R * c
  return round((d + 2.220446049250313e-16) * 100) / 100

# MQTT callback
def on_message(client, userdata, message):
  global lastLat, lastLong, nextRow, logs, minLat, minLong, maxLat, maxLong
  #print("%s\n\n%s" % (message.topic, message.payload))
  z = json.loads(message.payload)
  TS = z['received_at']
  T = TS.split('T')
  yyyymmdd = T[0]
  hhmmss = T[1].split('.')[0]
  print(f"\nReceived at {hhmmss}, on {yyyymmdd}")
  try:
    msg = z['uplink_message']
  except:
    print('No uplink message')
    return
  txt = base64.b64decode(msg['frm_payload'])
  md = msg['rx_metadata'][0]
  gw = md['gateway_ids']['gateway_id']
  try:
    rssi = md['rssi']
  except:
    print('no rssi')
    rssi = 255
  try:
    snr = md['snr']
  except:
    print('no snr')
    snr = 255
  # check whether we know this gateway
  nmr = gws.get(gw)
  if nmr == None:
    print(f"New gateway? --> {gw}")
    cur.execute('insert into gateways (eui) values ("'+gw+'");')
    cur.execute('SELECT Max(id)+1 from gateways;')
    rows = cur.fetchall()
    nmr = rows[0][0]
    gws[gw]=nmr
    gwsn[nmr]=gw
    print(f"id #{n}")

  print(f'Sent by: {gw}, RSSI: {rssi}, SNR: {snr}')
  print('Message:')
  print(txt)
  # Extract data and truncate GPS coords
  [x,y,r]=struct.unpack('f f h', txt)
  x = int(x * 1e5)
  y = int(y * 1e5)
  newLat = x / 1e5
  newLong = y / 1e5
  print(f'Latitude: {newLat}\tLongitude: {newLong}\tRSSI: {r}')
  # Either add new Lat / Long / RSSI or update average
  key = f"{newLat}:{newLong}"
  x = logs.get(key)
  if x == None:
    logs[key] = [r, 1]
    # Update minimums and maximums if needed
    # We'll calculate the map center from these
    if newLat < minLat:
      minLat = newLat
    if newLat > maxLat:
      maxLat = newLat
    if newLong < minLong:
      minLong = newLong
    if newLong < minLong:
      minLong = newLong
  else:
    x[0] += r
    x[1] += 1
    # we can calculate the averages from these
    # TODO: re-create the samples.js file

  print("Logging...")
  lastLong = newLong
  lastLat = newLat
  s = f'insert into logs (id, gw, TS, latitude, longitude, loraRSSI, loraSNR, radioRSSI) VALUES ({nextRow}, {nmr}, "{TS}", {newLat}, {newLong}, {rssi}, {snr}, {r});'
  print(s)
  cur.execute(s)
  con.commit()
  nextRow += 1

subscribe.callback(on_message, topics=['#'], qos=0, userdata=None, hostname="eu1.cloud.thethings.network", port=1883, client_id="", keepalive=60, will=None, auth={'username':"username", 'password':"NNSXS.password"}, tls=None)
