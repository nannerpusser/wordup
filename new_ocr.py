import cv2 as cv
import os
import customtkinter as ctk
import CTkMessagebox as CTkMessagebox
import time
from PIL import ImageGrab
from easyocr import Reader
from pywinauto import Application

# Paths for storing screenshots and templates
assets = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
scrot_path = os.path.join(assets + os.sep + "ocr" + os.sep + "scrot.png")
template_path = os.path.join(assets + os.sep + "ocr" + os.sep + "template.png")


class GetScreenshot:
    def __init__(self):
        self.msg_font = os.path.join(assets, "Segoe-Sans-Text.ttf")
        self.msg_font_load = ctk.CTkFont(family=self.msg_font, size=22)
        self.scrot_path = scrot_path
        self.template_path = template_path
    def take_screenshot(self):
        """Capture screenshot from the Wordament window."""
        try:
            app = Application().connect(title_re=".*Ultimate Word Games.*")
            if app is None or not app.window(title_re=".*Ultimate Word Games.*").exists():
                print("Wordament window not found")
                return None

            app.window(title_re=".*Ultimate Word Games.*").set_focus()
            app.window(title_re=".*Ultimate Word Games.*").maximize()

            time.sleep(0.5)  # Allow time for maximization
            img = ImageGrab.grab().crop((0, 0, 1920, 1040))
            if img is None:
                print("Failed to capture screenshot")
                return None

            img.save(self.scrot_path)
            time.sleep(0.1)
            app.window(title_re=".*Ultimate Word Games.*").minimize()
            return self.scrot_path

        except Exception as e:
            CTkMessagebox.CTkMessagebox(
                title="Wordament window not found!",
                message=f"Open Wordament, start a game, and try again.",
                icon="error",
                font=(self.msg_font_load, 14),
                fade_in_duration=0.1,
                justify="center",
            )
            print(f"An error occurred: {e}")
            return None

    def template_matching_crop(self):
        """Perform template matching and crop the desired region."""
        if not self.scrot_path or not os.path.isfile(self.scrot_path):
            raise ValueError("Invalid screenshot path")

        img = cv.imread(self.scrot_path)
        if img is None:
            raise ValueError("Failed to read screenshot")

        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        template = cv.imread(self.template_path, 0)
        if template is None:
            raise ValueError("Failed to read template")

        res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv.minMaxLoc(res)

        top_left = max_loc
        h, w = template.shape
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cropped_region = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

        if not os.path.exists(assets + os.sep + 'ocr'):
            raise ValueError("Assets directory does not exist")
        cropped_region = cv.cvtColor(cropped_region, cv.COLOR_BGR2GRAY)
        cropped_path = os.path.join(assets + os.sep + 'ocr' + os.sep + 'cropped_region.png')
        cv.imwrite(cropped_path, cropped_region)

        return cropped_region, cropped_path


class OCR:
    def __init__(self):
        self.ocr = Reader(['en'], gpu=False)

    def run_ocr(self, cropped_region):
        """Run OCR on the cropped region and return detected text."""
        if cropped_region is None:
            raise ValueError("No cropped region provided for OCR")

        # OCR processing
        result = self.ocr.readtext(cropped_region, allowlist="ABCDEFGHIJKLMNOPQRSTUVWXYZ-/", text_threshold=0.2, adjust_contrast=0.7, detail=1, add_margin=0.2, bbox_min_score=0.2)
        for text in result:
            if text[1] == "IZ":
                result.remove(text)
            elif text[1] == "":
                result.append((text[0], "//"))

        print(f"OCR Result: {result}")

        
        extracted_data = [text[1] for text in result]

        print(f"OCR Extracted Data: {extracted_data}")
        return extracted_data

        #extracted_data = [text[1] for text in result]

        #print(f"OCR Extracted Data: {extracted_data}")
        #return extracted_data
    

class WordamentOCR:
    """A high-level class to handle the entire OCR process."""
    def __init__(self):
        self.screenshot = GetScreenshot()
        self.ocr = OCR()

    def run(self):
        # Step 1: Take the screenshot
        scrot_path = self.screenshot.take_screenshot()
        if not scrot_path:
            print("Screenshot failed.")
            return []

        # Step 2: Template match and crop
        try:
            cropped_region, _ = self.screenshot.template_matching_crop()
        except ValueError as e:
            print(f"Error during template matching: {e}")
            return []

        # Step 3: Perform OCR on the cropped region
        
        return self.ocr.run_ocr(cropped_region)

def main():
    wordament_ocr = WordamentOCR()
    ocr_results = wordament_ocr.run()

    return ocr_results
        
if __name__ == "__main__":
    main()
