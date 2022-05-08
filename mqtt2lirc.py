import paho.mqtt.client as mqtt
import json
import argparse
import traceback

parser = argparse.ArgumentParser(description='mqtt2lirc')
parser.add_argument("hostname", help="broker hostname")
parser.add_argument('--port', dest="port", type=int, default=1883, help='broker port')
parser.add_argument('--username', '-u', dest='username', help='broker username')
parser.add_argument('--password', '-p', dest='password', help='broker password')
parser.add_argument('--topic', '-t', dest='topic', default='lirc/tx', help='broker topic to subscribe to')
args = parser.parse_args()

client = mqtt.Client(client_id="lirc")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(args.topic)

def on_message(client, userdata, message):
    try:
        print("message received " ,str(message.payload.decode("utf-8")))
        payload = json.loads(message.payload)
        remote = payload["remote"]
        keys = payload["keys"]
        print(remote, keys)
    except Exception:
        traceback.print_exc()

client.on_message = on_message
client.on_connect = on_connect

if args.username or args.password:
    client.username_pw_set(username=args.username, password=args.password)

client.connect(args.hostname, port=args.port, keepalive=60, bind_address="")

try:
    client.loop_forever()
except KeyboardInterrupt:
    pass
