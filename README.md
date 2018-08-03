# image-optimization-pipeline
Aplicación de múltiples técnicas y transformación en imágenes para su optimización.

## App
- Address: [http://www.loencontre.co:3000/](http://www.loencontre.co:3000/)

## API
- Address: [http://www.loencontre.co:8000/](http://www.loencontre.co:8000/)

## API endpoints

| Endpoint | Parameters | Method | Response | Description |
| --- | --- | --- | --- | --- |
| / |  | GET |  | Api root |
| /upload |  | POST | <ul><li>success</li><li>id</li></ul> | Upload new image |
| /processing/<image> |  | GET | <ul><li>success</li><li>original</li><li>transformations</li></ul> | Get trasnformations of image by id |
| /pipelines/<image> | <ul><li>list_transformations</li></ul> | POST | <ul><li>success</li><li>original</li><li>pipelines</li></ul> | Get pipelines of image by id |
| /pipeline/<image> | <ul><li>steps</li></ul> | POST | <ul><li>success</li><li>original</li><li>pipeline</li></ul> | Get specific pipeline of image by id |
| /ocr/<image> | <ul><li>text</li></ul> | POST | <ul><li>success</li><li>results</li></ul> | Get ocr of all pipelines of image by id |
| /steps/<pipeline>/ | | GET | <ul><li>success</li><li>steps</li></ul> | Get steps of pipeline by id |
| /ocr-individual/<pipeline> | | GET | <ul><li>success</li><li>results</li></ul> | Get text of pipeline by id |
