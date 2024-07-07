import customtkinter as ctk

class ResultWindow(ctk.CTkToplevel):
    def __init__(self, parent, result):
        super().__init__(parent)
        self.title("Results")
        self.geometry("380x700")

        self.resizable(False, False)

        self.frame = ctk.CTkScrollableFrame(master=self, width=380, height=700, fg_color="transparent")
        self.frame.grid(row=0, column=0, padx=5, pady=5, rowspan=4, columnspan=4, sticky="nswe")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("380x400")
        self.title("Wordament Solver")
        self.grid_anchor("center")

        self.resizable(False, False)


        # create 2x2 grid system
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.frame = ctk.CTkFrame(master=self, width=380, height=400, fg_color="transparent")
        self.frame.grid(row=0, column=0, padx=5, pady=5, rowspan=4, columnspan=4, sticky="nswe")

        self.frame.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.entry1 = ctk.CTkEntry(master=self.frame, placeholder_text="", width=55, height=45, font=("Segoe UI", 20))
        self.entry1.grid(row=0, column=0, padx=5, pady=5, sticky="nswe")
        self.entry2 = ctk.CTkEntry(master=self.frame, placeholder_text="", width=55, height=45, font=("Segoe UI", 20))
        self.entry2.grid(row=0, column=1, padx=5, pady=5, sticky="nswe")
        self.entry3 = ctk.CTkEntry(master=self.frame, placeholder_text="", width=55, height=45, font=("Segoe UI", 20))
        self.entry3.grid(row=0, column=2, padx=5, pady=5, sticky="nswe")
        self.entry4 = ctk.CTkEntry(master=self.frame, placeholder_text="", width=55, height=45, font=("Segoe UI", 20))
        self.entry4.grid(row=0, column=3, padx=5, pady=5, sticky="nswe")

        self.entry5 = ctk.CTkEntry(master=self.frame, placeholder_text="", width=55, height=45, font=("Segoe UI", 20))
        self.entry5.grid(row=1, column=0, padx=5, pady=5, sticky="nswe")
        self.entry6 = ctk.CTkEntry(master=self.frame, placeholder_text="", width=55, height=45, font=("Segoe UI", 20))
        self.entry6.grid(row=1, column=1, padx=5, pady=5, sticky="nswe")
        self.entry7 = ctk.CTkEntry(master=self.frame, placeholder_text="", width=55, height=45, font=("Segoe UI", 20))
        self.entry7.grid(row=1, column=2, padx=5, pady=5, sticky="nswe")
        self.entry8 = ctk.CTkEntry(master=self.frame, placeholder_text="", width=55, height=45, font=("Segoe UI", 20))
        self.entry8.grid(row=1, column=3, padx=5, pady=5, sticky="nswe")

        self.entry9 = ctk.CTkEntry(master=self.frame, placeholder_text="", width=55, height=45, font=("Segoe UI", 20))
        self.entry9.grid(row=2, column=0, padx=5, pady=5, sticky="nswe")
        self.entry10 = ctk.CTkEntry(master=self.frame, placeholder_text="", width=55, height=45, font=("Segoe UI", 20))
        self.entry10.grid(row=2, column=1, padx=5, pady=5, sticky="nswe")
        self.entry11 = ctk.CTkEntry(master=self.frame, placeholder_text="", width=55, height=45, font=("Segoe UI", 20))
        self.entry11.grid(row=2, column=2, padx=5, pady=5, sticky="nswe")
        self.entry12 = ctk.CTkEntry(master=self.frame, placeholder_text="", width=55, height=45, font=("Segoe UI", 20))
        self.entry12.grid(row=2, column=3, padx=5, pady=5, sticky="nswe")

        self.entry13 = ctk.CTkEntry(master=self.frame, placeholder_text="", width=55, height=45, font=("Segoe UI", 20))
        self.entry13.grid(row=3, column=0, padx=5, pady=5, sticky="nswe")
        self.entry14 = ctk.CTkEntry(master=self.frame, placeholder_text="", width=55, height=45, font=("Segoe UI", 20))
        self.entry14.grid(row=3, column=1, padx=5, pady=5, sticky="nswe")
        self.entry15 = ctk.CTkEntry(master=self.frame, placeholder_text="", width=55, height=45, font=("Segoe UI", 20))
        self.entry15.grid(row=3, column=2, padx=5, pady=5, sticky="nswe")
        self.entry16 = ctk.CTkEntry(master=self.frame, placeholder_text="", width=55, height=45, font=("Segoe UI", 20))
        self.entry16.grid(row=3, column=3, padx=5, pady=5, sticky="nswe")
        
        self.entry1.focus()

              

        self.submit_button = ctk.CTkButton(master=self.frame, text="Submit", command=self.submit)
        self.submit_button.grid(row=4, column=0, columnspan=2, padx=5, pady=9, sticky="nesw")

        self.clear_button = ctk.CTkButton(master=self.frame, text="Clear", command=self.clear)
        self.clear_button.grid(row=4, column=2, columnspan=2, padx=5, pady=9, sticky="nesw")
        
    def submit(self):
        board = [
            [self.entry1.get(), self.entry2.get(), self.entry3.get(), self.entry4.get()],
            [self.entry5.get(), self.entry6.get(), self.entry7.get(), self.entry8.get()],
            [self.entry9.get(), self.entry10.get(), self.entry11.get(), self.entry12.get()],
            [self.entry13.get(), self.entry14.get(), self.entry15.get(), self.entry16.get()]
        ]

 

    def clear(self):
        for i in range(4):
            for j in range(4):
                self.frame.grid_slaves(row=i, column=j)[0].delete(0, "end")
                self.entry1.focus()
    
if __name__ == "__main__":
    app = App()
    app.mainloop()