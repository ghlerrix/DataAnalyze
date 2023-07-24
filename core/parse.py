import json
from collections import defaultdict
import time
from .converter import Converter


class Parse():
    def __init__(self, type, path) -> None:
        if type == 'coco':
            self.dataset = json.load(open(path))
        elif type == 'voc':
            self.dataset = Converter.voc2coco(path)
        else:
            assert 'Currently only voc and coco formats are supported'

        print('Parsing dataset, please wait...')
        startTime = time.time()

        self.cats = self.dataset['categories']
        self.imgs = self.dataset['images']
        self.anns = self.dataset['annotations']

        self.img2anns, self.cat2imgs, self.cat2anns = \
            defaultdict(list), defaultdict(list), defaultdict(list)
        self.size2anns = defaultdict(list)
        self.allWH = defaultdict(list)
        self.allAnnsWH = defaultdict(list)
        self.cat2annsWH = defaultdict(list)

        for ann in self.anns:
            self.img2anns[ann['image_id']].append(ann['id'])
            if ann['image_id'] not in self.cat2imgs[ann['category_id']]:
                self.cat2imgs[ann['category_id']].append(ann['image_id'])
            self.cat2anns[ann['category_id']].append(ann['id'])
            if ann['area'] <= 32 * 32:
                self.size2anns['small'].append(ann['id'])
            elif 32 * 32 < ann['area'] < 96 * 96:
                self.size2anns['medium'].append(ann['id'])
            else:
                self.size2anns['large'].append(ann['id'])
            self.allAnnsWH[ann['id']] = (
                ann['bbox'][2], ann['bbox'][3])
            self.cat2annsWH[ann['category_id']].append(
                (ann['bbox'][2], ann['bbox'][3]))

        self.eachImg2anns = defaultdict(int)
        for value in self.img2anns.values():
            self.eachImg2anns[len(value)] += 1

        for img in self.imgs:
            self.allWH[img['id']] = (img['width'], img['height'])

        self.eachAnn2ratio = defaultdict(int)
        for ann in self.anns:
            self.eachAnn2ratio[
                round(ann['bbox'][2] / ann['bbox'][3], 1)] += 1

        endTime = time.time()
        spendTime = round(endTime - startTime, 3)
        print(f'Parsing done. ({spendTime}s)')

    def getImgNameById(self, id):
        return next(
            (img['file_name'] for img in self.imgs if id == img['id']), None)

    def getBboxById(self, id):
        return next(
            ((ann['bbox'], self.getCategoryById(ann['category_id'])) 
             for ann in self.anns if id == ann['id']), None)

    def getCategoryById(self, id):
        return next(
            (cat['name'] for cat in self.cats if id == cat['id']), None)
