# Adobe Ghost 1.0 - engineer-186f

import os
import sys
import platform

import xml.etree.ElementTree as ET

import json

from random import randint
from time import sleep

# -------------------------------------------------------------------------

PROGRAM_DATA = None

NEW_LINE_CHAR = '\n'

DEF_PROGRAM = "Photoshop"
CONFIG_PATH = "config.json"
FILE_NAME   = "application.xml"
SYS_PATH    = "/Library/Application Support/"
APP_PATH    = "Adobe/Adobe Photoshop CC 2018/AMT/"

DEF_PATH = SYS_PATH + APP_PATH

ASCII_ART = [
    "+-------------------------------------------------\  ",
    "|                                                  \ ",
    "|                                                   |",
    "|                  Adobe Ghost 1.0                  |",
    "|              for macOS/OSX >= 10.10               |",
    "|                                                   |",
    "|          Adobe CC Program Trial Extender          |",
    "|                                                   |",
    "|          http://github.com/engineer-186f          |",
    "|                                                   |",
    "|                      (0.o)                        |",
    " \                                                  |",
    "  \-------------------------------------------------+"
]

# -------------------------------------------------------------------------

def print_art(text_list = [], file = None, new_line = False):
    final_list = []

    if file != None:
        if check_file(file):
            with open(file) as file_instance:
                for line in file_instance:
                    final_list.append(line)
        else:
            final_list.append("ASCII art file not found.")

    if len(text_list) > 0:
        final_list = text_list
    else:
        final_list.append("No existing arguments.")

    for line in final_list: print line

    if new_line == True: print ""

# -------------------------------------------------------------------------

def quit_program():
    print "[+] Quitting program... \n"

    exit(1)

# -------------------------------------------------------------------------

def get_program_path(data, key_value):
    for element in data["programs"]:
        if key_value.lower() in element["label"].lower():
            return element["path"]

    return None

# -------------------------------------------------------------------------

def check_get_os():
    if platform.system() == "Darwin":
        return "Mac OS X / macOS {}".format(platform.mac_ver()[0])
    
    return platform.os()

# -------------------------------------------------------------------------

def check_file(file_name):
    if os.path.isfile(file_name): 
        return True

    return False

# -------------------------------------------------------------------------

def get_xml_data(file_name):
    if check_file(file_name):
        return ET.parse(file_name)

    return None

# -------------------------------------------------------------------------

def get_json_data(file_name):
    if check_file(file_name):
        with open(file_name) as data:
            return json.load(data)

    return None

# -------------------------------------------------------------------------

def generate_key(length = 24):
    value = ""

    for x in xrange(0, length):
        value += str(randint(0, 9))

    return value

# -------------------------------------------------------------------------

def get_modified_key(key, length = 24, removal_length = 5):
    value = key

    value = value[:-removal_length]

    for x in xrange(0, removal_length):
        value += str(randint(0, 9))

    return value

# -------------------------------------------------------------------------

def modify(file_path, file_name, program_name):
    xml_file = file_path + file_name

    if check_file(xml_file):
        print "[+] {} path: {}".format(program_name, xml_file)
    else:
        print "[-] Application path not found."

        quit_program()

    dom = get_xml_data(xml_file)

    root = dom.getroot()

    if root != None:
        print "[+] XML file root fetched!"
    else:
        print "[-] Invalid XML file..."

        quit_program()

    initial_node = None

    for child in root:
        if child.tag == "Other":
            initial_node = child

            break

    for sub_child in initial_node:
        if sub_child.attrib["key"] == "TrialSerialNumber":
            print "[+] Serial number: {}".format(sub_child.text)
            print "[+] Creating a new key..."

            new_key = get_modified_key(sub_child.text)

            if new_key > 0:
                print "[+] Generated key: {}".format(new_key)
                print "[+] Assigning new key..."

                old_key = sub_child.text

                sub_child.text = new_key

                if sub_child.text == new_key:
                    print "[+] New key replaced! {} -> {}".format(
                        old_key, new_key
                    )
                else:
                    print "[-] Could not assign new key."

                    quit_program()
            else:
                print "[-] Could not generate key."

                quit_program()

    print "[+] Writing new changes to {}, wait...".format(file_name)

    dom.write(xml_file)
    
    print "[+] Success! Have a good day..."

# -------------------------------------------------------------------------

def main(argv):
    os.system("clear")

    (head, tail) = os.path.split(__file__)

    dir_path = head

    # os.chdir(dir_path)

    config = get_json_data(CONFIG_PATH)

    print_art(ASCII_ART, None, True)

    if os.getuid() != 0:
        print "[-] Not running as root."
        print "[+] Program must run as root!"

        quit_program()

    system_os = check_get_os()

    if "macOS" in system_os:
        print "[+] OS: {}".format(system_os)
    else:
        print "[-] Unsupported OS!"

        quit_program()

    file_path = DEF_PATH
    file_name = FILE_NAME

    program_name = argv[1] if len(argv) > 1 else DEF_PROGRAM

    file_path = get_program_path(config, program_name)

    if file_path == None: 
        file_path = DEF_PATH

        program_name = DEF_PROGRAM

    print "[+] Selected program: {}".format(program_name)

    modify(file_path, file_name, program_name)

    quit_program()

# -------------------------------------------------------------------------

if __name__ == "__main__": main(sys.argv)
