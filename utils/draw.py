import os
import matplotlib.pyplot as plt



class Draw:
    def __init__(self, outPath):
        self.outPath = os.path.join(outPath, 'img')

    def drawImageWHScatter(self, imagesWH):
        self.drawScatter(imagesWH[0],
            imagesWH[1],
            "Scatter of image W & H",
            'W', 'H',
            'imageWH.png')

    def drawBboxWHScatter(self, bboxsWH):
        self.drawScatter(bboxsWH[0],
            bboxsWH[1],
            "Scatter of bbox W & H",
            'W', 'H',
            'bboxWH.png')

    def drawAnchorRatioBar(self, anchorRatios):
        r_dict = {item: anchorRatios.count(item) for item in set(anchorRatios)}

        self.drawBar(r_dict.keys(), r_dict.values(),
                'AnchorBoxRatioBar', 'ratio', 'num', 'AnchorBoxRatio.png')

    def drawEachCategoryNum(self, eachCategoriesNum):

        self.drawBar(eachCategoriesNum.keys(), eachCategoriesNum.values(),
            'the numbers of category', 'category', 'num', 'EachCategoryNum.png')
        self.drawPie(eachCategoriesNum.values(), eachCategoriesNum.keys(), 'the numbers of category', 'EachCategoryNumPie.png')

    def drawEachCategoryImagesNum(self, eachCategoryImageNum):
        self.drawBar(eachCategoryImageNum.keys(), eachCategoryImageNum.values(),
            'the numbers of images for each category', 'category', 'num', 'EachCategoryImagesNum.png')

    def drawEachImageBboxNum(self, eachImageBboxNum_list):
        c_dict = {item: eachImageBboxNum_list.count(item) for item in set(eachImageBboxNum_list)}

        self.drawBar(c_dict.keys(), c_dict.values(),
            'the numbers of bboxes included in each image',
            'numbers of bboxes in each image', 'num', 'EachImageBboxNum.png')

    def drawSizeBboxNum(self, sizeBboxNum):
        self.drawBar(sizeBboxNum.keys(), sizeBboxNum.values(),
            'Number of bbox in different sizes', 'size', 'num', 'SizeBboxNum.png')

    def drawEachCategoryBboxWH(self, eachCategoriesBbox):
        if not os.path.exists(os.path.join(self.outPath, 'EachCategoryBboxWH')):
            os.makedirs(os.path.join(self.outPath, 'EachCategoryBboxWH'))
        for c in eachCategoriesBbox:
            self.drawScatter(eachCategoriesBbox[c][0], eachCategoriesBbox[c][1], f'{c}WH', 'w', 'h', os.path.join('EachCategoryBboxWH', f'{c}WH.png'))


    def drawScatter(self, x, y, title, xlabel, ylabel, imgName):
        """
        draw a scatter
        :param x: x
        :param y: y
        :param title: title of image
        :param xlabel: x label of image
        :param ylabel: y label of image
        :param imgName: name of image
        :return:
        """
        plt.scatter(x, y)
        self._extracted_from_drawBar_4(title, xlabel, ylabel, imgName)

    def drawBar(self, x, y, title, xlabel, ylabel, imgName):
        """
        draw a bar
        :param x: x
        :param y: y
        :param title: title of image
        :param xlabel: x label of image
        :param ylabel: y label of image
        :param imgName: name of image
        :return:
        """
        rects = plt.bar(x, y)
        for rect in rects:  # rects 是柱子的集合
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), ha='center', va='bottom')
        self._extracted_from_drawBar_4(title, xlabel, ylabel, imgName)

    # TODO Rename this here and in `drawScatter` and `drawBar`
    def _extracted_from_drawBar_4(self, title, xlabel, ylabel, imgName):
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.savefig(os.path.join(self.outPath, imgName))
        plt.close()

    def drawPie(self, size, labels, title, imgName):
        """
        draw a pie
        :param size: size
        :param labels: labels of image
        :param title: title of image
        :param imgName: name of image
        :return:
        """
        plt.pie(size, labels=labels, labeldistance=1.1,
                autopct="%1.1f%%", shadow=False, startangle=90, pctdistance=0.6)
        plt.title(title)
        plt.axis("equal")  # 设置横轴和纵轴大小相等，这样饼才是圆的
        plt.savefig(os.path.join(self.outPath, imgName))
        plt.close()