import cv2
import numpy as np
import pyautogui
import pytesseract
from playaudio import playaudio


tess_config = r'--psm 7 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def check_ROI(x, y, width, height, UI):
    x = int(x)
    y = int(y)
    width = int(width)
    height = int(height)
    # Set the region of the screen to capture
    screen_region = (x, y, width, height)  # Replace with actual values

    # Set the output video file name
    # output_file = "screen_capture.mp4"

    # Get the screen dimensions
    screen_width, screen_height = pyautogui.size()

    # Define the video codec and create a VideoWriter object
    # fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    # out = cv2.VideoWriter(output_file, fourcc, 20.0, (width, height))

    # Set the region of interest (ROI)
    roi = (x, y, x + width, y + height)

    def update_values(*args):

        UI.update_values()
        x = UI.values['x']
        y = UI.values['y']
        width = UI.values['width']
        height = UI.values['height']

        try:
            x = int(x)
            y = int(y)
            width = int(width)
            height = int(height)
        except:
            x = 1
            y = 1
            width = 1
            height = 1

        if x * y * width * height == 0:
            x = 1
            y = 1
            width = 1
            height = 1

        return x, y, width, height

    while getattr(UI.running_thread, "do_run", True):

        x, y, width, height = update_values()
        roi = (x, y, x + width, y + height)

        # Capture the screen frame
        screenshot = pyautogui.screenshot()

        # Convert the screenshot to OpenCV format
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Extract the region of interest (ROI)
        roi_frame = frame[roi[1]:roi[3], roi[0]:roi[2]]

        # Write the ROI frame to the output video file
        # out.write(roi_frame)

        # Display the captured frame
        cv2.imshow("Screen Capture", roi_frame)

        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1) == ord("q"):
            break

    cv2.destroyAllWindows()


def start_detection(x, y, width, height, UI, sound):
    pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'

    if sound is None:
        sound_file = "ha-gay-By-tuna.mp3"
    else:
        sound_file = sound
    x = int(x)
    y = int(y)
    width = int(width)
    height = int(height)
    roi = (x, y, x + width, y + height)
    while getattr(UI.running_thread_detect, "do_run", True):
        # Capture the screen frame
        screenshot = pyautogui.screenshot()

        # Convert the screenshot to OpenCV format
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Extract the region of interest (ROI)
        roi_frame = frame[roi[1]:roi[3], roi[0]:roi[2]]
        # Convert the image to grayscale
        gray = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)

        # Apply thresholding to convert to binary image
        ksize = (2, 2)
        blured = cv2.blur(gray, ksize)
        _, thresholded = cv2.threshold(blured, 170, 255, cv2.THRESH_BINARY_INV)
        cv2.imshow("Detekce",thresholded)
        # cv2.imshow("Detekce blur", blured)

        # Display the original and preprocessed images
        # cv2.imshow("Original Image", roi_frame)
        # cv2.imshow("Grayscale", gray)
        # cv2.imshow("Thresholded", thresholded)

        zabiti_text = UI.detection_text
        text = pytesseract.image_to_string(thresholded, lang='eng', config=tess_config)
        ocr_output_cleaned = text.replace("\n", "")
        # test = ocr_output_cleaned.lower()
        # Perform case-insensitive comparison
        if zabiti_text.lower() == ocr_output_cleaned.lower():
            # print("The words are equal (case-insensitive).")
            print("Slabkoooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
            playaudio(sound_file)
        else:
            pass
            print(ocr_output_cleaned.lower())

        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1) == ord("q"):
            break
    cv2.destroyAllWindows()


def start_test_detection(x, y, width, height, UI):
    pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'

    x = int(x)
    y = int(y)
    width = int(width)
    height = int(height)
    roi = (x, y, x + width, y + height)
    while getattr(UI.running_thread_test_detect, "do_run", True):
        # Capture the screen frame
        screenshot = pyautogui.screenshot()
        # Convert the screenshot to OpenCV format
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Extract the region of interest (ROI)
        roi_frame = frame[roi[1]:roi[3], roi[0]:roi[2]]
        # Convert the image to grayscale
        gray = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)

        # Apply thresholding to convert to binary image
        ksize = (UI.blur_value, UI.blur_value)
        blured = cv2.blur(gray, ksize)
        _, thresholded = cv2.threshold(blured, UI.threshold_value_min, UI.threshold_value_max, cv2.THRESH_BINARY_INV)

        cv2.imshow("Detekce",thresholded)
        cv2.imshow("Detekce blur", blured)

        # Display the original and preprocessed images
        # cv2.imshow("Original Image", roi_frame)
        # cv2.imshow("Grayscale", gray)
        # cv2.imshow("Thresholded", thresholded)

        zabiti_text = UI.detection_text
        zabiti_text = zabiti_text.replace("\n", "")
        zabiti_text = zabiti_text.replace(" ", "")

        text = pytesseract.image_to_string(thresholded, lang='eng', config=tess_config)
        ocr_output_cleaned = text.replace("\n", "")
        ocr_output_cleaned = ocr_output_cleaned.replace(" ", "")
        # test = ocr_output_cleaned.lower()
        # Perform case-insensitive comparison
        if zabiti_text.lower() == ocr_output_cleaned.lower():
            # print("The words are equal (case-insensitive).")
            UI.detect_text_info.configure(text="Detected", bg_color="green")
        else:
            UI.detect_text_info.configure(text="Not detected", bg_color="red")
            print(ocr_output_cleaned.lower())

        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1) == ord("q"):
            break
    cv2.destroyAllWindows()
