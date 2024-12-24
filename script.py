"""
Adobe Ghost 2.0 - BluDay

https://github.com/BluDay

( 0 _ o )

Refactored version of the original script.
"""

from os        import getuid
from platform  import mac_ver
from random    import randint
from sys       import argv, exit
from xml.etree import ElementTree as XmlElementTree

ADOBE_PROGRAM_NAME_TO_PATH_MAP = {
    'Photoshop'         : '/Library/Application Support/Adobe/Adobe Photoshop CC 2018/AMT/',
    'Illustrator'       : '/Applications/Adobe Illustrator CC 2018/Support Files/AMT/AI/AMT/',
    'InDesign'          : '/Applications/Adobe InDesign CC 2018/Resources/AMT/ID/AMT/',
    'Lightroom Classic' : '/Library/Application Support/Adobe/Adobe Lightroom Classic CC AMT/AMT/',
    'XD'                : '/Library/Application Support/Adobe/Adobe XD CC/AMT/'
}

APPLICATION_XML_FILE = 'Application.xml'

def run():
    if getuid() != 0:
        raise Exception('[-] Script must run as root.')

    if not mac_ver():
        raise Exception('[-] Unsupported OS! Must run on Mac OSX 10.10 or above.')

    try:
        target_program_name = argv[1]

        if argv[1] == 'Lightroom':
            target_program_name += ' {}'.format(argv[2])
    except IndexError:
        target_program_name = 'Photoshop'

    if target_program_name not in ADOBE_PROGRAM_NAME_TO_PATH_MAP.keys():
        raise Exception('[-] Could not find supported Adobe program named "{}".'.format(target_program_name))

    target_program_path = ADOBE_PROGRAM_NAME_TO_PATH_MAP[target_program_name]

    xml_file = target_program_path + APPLICATION_XML_FILE

    print '[+] Selected Adobe program: {}'.format(target_program_name)
    print '[+] {} path: {}'.format(target_program_name, xml_file)

    try:
        xml_document = XmlElementTree.parse(xml_file)

        root_xml_element = xml_document.getroot()
    except:
        raise Exception('[-] Could not parse XML document.')

    print '[+] XML file root fetched!'

    target_element = None

    for element in root_xml_element:
        if element.tag != 'Other':
            continue

        for sub_element in element:
            if sub_element.attrib['key'] == 'TrialSerialNumber':
                target_element = sub_element

                break

    if not target_element:
        raise Exception('[-] Could not find an element with a `TrialSerialNumber` attribute to modify.')

    print '[+] Serial number: {}'.format(target_element.text)
    print '[*] Modifying the expired key...'

    old_key = target_element.text

    new_key = old_key[:-5] + ''.join(str(randint(0, 9)) for _ in xrange(5))

    if not new_key:
        raise Exception('[-] Could not modify the expired key.')

    print '[+] Modified key: {}'.format(new_key)

    target_element.text = new_key

    print '[*] Writing new changes to {}...'.format(xml_file)

    try:
        xml_document.write(xml_file)
    except:
        raise Exception('[-] Could not write key to the {} file for {}.'.format(
            'Application.xml',
            target_program_name
        )

    print '[+] {} -> {}'.format(old_key, new_key)
    print '[+] Complete. Have a good day.'

if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print e

        exit(1)