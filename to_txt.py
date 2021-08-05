import os
import sys
import xml.etree.ElementTree as ET


def to_txt():
    txt_dir = './txt/'
    for file in os.listdir(txt_dir):
        txt_file = open(os.path.join(txt_dir, file.replace(".vtt", ".txt")), 'w')
        if file.endswith(".vtt"):
            with open(os.path.join("./txt/", file)) as f:
                for line in f:
                    if not line.startswith('0'):
                        if not line.startswith('WEBVTT'):
                            if not line.startswith('Kind:'):
                                if not line.startswith('Language:'):
                                    if not line.startswith('\n'):
                                        if not line.startswith('[BLANK_AUDIO]'):
                                            txt_file.write("%s" % line)


def xml_to_txt(file, target_file):
    temp_xml = ET.parse(file)
    root = temp_xml.getroot()
    f= open(target_file, "w+")
    for item in root:
        f.write(f'{item.text}\n')
