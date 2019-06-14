#!/usr/bin/python3

import urllib.request
import codecs
import csv
import json


SUPPORTED_DEVICES_URL = "https://storage.googleapis.com/play_public/supported_devices.csv"
ENCODING = 'utf-16'


def build_device_map(lines):
    device_map = {}
    
    for row in csv.reader(lines):
        model = row[3]

        if not model:
            continue

        brand = row[0]
        marketing_name = row[1]
        device = row[2]
        
        full_name = brand + ' '

        if marketing_name:
            full_name += marketing_name
        elif device:
            full_name += device
        else:
            full_name += model

        device_map[model] = {
            'brand': brand,
            'marketing_name': marketing_name,
            'device': device,
            'full_name': full_name
        }

    return device_map


def main():
    response = urllib.request.urlopen(SUPPORTED_DEVICES_URL)
    lines = codecs.decode(response.read(), ENCODING).splitlines()[1:]

    device_map = build_device_map(lines)
        
    with open('devices.csv', mode='w', encoding=ENCODING) as f:
        csv_writer = csv.writer(f)
        for key in sorted(device_map):
            device = device_map[key]
            csv_writer.writerow([key, device['brand'], device['marketing_name'], device['full_name']])

    with open('devices.json', mode='w', encoding=ENCODING) as f:
        f.write(json.dumps(device_map, sort_keys=True, indent=4))

    with open('devices.json.min', mode='w', encoding=ENCODING) as f:
        f.write(json.dumps(device_map, sort_keys=True, separators=(',', ':')))


if __name__ == "__main__":
    main()
