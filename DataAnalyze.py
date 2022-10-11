import os
from utils.read import *
from utils.data import *
from utils.draw import *
from utils.excel import *

class DataAnalyze:
    """
    voc or coco dataset analyze
    """
    def __init__(self, type, path, outPath):
        """
        :param type: dataset format, optional: 'coco', 'voc'
        :param path: dataset path
        :param outPath: result path
        """
        self.outPath = outPath

        if not os.path.exists(self.outPath):
            os.makedirs(self.outPath)

        print('Processing, please wait...')

        if type == 'coco':
            self.analyzeInfo(readCoco(path))
            self.output()
        elif type == 'voc':
            self.analyzeInfo(readVoc(path))
            self.output()
        else:
            print('Currently only voc and coco formats are supported, please check if the first parameter is correct.')
        
        print(f'Processing completed. The result is saved in {self.outPath}.')

    def calEachCategorieNum(self, categorie):
        if categorie not in self.eachCategoriesNum.keys():
            self.eachCategoriesNum.update({categorie: 1})
        else:
            self.eachCategoriesNum[categorie] += 1


    def calEachCategorieBbox(self, categorie, bboxWH):
        if categorie not in self.eachCategoriesBbox.keys():
            self.eachCategoriesBbox.update({categorie: [[bboxWH[0]], [bboxWH[1]]]})
        else:
            self.eachCategoriesBbox[categorie][0].append(bboxWH[0])
            self.eachCategoriesBbox[categorie][1].append(bboxWH[1])


    def analyzeInfo(self, info_data):
        self.imagesWH = [[], []]
        self.bboxsWH = [[], []]
        self.anchorRatios = []
        self.eachCategoriesNum = {}
        self.eachCategoriesBbox = {}
        self.eachCategoryImageNum = {}
        self.eachImageCategoryNum = {}
        self.eachImageBboxNum_list = []
        self.sizeBboxNum = dict.fromkeys(['small', 'medium', 'large'], 0)
        self.imagesNum = len(info_data)
        for info in info_data:
            w, h = getImageWH(info)
            self.imagesWH[0].append(w)
            self.imagesWH[1].append(h)
            calculatedCategory = []
            for obj in info['bndbox']:
                [bboxW, bboxH], anchorRatio, categorie, sizeType = getBboxInfo(info['file'], obj)

                self.calEachCategorieNum(categorie)
                self.bboxsWH[0].append(bboxW)
                self.bboxsWH[1].append(bboxH)
                self.calEachCategorieBbox(categorie, [bboxW, bboxH])
                if anchorRatio != -1:
                    self.anchorRatios.append(anchorRatio)
                if obj['objName'] not in self.eachCategoryImageNum.keys():
                    self.eachCategoryImageNum[obj['objName']] = 1
                    calculatedCategory.append(obj['objName'])
                elif obj['objName'] not in calculatedCategory:
                    self.eachCategoryImageNum[obj['objName']] += 1
                    calculatedCategory.append(obj['objName'])
                if sizeType == 1:
                    self.sizeBboxNum['small'] += 1
                elif sizeType == 2:
                    self.sizeBboxNum['medium'] += 1
                elif sizeType == 3:
                    self.sizeBboxNum['large'] += 1
            if len(calculatedCategory) in self.eachImageCategoryNum:
                self.eachImageCategoryNum[len(calculatedCategory)] += 1
            else:
                self.eachImageCategoryNum[len(calculatedCategory)] = 1
            self.eachImageBboxNum_list.append(len(info['bndbox']))
        self.bboxNum = len(self.anchorRatios)

    def output(self):
        print('\n***************** Info *****************\n')
        print('number of images: %d' % self.imagesNum)
        print('number of boxes: %d' % len(self.anchorRatios))
        className_list = set(self.eachCategoriesNum.keys())
        print('classes = ', list(className_list))
        print('\n***************** Info *****************\n')

        print('Exporting images, please wait...')
        draw = Draw(self.outPath)
        draw.drawEachCategoryBboxWH(self.eachCategoriesBbox)
        draw.drawImageWHScatter(self.imagesWH)
        draw.drawBboxWHScatter(self.bboxsWH)
        draw.drawSizeBboxNum(self.sizeBboxNum)
        draw.drawAnchorRatioBar(self.anchorRatios)
        draw.drawEachCategoryImagesNum(self.eachCategoryImageNum)
        draw.drawEachCategoryNum(self.eachCategoriesNum)
        draw.drawEachImageBboxNum(self.eachImageBboxNum_list)
        print('Export images completed.')

        print('Exporting Excel table, please wait...')
        excel = Excel(self.outPath)
        excel.imageWH(self.imagesWH)
        excel.bboxWH(self.bboxsWH)
        excel.anchorRatio(self.anchorRatios)
        excel.eachCategory(self.eachCategoriesNum)
        excel.eachCategoryImagesNum(self.eachCategoryImageNum)
        excel.eachImageBboxNum(self.eachImageBboxNum_list)
        excel.sizeBboxNum(self.sizeBboxNum)
        excel.eachCategoryBboxWH(self.eachCategoriesBbox)
        print('Export Excel table completed.')


