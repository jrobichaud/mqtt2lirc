# mqtt2lirc
mqtt subscriptions to send remote keys through lirc

# Usage

```python
usage: mqtt2lirc.py [-h] [--port PORT] [--username USERNAME] [--password PASSWORD] [--topic TOPIC] hostname

mqtt2lirc

positional arguments:
  hostname              broker hostname

optional arguments:
  -h, --help            show this help message and exit
  --port PORT           broker port
  --username USERNAME, -u USERNAME
                        broker username
  --password PASSWORD, -p PASSWORD
                        broker password
  --topic TOPIC, -t TOPIC
                        broker topic to subscribe to
```

# Example

```bash
python -m "mqtt2lirc" "homeassistant.local" -u "homeassistant" -p "changeme";sudo systemctl stop lircd.socket;sudo systemctl start lircd.socket
```

