import customtkinter as ctk
import os
from PIL import Image
from tkinter import ttk
import threading
from CTkMessagebox import CTkMessagebox

ctk.set_appearance_mode("dark")
width = 500
height = 650
assets = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

class TopWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry(CenterWindowToDisplay(self, 300, 400, self._get_window_scaling()))
        self.resizable(False, False)
        self.minsize(200, 400)
        self.title("Help")
      
        
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        global bg_image

        self.entryfont = (os.path.join(assets + "Segoe-Sans-Text.ttf"), 26)
        bg_image = os.path.join(assets + os.sep + "colorkit.png")
      

        self.title("Wordament Solver")
        self.geometry(CenterWindowToDisplay(self, width, height, 1.0))
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
            

        self.image = ctk.CTkImage(Image.open(bg_image), size=(width, height))

        self.bg_image = ctk.CTkLabel(self, text="", image=self.image)
        self.bg_image.grid(row=0, column=0, columnspan=2, rowspan=2, sticky="nsew")

        self.create_widgets()
    def create_widgets(self):
        # Board input frame
        self.board_frame = ctk.CTkFrame(self, bg_color="transparent", corner_radius=4)
        self.board_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        # Configure grid of the board_frame
        for i in range(4):
            self.board_frame.grid_columnconfigure(i, weight=1)
            self.board_frame.grid_rowconfigure(i, weight=1)

        # Create a StringVar for each entry
        self.entry_vars = [[ctk.StringVar() for _ in range(4)] for _ in range(4)]

        self.board_entries = []
        for i in range(4):
            row_entries = []
            for j in range(4):
                entry = ctk.CTkEntry(
                    self.board_frame,
                    bg_color="transparent",
                    font=self.entryfont,
                    justify="center",
                    textvariable=self.entry_vars[i][j],
                )
                entry.grid(row=i, column=j, padx=4, pady=4, sticky="nsew", columnspan=1)
                row_entries.append(entry)
                # Add trace to StringVar
                self.entry_vars[i][j].trace_add(
                    "write", lambda *_, r=i, c=j: self.validate_entry(r, c)
                )
            self.board_entries.append(row_entries)

def CenterWindowToDisplay(
    Screen: ctk.CTk, width: int, height: int, scale_factor: float = 1.0
):
    """Centers the window to the main display/monitor"""
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    x = int(((screen_width / 2) - (width / 2)) * scale_factor)
    y = int(((screen_height / 2) - (height / 2)) * scale_factor)
    return f"{width}x{height}+{x}+{y}"
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
