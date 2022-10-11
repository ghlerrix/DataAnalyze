### Install

```bash
git clone https://github.com/Shanyaliux/DataAnalyze.git
cd DataAnalyze
pip install -r requirements.txt
```

### Usage

#### DataAnalyze
```bash
python analyze.py ${type} ${path} [--out ${out}]
```
- `type` The format of the dataset, optional 'coco' or 'voc'. 
- `path` The path of dataset.
If `type` is 'coco', the `path` is the json file path. 
If `type` is 'voc', the `path` is the path of the xml file directory.  
- `--out` is the output directory, default is './out'

##### Example
```bash
python analyze.py coco ./tarin.json --out ./out/
```

```bash
python analyze.py voc ./xml/ --out ./out/
```

#### DataVisualize
```bash
python analyze.py ${type} ${path} [--out ${out}]
```
- `type` The format of the dataset, optional 'coco' or 'voc'. 
- `imgPath` The images' path of dataset.
- `labels` The path of dataset.
If `type` is 'coco', the `path` is the json file path. 
If `type` is 'voc', the `path` is the path of the xml file directory.  
- `--out` is the output directory, default is './out'
- `--thickness` is thickness of the bbox.

##### Example
```bash
python visualize.py coco images/ ./tarin.json --out ./out/ --thickness 1
```

```bash
python visualize.py voc ./images/ ./xml/ --out ./out/ --thickness 1
```



### Screenshot
![1](./sample/boxWH.png)
![2](./sample/AnchorBoxRatio.png)
![3](./sample/EachClassNum.png)
![4](./sample/EachClassNumPie.png)


