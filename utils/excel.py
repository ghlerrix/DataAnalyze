import os
import pandas as pd

class Excel:
    def __init__(self, outPath):

        self.outPath = os.path.join(outPath, 'excel')
        if not os.path.exists(self.outPath):
            os.mkdir(self.outPath)

    def imageWH(self, imagesWH):
        self.excel2cols('W', 'H', imagesWH, 'imageWH.xlsx')

    def bboxWH(self, bboxsWH):
        self.excel2cols('W', 'H', bboxsWH, 'bboxsWH.xlsx')

    def anchorRatio(self, anchorRatios):
        r_dict = {item: anchorRatios.count(item) for item in set(anchorRatios)}
        self.excel2cols('ratio', 'num', [r_dict.keys(), r_dict.values()], 'anchorRatios.xlsx')

    def eachCategory(self, eachCategoriesNum):
        self.excel2cols('category', 'num', [eachCategoriesNum.keys(), eachCategoriesNum.values()], 'eachCategory.xlsx')

    def eachCategoryImagesNum(self, eachCategoryImageNum):
        self.excel2cols('category', 'num', [eachCategoryImageNum.keys(), eachCategoryImageNum.values()], 'eachCategoryImageNum.xlsx')

    def eachImageBboxNum(self, eachImageBboxNum_list):
        c_dict = {item: eachImageBboxNum_list.count(item) for item in set(eachImageBboxNum_list)}
        self.excel2cols('numbers of bboxes in each image', 'num', [c_dict.keys(), c_dict.values()], 'eachImageBboxNum.xlsx')

    def sizeBboxNum(self, sizeBboxNum):
        self.excel2cols('Number of bbox in different sizes', 'num', [sizeBboxNum.keys(), sizeBboxNum.values()], 'sizeBboxNum.xlsx')

    def eachCategoryBboxWH(self, eachCategoriesBbox):
        if not os.path.exists(os.path.join(self.outPath, 'EachCategoryBboxWH')):
            os.makedirs(os.path.join(self.outPath, 'EachCategoryBboxWH'))
        for c in eachCategoriesBbox:
            self.excel2cols('W', 'H', eachCategoriesBbox[c], os.path.join('EachCategoryBboxWH', f'{c}WH.xlsx'))


    def excel2cols(self, col1, col2, list, filename):
        col1 = col1
        col2 = col2
        data = pd.DataFrame({col1: list[0], col2: list[1]})
        data.to_excel(os.path.join(self.outPath, filename), sheet_name='sheet1', index=False)
