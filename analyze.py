import argparse
import contextlib
import os
from core import Parse, Draw
import shutil


def parse_args():
    parser = argparse.ArgumentParser(description='dataset analyze')
    parser.add_argument('type', type=str,
                        help="Dataset format, optional 'voc' and 'coco'")
    parser.add_argument('path', type=str,
                        help='Dataset path, if it is a voc dataset,  \
                            it corresponds to the xml directory, \
                            if it is a coco dataset, \
                            it is the json file path')
    parser.add_argument('--out', type=str, default='out',
                        help='Result output directory')
    return parser.parse_args()


def main():  # sourcery skip: extract-duplicate-method, move-assign-in-block
    args = parse_args()

    with contextlib.suppress(Exception):
        shutil.rmtree(args.out)
    os.mkdir(args.out)

    parse = Parse(args.type, args.path)
    print()
    print(f'number of images: {len(parse.imgs)}')
    print(f'number of annotations: {len(parse.anns)}')
    print(f'number of categories: {len(parse.cats)}')
    print('names of categories: ', [c['name'] for c in parse.cats])
    print()

    draw = Draw(args.out)

    # The number of images in each category
    data = {'Category': [c['name'] for c in parse.cats],
            'Count': [len(parse.cat2imgs[c]) for c in parse.cat2imgs]}
    title = 'The number of images in each category'
    draw.drawBar(data, 'Category', 'Count', 'Count', title)
    draw.drawPie(data, 'Category', 'Count', f'PIE {title}')

    # The number of annotations in each category
    data = {'Category': [c['name'] for c in parse.cats],
            'Count': [len(parse.cat2anns[c]) for c in parse.cat2anns]}
    title = 'The number of annotations in each category'
    draw.drawBar(data, 'Category', 'Count', 'Count', title)
    draw.drawPie(data, 'Category', 'Count', f'PIE {title}')

    data = {'AnnsNum': parse.eachImg2anns.keys(),
            'Count': parse.eachImg2anns.values()}
    title = 'The number of annotations on each image'
    draw.drawBar(data, 'AnnsNum', 'Count', 'Count', title, dtick=1)

    size = ['small', 'medium', 'large']
    data = {'Size': size,
            'Count': [len(parse.size2anns[s]) for s in size]}
    title = 'The number of annotations of different sizes'
    draw.drawBar(data, 'Size', 'Count', 'Count', title)
    draw.drawPie(data, 'Size', 'Count', f'PIE {title}')

    title = 'Scatter of images\' W & H'
    data = {'X': [parse.allWH[idx][0] for idx in parse.allWH],
            'Y': [parse.allWH[idx][1] for idx in parse.allWH]}
    draw.drawScatter(data, title=title,
                     xlabel='W', ylabel='H')

    title = 'Scatter of annotations\' W & H'
    data = {'X': [parse.allAnnsWH[idx][0] for idx in parse.allAnnsWH],
            'Y': [parse.allAnnsWH[idx][1] for idx in parse.allAnnsWH]}
    draw.drawScatter(data, title=title,
                     xlabel='W', ylabel='H')

    for c in parse.cats:
        title = f"Scatter of annotations in {c['name']} W & H"
        cid = c['id']
        data = {'X': [i[0] for i in parse.cat2annsWH[cid]],
                'Y': [i[1] for i in parse.cat2annsWH[cid]]}
        draw.drawScatter(data, title=title,
                         xlabel='W', ylabel='H')

    data = {'Ratio': parse.eachAnn2ratio.keys(),
            'Count': parse.eachAnn2ratio.values()}
    title = 'Width to height ratio bar chart of the annotations'
    draw.drawBar(data, 'Ratio', 'Count', 'Count', title, dtick=.5)


if __name__ == '__main__':
    main()
