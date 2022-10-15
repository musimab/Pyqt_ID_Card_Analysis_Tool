
# Identity Card Anaylysis Tool

In this study, a gui was designed with the pyqt framework, this gui contains many networks to extract the information on the id card. The id card image is first detected by image processing techniques, then it is sent to the character density map and the unet model is run on the character outputs and the relevant parts are extracted.
### Arguments
* `--folder_name`: folder path
* `--neighbor_box_distance`: Nearest box distance 
* `--face_recognition`: Face recognition method (dlib, ssd, haar)
* `--rotation_interval`: Id card rotation interval in degrees
* `--ocr_method`: ocr method (EasyOcr and TesseractOcr)


### Gui Features

![Screenshot from 2022-10-12 21-22-15](https://user-images.githubusercontent.com/47300390/195426938-1604d78b-e48f-445e-8043-fea852bf8417.png)

### Face Detectors
![Screenshot from 2022-10-12 21-22-37](https://user-images.githubusercontent.com/47300390/195426988-23bb228f-b8c5-4f8f-9ec7-a91e2e71d7f3.png)

### Id Card Analysis Tool video

https://user-images.githubusercontent.com/47300390/195427535-be214282-8b6a-46c8-8a6a-99802ceb0195.mp4
