# image-optimization-pipeline
Aplicación de múltiples técnicas y transformación en imágenes para su optimización.

## Deployment
- APP: [http://www.loencontre.co:3000](http://www.loencontre.co:3000)
- API: [http://www.loencontre.co:8000](http://www.loencontre.co:8000)

## Requirements

### phyton 3
```sh
sudo apt install python3
```

### python-pip
```sh
sudo apt install python-pip
```

### virtualenv
```sh
sudo pip install virtualenv
```

### python3-dev
```sh
sudo apt install python3-dev
```

### tesseract-ocr
```sh
sudo apt install tesseract-ocr
```

### tesseract-spa
```sh
sudo apt install tesseract-spa
```


## Run
```sh
git clone https://github.com/larry852/image-optimization-pipeline
cd image-optimization-pipeline
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt

# Run app http://localhost:3000/
python app.py
# Run api http://localhost:8000/
python api.py
```

## API endpoints

| Endpoint | Parameters | Method | Response | Description |
| --- | --- | --- | --- | --- |
| / |  | GET |  | Api root |
| /upload |  | POST | <ul><li>success</li><li>id</li></ul> | Upload new image |
| /processing/{image} |  | GET | <ul><li>success</li><li>original</li><li>transformations</li></ul> | Get trasnformations of image by id |
| /pipelines/{image} | <ul><li>list_transformations</li></ul> | POST | <ul><li>success</li><li>original</li><li>pipelines</li></ul> | Get pipelines of image by id |
| /pipeline/{image} | <ul><li>steps</li></ul> | POST | <ul><li>success</li><li>original</li><li>pipeline</li></ul> | Get specific pipeline of image by id |
| /ocr/{image} | <ul><li>text</li></ul> | POST | <ul><li>success</li><li>results</li></ul> | Get comparative ocr of all pipelines of image by id |
| /steps/{pipeline} | | GET | <ul><li>success</li><li>steps</li></ul> | Get steps of pipeline by id |
| /ocr-steps/{original}/{folder} | | GET | <ul><li>success</li><li>results</li></ul> | Get text of each step of pipeline by folder id |
| /ocr-individual/{pipeline} | | GET | <ul><li>success</li><li>results</li></ul> | Get text of pipeline by id |
