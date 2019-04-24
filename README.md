1. Install tesseract(v4) https://github.com/tesseract-ocr/tesseract
2. Install opencv https://docs.opencv.org/3.4.3/d7/d9f/tutorial_linux_install.html
3. Run python 3.5 virtual environment
4. Install dependencies: `$ pip install -r requirements.txt`
5. Run script: `$ python main.py --folder=path_to_folder --layout=path_to_layout`  
E.g. :   
Absolute path: `$ python main.py --folder=/home/user/handlr/to_label --layout=/home/user/handlr/P45.json`  
Relative path: `$ python main.py --folder=to_label --layout=P45.json`
6. If you want to try experimental plate recognition to text instead of 5. run:  `$ python main.py --folder=path_to_folder --layout=path_to_layout --plate_text=True`   
