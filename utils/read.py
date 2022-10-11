from cmath import inf
import glob
import json
import os
import xml.etree.ElementTree as ET


def readXml(xml, ignoreDiff=False):
    """
    read single xml file
    :param xml: path of xml file
    :param ignoreDiff: whether to ignore difficult. defalut: False
    :return: xmlInfo, format: {'file': '', 'filename': '', 'width': '', 'height': '', 'bndbox': []}
    """
    root = ET.parse(xml).getroot()
    filename = root.find('filename').text
    size = root.find('size')
    width = size.find('width').text
    height = size.find('height').text
    xmlInfo = {'file': xml, 'filename': filename, 'width': width, 'height': height, 'bndbox': []}

    for obj in root.findall('object'):
        if ignoreDiff and obj.find('difficult') is not None:
            difficult = obj.find('difficult').text
            if int(difficult) == 1:
                continue
        objName = obj.find('name').text
        bndbox = obj.find('bndbox')
        xmin = bndbox.find('xmin').text
        ymin = bndbox.find('ymin').text
        xmax = bndbox.find('xmax').text
        ymax = bndbox.find('ymax').text
        
        tempBox = {'objName': objName, 'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax}
        xmlInfo['bndbox'].append(tempBox)
    return xmlInfo

def readVoc(xmlPath):
    """
    read multiple xml file
    :param xmlPath: path of xml file directory
    :return: list of xmlInfo
    """
    vocInfo = []
    xmlList = glob.glob(xmlPath + os.sep + '*.xml')
    xmlList.sort()
    for xml in xmlList:
        xmlFile = xml
        vocInfo.append(readXml(xmlFile))
    return vocInfo

def readCoco(jsonFile):
    """
    read coco json file
    :param jsonFile: path of json file
    :return: list of cocoInfo
    """
    with open(jsonFile) as f:
        jsonData = json.load(f)
        categories_dict = {categories['id']: categories['name'] for categories in jsonData['categories']}

        info_dict = {}
        for image in jsonData['images']:
            cocoInfo = {'file': image['file_name'], 'filename': image['file_name'], 
                'width': image['width'], 'height': image['height'], 'bndbox': []}
            info_dict[image['id']] = cocoInfo
        for annotation in jsonData['annotations']:
            xmin = annotation['bbox'][0]
            ymin = annotation['bbox'][1]
            xmax = str(float(xmin) + (float(annotation['bbox'][2])))
            ymax = str(float(ymin) + (float(annotation['bbox'][3])))
            tempBox = {'objName': categories_dict[annotation['category_id']], 
                'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax}

            info_dict[annotation['image_id']]['bndbox'].append(tempBox)
        return list(info_dict.values())