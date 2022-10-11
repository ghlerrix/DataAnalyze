import argparse
from DataAnalyze import DataAnalyze

def parse_args():
    parser = argparse.ArgumentParser(description='dataset analyze')
    parser.add_argument('type', type=str, help="Dataset format, optional 'voc' and 'coco'")
    parser.add_argument('path', type=str, help='Dataset path, if it is a voc dataset, it corresponds '
                                               'to the xml directory, if it is a coco dataset, it is the json file '
                                               'path')
    parser.add_argument('--out', type=str, default='out', help='Result output directory')
    return parser.parse_args()


def main():
    args = parse_args()
    DataAnalyze(args.type, args.path, args.out)


if __name__ == '__main__':
    main()
