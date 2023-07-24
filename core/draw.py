import plotly.express as px
import pandas as pd
import os
import time
import cv2
import matplotlib.pyplot as plt


class Draw:
    def __init__(self, out) -> None:
        self.out = out

    def drawBar(self, data, x, y, text, title, dtick=None):
        startTime = time.time()
        fig = px.bar(
            data,
            x=x,
            y=y,
            text=text)
        fig.update_layout(
            title={'text': title, 'x': 0.5})
        if dtick is not None:
            fig.update_xaxes(dtick=dtick)
        fig.write_image(
            os.path.join(self.out, f'{title}.png'))
        pd.DataFrame(data).to_excel(
            os.path.join(self.out, f'{title}.xlsx'), index=False)
        endTime = time.time()
        print(f"The bar of '{title}' has beed done! "
              f"({round(endTime - startTime, 3)}s)")

    def drawPie(self, data, names, values, title):
        startTime = time.time()
        fig = px.pie(
            data, values=values, names=names)
        self.saveFigAndXlsx(fig, title, data)
        endTime = time.time()
        print(f"The pie of '{title}' has beed done!"
              f"({round(endTime - startTime, 3)}s)")

    def drawScatter(self, data, title, xlabel, ylabel):
        startTime = time.time()
        fig = px.scatter(
            x=data['X'],
            y=data['Y'],
            title=title,
            labels={'x': xlabel, 'y': ylabel})
        self.saveFigAndXlsx(fig, title, data)
        endTime = time.time()
        print(f"The scatter of '{title}' has beed done!"
              f"({round(endTime - startTime, 3)}s)")

    def saveFigAndXlsx(self, fig, title, data):
        fig.update_layout(title={'text': title, 'x': 0.5})
        fig.write_image(os.path.join(
            self.out, f'{title}.png'))
        pd.DataFrame(data).to_excel(
            os.path.join(self.out, f'{title}.xlsx'), index=False)

    @staticmethod
    def cv_img_rgb(path):
        img = plt.imread(path)
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def drawBboxs(self, imgPath, bboxs, out, color=(0, 255, 255),
                  thickness=1, textColor=(0, 255, 255), textThickness=1):
        file_name = os.path.split(imgPath)[-1]
        try:
            img = self.cv_img_rgb(imgPath)
        except Exception:
            directory = os.path.dirname(imgPath)
            imgList = os.listdir(directory)
            for i in imgList:
                imgName = os.path.splitext(i)[0]
                if imgName == file_name:
                    file_name = i
                    img = self.cv_img_rgb(os.path.join(directory, i))
                    break
        for bbox in bboxs:
            text_org = (int(bbox[0][0]), int(bbox[0][1]) - 5)
            cv2.putText(img, bbox[1], text_org,
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, textColor, textThickness)
            img = cv2.rectangle(img, (int(bbox[0][0]), int(bbox[0][1])),
                                (int(bbox[0][0] + bbox[0][2]),
                                 int(bbox[0][1] + bbox[0][3])),
                                color=color,
                                thickness=thickness)
        cv2.imwrite(os.path.join(out, file_name), img)
