import paho.mqtt.client as mqtt
import json
import argparse
import traceback
import lirc
import sys

parser = argparse.ArgumentParser(description='mqtt2lirc')
parser.add_argument("hostname", help="broker hostname")
parser.add_argument('--port', dest="port", type=int, default=1883, help='broker port (default: %(default)s)')
parser.add_argument('--username', '-u', dest='username', help='broker username')
parser.add_argument('--password', '-p', dest='password', help='broker password')
parser.add_argument('--topic', '-t', dest='topic', default='lirc/tx', help='broker topic to subscribe to (default: %(default)s)')
args = parser.parse_args()

mqtt_client = mqtt.Client(client_id="lirc")
lirc_client = lirc.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected (Code 0)")
        client.subscribe(args.topic)
        return
    elif rc == 1:
        raise Exception("Connection refused (Code 1) – incorrect protocol version")
    elif rc == 2:
        raise Exception("Connection refused (Code 2) – invalid client identifier")
    elif rc == 3:
        raise Exception("Connection refused (Code 3) – server unavailable")
    elif rc == 4:
        raise Exception("Connection refused (Code 4) – bad username or password")
    elif rc == 5:
        raise Exception("Connection refused (Code 5) – not authorised")
    raise Exception(f"Connection refused (Code {rc}) – unknown error code")

def on_message(client, userdata, message):
    try:
        print("message received " ,str(message.payload.decode("utf-8")))
        payload = json.loads(message.payload)
        remote = payload["remote"]
        key = payload["key"]
        repeat_count = payload.get("repeat_count", 1)
        print("sending key", remote, key, f"repeat_count={repeat_count}")
        lirc_client.send_once(remote, key, repeat_count=repeat_count)
    except lirc.exceptions.LircdCommandFailureError as error:
        print('Unable to send key', file=sys.stderr)
        print(error)
    except Exception:
        traceback.print_exc()

mqtt_client.on_message = on_message
mqtt_client.on_connect = on_connect

if args.username or args.password:
    mqtt_client.username_pw_set(username=args.username, password=args.password)

mqtt_client.connect(args.hostname, port=args.port, keepalive=60, bind_address="")

try:
    mqtt_client.loop_forever()
except KeyboardInterrupt:
    pass
finally:
    lirc_client.close()
