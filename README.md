# Text-detection-with-Tesseract
This is simple but i think useful demo to detect almost any kinds of text.

**NOTE**: This is really only demo from full developed program it has far away. There is some debugging features enabled so expect some kind of output in your console so don't be scared.

Features: 
* UI
* Custom threshholds
* Editing ROI(Region of interest) detection
* Editing ROI with drag and mark feature 
* Detect custom text of your choice
* Play custom sound when text is detected
* Testing detection for viewing what program can see
* Saving and loading your settings

Known issues:
* Sometimes when you edit values while detecting text it crash
* Not much pleasing UI (deal with it is is a demo) 
* Wrong reading of monitor resolutions
* Can't detect monitors on left side (only positive y,x)

How to run it ? 
**NOTE**: When you have a problem use google/bing first a lot of installation problems are resolved there.
0.(Optional) Create Venv
1. Install python
2. Install requirements.txt
3. With python run main.py `python main.py`
4. And you should see this window pop up.
![image](https://github.com/Edesak/Text-detection-with-Tesseract/assets/20689154/345aa5ce-f843-45ff-83ac-dae7fd6f3d31)

Tutorial:
If  it's not clear what each UI element means here is compant version that explains. 
* Start ROI - Starts the detection
* Edit ROI - Shows you where it detects only for you to check the area
* Test ROI - Shows you the area and what program see after threashold function. If your text is detected the red thing with be green thing. 
* X,Y,Width,Height - Can be changed with slider or by writing down the coodinates Width and Height then adds up to these coordinates
* Load sound file - Load sound file 
* Drag and mark - It creates screenshot of you monitor and then you click and drag around the area you want to be detected. After you release it should get X,Y,W,H automatically
* Thresholds Min,Max - Controling the thresholds for reading the image you can see more in Test ROI
* Save/Load config - Well save and load
* Text to detect - your custom text to detect here

Any additional Questions or issues write to issues in this git repository or write me on discord: Edesak#5182
