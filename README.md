# WebOCR

This is an extension that helps you translate from you webview

# Preview
Preview this extension here [Powerpoint](https://drive.google.com/file/d/13lAtVpY0Fzc_BHOnJboP6k3N_WD3JVRX/view?usp=sharing)

## INSTALLATION
### Step 1: Clone this repository with
```
git clone https://github.com/Yamakaze-chan/WebOCR.git
```

### Step 2: Change you current to directory to WebOCR folder
```
cd WebOCR
```
### Step 3: Install requirements
### _1.With Docker_ ([Docker Installation](https://www.simplilearn.com/tutorials/docker-tutorial/how-to-install-docker-on-ubuntu))
Step 3.1.1: Build Docker Image
```
docker build -t <name_of_your_docker_image> .
```
Step 3.1.2: Run with your Docker
```
docker run -p <port>:<port> -d <name_of_your_docker_image_of_step_3.1.1> 
```
for example I want to run at <port> `5000` and <name_of_your_docker_image> is `webocr1`
```
docker run -p 5000:5000 -d webocr1
```
for more information, please read [Docker Document](https://docs.docker.com/reference/)

### _2.With Miniconda_ ([Miniconda Installation](https://docs.anaconda.com/miniconda/))
Step 3.2.1: Create an environment
```
conda create --name <your_env_name>
```
_For example_: I want to create environment name `webocr`
`conda create --name webocr`

Step 3.2.2: Activate environment
```
conda activate <your_env_name>
```
_For example_: To activate environment name `webocr`
`conda activate webocr`

Step 3.2.3: Install required libraries
```
pip install -r requirements.txt
```

### *In case you want your model weight is locally*
Step 4: Create `model` folder
```
mkdir model
```
Step 5: Download EasyOCR Japanese model weight from [Jaded AI](https://www.jaided.ai/easyocr/modelhub/) and put in `model` folder

Step 6: Download MangaOCR model weight from [Huggingface](https://huggingface.co/kha-white/manga-ocr-base/tree/main) and put in `model` folder

Step 7: Uncomment line 90 & 91, comment line 92 & 93 of file `ocr.py`

## ADD EXTENSION TO YOUR BROWSER
Step 1: Access `Manage Extensions` from your browser setting

Step 2: Enable `Developer mode`

Step 3: Click the `Load Unpacked` button which will allow us to load our project

Step 4: Choose folder `extension` from current directory (folder contains `manifest.json` file)
