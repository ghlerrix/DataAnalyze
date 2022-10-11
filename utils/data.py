def calculateAnchorRatio(w, h):
        """
        calculate anchor ratio
        :param w: width
        :param h: height
        :return: AnchorRatio
        """
        r = w / h if w > h else h / w
        return round(r)

def getImageWH(info):
        w, h = info['width'], info['height']
        return [float(w), float(h)]

def getBboxInfo(file, obj):
    w = float(obj['xmax']) - float(obj['xmin'])
    h = float(obj['ymax']) - float(obj['ymin'])

    # anchorRatio
    anchorRatio = -1
    try:
        anchorRatio = calculateAnchorRatio(w, h)
    except Exception:
        print('\n============ Errors ============\n')
        print(file, 'Image has wrong height and width.')
        print('\n============ Errors ============\n')

    # categories
    categorie = obj['objName']

    area = w * h
    if area < (32 * 32):
        sizeType = 1
    elif area < (96 * 96):
        sizeType = 2
    else:
        sizeType = 3

    return [w, h], anchorRatio, categorie, sizeType