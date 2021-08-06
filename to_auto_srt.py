import os
import sys
import xml.etree.ElementTree as ET
index = 0


def main(xml_path, target_srt_path):
    temp_xml = ET.parse(xml_path)
    root = temp_xml.getroot()
    global index
    index = 0
    for item in root:
        st = item.text.replace("&#39;", "'")
        with open(target_srt_path, "a+") as file:
            start = get_time(int(float(item.attrib['start']) * 1000))
            try:
                end = get_time(int(float(root[index + 1].attrib['start']) * 1000))
            except:
                end = get_time(int(float(item.attrib['start']) * 1000 + float(item.attrib['dur']) * 1000))
            file.write(f'{index+1}\n{start} --> {end}\n{st}\n\n')
        index = index + 1


def get_time(current):
    buf_sec = current // 1000
    hours = f'{buf_sec // 3600}'
    mins = f'0{(buf_sec % 3600) // 60}'
    secs = f'0{(buf_sec % 3600) % 60}'
    millisecs = f'000{current % 1000}'
    return f'{hours}:{mins[-2:]}:{secs[-2:]},{millisecs[-3:]}'
