import argparse
import contextlib
import os
from core import Parse, Draw
import shutil
from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser(description='dataset visualize')
    parser.add_argument(
        'type', type=str, help="Dataset format, optional 'voc' and 'coco'")
    parser.add_argument('imgsPath', type=str, help="Images path")
    parser.add_argument('labelsPath', type=str,
                        help='Labels path, if it is a voc dataset, '
                        'it corresponds to the xml directory, '
                        'if it is a coco dataset, '
                        'it is the json file path')
    parser.add_argument('--out', type=str,
                        default='visualizeOut', help='Result output directory')
    parser.add_argument('--color', type=list, default=(0, 255, 0),
                        help="bbox color")
    parser.add_argument('--thickness', type=int, default=1,
                        help="bbox thickness")
    parser.add_argument('--textColor', type=list, default=(0, 255, 0),
                        help="label color")
    parser.add_argument('--textThickness', type=int, default=1,
                        help="label thickness")
    return parser.parse_args()


def main():
    args = parse_args()

    with contextlib.suppress(Exception):
        shutil.rmtree(args.out)
    os.mkdir(args.out)

    parse = Parse(args.type, args.labelsPath)
    draw = Draw(args.out)

    for ann in tqdm(parse.img2anns, desc="drawing...", leave=True):
        imgName = parse.getImgNameById(ann)
        bboxs = []
        for bboxId in parse.img2anns[ann]:
            bbox = parse.getBboxById(bboxId)
            bboxs.append(bbox)

        draw.drawBboxs(os.path.join(args.imgsPath, imgName), bboxs, args.out,
                       args.color, args.thickness,
                       args.textColor, args.textThickness)


if __name__ == '__main__':
    main()
