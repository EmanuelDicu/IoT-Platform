from influxdb import InfluxDBClient
from paho.mqtt.client import Client as MqttClient

import json
from datetime import datetime
import logging as log
from os import getenv
from re import match

log.basicConfig(
    level=log.ERROR,
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

if getenv('DEBUG_DATA_FLOW') == 'true':
    log.getLogger().setLevel(log.INFO)

TOPIC_STR = '^[^/]+/[^/]+$'
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'

def create_db_line(location, station, timestamp, keyval):
    key, val = keyval
    if key == 'timestamp' or type(val) not in [int, float]:
        return None

    log.info(f'{location}.{station}.{key} {val}')

    return {
        'measurement': f'{station}.{key}',
        'tags': {
            'location': location,
            'station': station
        },
        'time': timestamp,
        'fields': {
            'value': float(val)
        }
    }

def on_message(_, db: InfluxDBClient, message):
    if not message.topic or not message.payload or \
       not match(TOPIC_STR, message.topic):
        return

    log.info(f'Received message by topic [{message.topic}]')

    payload = json.loads(message.payload)

    if 'timestamp' not in payload:
        timestamp = datetime.now().strftime(TIME_FORMAT)
        log.info('Data timestamp is NOW')
    else:
        timestamp = payload['timestamp']
        log.info(f'Data timestamp is: {timestamp}')

    location, station = message.topic.split('/')
    lines = list(filter(None, map(
        lambda kv: create_db_line(location, station, timestamp, kv), payload.items())))

    if lines:
        db.write_points(lines)

def main():
    db = InfluxDBClient(host="database")
    db.create_database("iot_db")
    db.switch_database("iot_db")

    mq = MqttClient(userdata=db)
    mq.on_message = on_message
    mq.connect("mqtt")
    mq.subscribe("#")
    mq.loop_forever()

if __name__ == "__main__":
    main()
