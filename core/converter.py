import os
import xml.etree.ElementTree as ET


class Converter:
    @staticmethod
    def voc2coco(xmlpath):
        categories = []
        coco_dataset = {
            'licenses': [],
            'images': [],
            'annotations': [],
            'info': {},
            'categories': categories,
        }

        xmlList = os.listdir(xmlpath)
        for xmlname in xmlList:
            if xmlname.endswith(".xml"):
                xml_file = os.path.join(xmlpath, xmlname)
                tree = ET.parse(xml_file)
                root = tree.getroot()

                size = root.find('size')
                file_name = root.find("filename").text

                # 提取图像信息
                image_info = {
                    "id": len(coco_dataset['images']) + 1,
                    "file_name": file_name,
                    # 根据实际情况设置图像宽度和高度
                    "width": int(size.find('width').text),
                    "height": int(size.find('height').text),
                    "date_captured": "",
                    "license": None,
                    "coco_url": "",
                    "flickr_url": ""
                }
                coco_dataset['images'].append(image_info)

                for obj in root.findall('object'):
                    name = obj.find('name').text

                    if not categories:
                        category_id = len(categories) + 1
                        categories.append({'id': category_id,
                                           'name': name,
                                           'supercategory': 'object'})
                        coco_dataset['categories'] = categories

                    clist = [c['name'] for c in categories]
                    if name in clist:
                        category_id = clist
                        for c in categories:
                            if c['name'] == name:
                                category_id = c['id']
                    else:
                        category_id = len(categories) + 1
                        categories.append({'id': category_id,
                                           'name': name,
                                           'supercategory': 'object'})
                        coco_dataset['categories'] = categories

                    bnd_box = obj.find('bndbox')
                    bbox = [
                        int(bnd_box.find('xmin').text),
                        int(bnd_box.find('ymin').text),
                        int(bnd_box.find('xmax').text),
                        int(bnd_box.find('ymax').text)
                    ]
                    bbox = [
                        bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]
                    ]

                    ann_info = {
                        'id': len(coco_dataset['annotations']) + 1,
                        'image_id': len(coco_dataset['images']),
                        'category_id': category_id,
                        'bbox': bbox,
                        'area': bbox[2] * bbox[3],
                        'iscrowd': 0
                    }
                    coco_dataset['annotations'].append(ann_info)

        return coco_dataset
