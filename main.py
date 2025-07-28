from CTkToolTip import CTkToolTip
from iniParser import iniParser
from version import __version__
from tkinter import filedialog
from datetime import datetime
from customtkinter import *
from PIL import Image
import os, shutil


class SkinMerger(CTk):
    def __init__(self):
        super().__init__()
        set_appearance_mode("dark")
        self.geometry("900x400")
        self.title(f"osu!mania Skin Merger v{__version__} by Greenest-Guy")
        self.resizable(False, False)
        self.FM = SkinMergerLogic(self)

        dir_path = os.path.dirname(os.path.abspath(__file__))

        icon_path = os.path.join(dir_path, "merge_logo.ico")
        self.iconbitmap(icon_path)

        # Background Image
        background_image = CTkImage(light_image=Image.open(os.path.join(dir_path, "BG.png")), 
                                    dark_image=Image.open(os.path.join(dir_path, "BG.png")), 
                                    size=(900, 400))
        
        CTkLabel(self, image=background_image, text="").place(x=0, y=0)

        # BUTTON Base Skin
        base_skin_button = CTkButton(self, width=150, height=25, bg_color="#090909", text="Base Skin", command=self.FM.selectBaseSkin,
                                    fg_color="#ffffff", hover_color="#b1b1b1", text_color="#000000", font=("", 16))
        
        base_skin_button.place(x=135-base_skin_button.cget("width")/2, y=65)

        CTkToolTip(base_skin_button, message="The merge skin will be added to this skin")

        # BUTTON Merge Skin
        merge_skin_button = CTkButton(self, width=150, height=25, bg_color="#090909", text="Merging Skin", command=self.FM.selectMergeSkin,
                                       text_color="#000000", fg_color="#ffffff", hover_color="#b1b1b1", font=("", 16))
        
        merge_skin_button.place(x=135-base_skin_button.cget("width")/2, y=146)

        CTkToolTip(merge_skin_button, message="Keycount from this skin gets added to the base skin")

        # OPTION MENU Key Select
        self.key_select = CTkOptionMenu(self, values=["N/A"], width=65, height=25, text_color="#000000", bg_color="#090909"
                                   , font=("", 16), fg_color="#ffffff", button_color="#bebebe", button_hover_color="#929292", command=self.FM.updateTextbox)
        
        self.key_select.place(x=135-self.key_select.cget("width")/2, y=228)

        CTkToolTip(self.key_select, message="The keycount being added to the base skin from the merge skin")

        # BUTTON Merge
        merge_button = CTkButton(self, width=150, height=25, bg_color="#090909", text="Merge",
                                       text_color="#000000", fg_color="#ffffff", hover_color="#b1b1b1", font=("", 16), command=self.FM.merge)
        
        merge_button.place(x=135-base_skin_button.cget("width")/2, y=310)

        CTkToolTip(merge_button, message="Add the selected keycount from the merge skin to the base skin!")

        # Textbox
        self.textbox = CTkTextbox(self, width=598, height=323, font=("", 16))
        self.textbox.place(x=267, y=39)
        self.textbox.configure(state="disabled")
    

    # Error Window Pop-up
    def showErrorWindow(self, message: str, log=None):
        if hasattr(self, "error_box"):
            self.error_box.destroy()
        
        self.error_box = CTkFrame(self, width=300, height=120, fg_color="#2a0000", corner_radius=12, bg_color="#1d1e1e")
        self.error_box.place(relx=0.5, rely=0.5, anchor="center")

        error_label = CTkLabel(self.error_box, text=message, text_color="#ffcccc", wraplength=280, font=("", 14))
        error_label.pack(pady=(15, 5), padx=10)

        close_button = CTkButton(self.error_box, text="Close", width=100, fg_color="#ff4c4c",
                                hover_color="#cc0000", corner_radius=32, command=self.error_box.destroy)
        close_button.pack(pady=(0, 10))

        if log:
            CTkToolTip(error_label, message=log)

    
    # Error Window Pop-up
    def showMessagerWindow(self, message: str):
        if hasattr(self, "message_box"):
            self.message_box.destroy()
        
        self.message_box = CTkFrame(self, width=300, height=120, fg_color="#00002a", corner_radius=12, bg_color="#1d1e1e")
        self.message_box.place(relx=0.5, rely=0.5, anchor="center")

        error_label = CTkLabel(self.message_box, text=message, text_color="#ccccff", wraplength=280, font=("", 14))
        error_label.pack(pady=(15, 5), padx=10)

        close_button = CTkButton(self.message_box, text="Close", width=100, fg_color="#4c4cff",
                                hover_color="#0000cc", corner_radius=32, command=self.message_box.destroy)
        close_button.pack(pady=(0, 10))
        

class SkinMergerLogic:
    def __init__(self, app):
        self.app = app

        # Paths
        self.base_skin_path = None
        self.merge_skin_path = None

        # Keymodes
        self.base_skin_keymodes = None
        self.merge_skin_keymodes = None

        # Selections
        self.selected_keymode = None
        self.merge_filepaths = []
    

    def selectBaseSkin(self):
        try:
            self.base_skin_path = filedialog.askdirectory(title="Select Base Skin Folder")
            self.base_skin_keymodes = iniParser.getKeys(iniParser.findSkinini(self.base_skin_path))
    
        except Exception as e:
            self.app.showErrorWindow("Not a valid skin folder", e)
            return None
        
        self.updateTextbox()
        

    def selectMergeSkin(self):
        try:
            self.merge_skin_path = filedialog.askdirectory(title="Select Merge Skin Folder")
            self.merge_skin_keymodes = iniParser.getKeys(iniParser.findSkinini(self.merge_skin_path))

            keymodes_string = []
            for i in self.merge_skin_keymodes:
                keymodes_string.append(f"{i}k")

            self.app.key_select.configure(values=keymodes_string)
            self.app.key_select.set(keymodes_string[0])
    
        except Exception as e:
            self.merge_skin_path = None
            self.merge_skin_keymodes = None
            self.app.key_select.configure(values=[])
            self.app.key_select.set("N/A")
            self.app.showErrorWindow("Not a valid skin folder", e)
            return None
        
        self.updateTextbox()


    def updateTextbox(self, _=None):
        self.enableTextbox()
        self.app.textbox.delete("0.0", "end")

        # Base Skin Output
        if self.base_skin_path is not None and self.base_skin_path != "" and iniParser.findSkinini(self.base_skin_path) != None:
            self.app.textbox.insert("end", f"Selected Base Skin: {self.getFileName(self.base_skin_path)}\n")
            self.app.textbox.insert("end", "Keymodes: ")
            
            for i in self.base_skin_keymodes:
                self.app.textbox.insert("end", f"{i}k")

                if self.base_skin_keymodes.index(i) != len(self.base_skin_keymodes) - 1:
                    self.app.textbox.insert("end", f", ")
        
        else:
            self.app.textbox.insert("end", f"Selected Base Skin: N/A\n")
            self.app.textbox.insert("end", "Keymodes: N/A")
        
        self.app.textbox.insert("end", "\n\n")

        # Merge Skin Output
        if self.merge_skin_path is not None and self.merge_skin_path != "":
            self.app.textbox.insert("end", f"Selected Merge Skin: {self.getFileName(self.merge_skin_path)} \n")
            self.app.textbox.insert("end", "Keymodes: ")
            
            for i in self.merge_skin_keymodes:
                self.app.textbox.insert("end", f"{i}k")

                if self.merge_skin_keymodes.index(i) != len(self.merge_skin_keymodes) - 1:
                    self.app.textbox.insert("end", f", ")

        else:
            self.app.textbox.insert("end", f"Selected Merge Skin: N/A\n")
            self.app.textbox.insert("end", "Keymodes: N/A")
        
        self.app.textbox.insert("end", "\n\n")

        # Merge Settings
        self.app.textbox.insert("end", f"Selected Keymode to be Merged: {self.app.key_select.get()}")
        
        self.disableTextbox()
    
    
    def merge(self):
        # error
        if iniParser.findSkinini(self.base_skin_path) is None and iniParser.findSkinini(self.merge_skin_path) is None:
            self.app.showErrorWindow("Invalid base and merge skin")
            return None
        
        elif iniParser.findSkinini(self.base_skin_path) is None:
            self.app.showErrorWindow("Invalid base skin")
            return None
        
        elif iniParser.findSkinini(self.merge_skin_path) is None:
            self.app.showErrorWindow("Invalid merge skin")
            return None
        
        if self.base_skin_path == self.merge_skin_path:
            self.app.showErrorWindow("Base skin and merge skin cannot be the same")
            return None

        keycount = int(self.app.key_select.get().strip('k'))
        mania_chunks = iniParser.dictKeyChunks(iniParser.findSkinini(self.merge_skin_path))
        name = f"Merged-Skin-{self.getTime()}"

        # creates skin folder in downloads with files from base skin
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

        new_skin_folder = os.path.join(downloads_folder, name)

        try:
            shutil.copytree(self.base_skin_path, new_skin_folder)
        
        except Exception as e:
            self.app.showErrorWindow("Failed to copy base skin directory to downloads", e)
            return None

        # creates merge files folder
        merge_files_folder = os.path.join(new_skin_folder, "merge_files")

        try:
            os.mkdir(merge_files_folder)
        
        except Exception as e:
            self.app.showErrorWindow("Failed to make merge files folder", e)
            return None

        # gets needed_files and puts them in merge files folder
        needed_files = iniParser.getSectionImages(self.merge_skin_path, mania_chunks[keycount])

        missing_files = []
        for i in needed_files:
            try:
                shutil.copy(i, merge_files_folder)
            
            except Exception as e:
                missing_files.append(os.path.basename(i))
                self.app.showErrorWindow(f"Couldnt copy {len(missing_files)} file(s). Skin sent to your downloads folder.", ", ".join(missing_files))
        
        # edits skin.ini file
        skin_file_path = iniParser.findSkinini(new_skin_folder)
        iniParser.replaceKeySection(skin_file_path, mania_chunks, keycount)

        # Update Author
        iniParser.editValue(skin_file_path, "Author", f"{iniParser.getValue(iniParser.findSkinini(self.base_skin_path), "Author")} + {iniParser.getValue(iniParser.findSkinini(self.merge_skin_path), "Author")}")

        self.finishMerge(len(missing_files))
    

    def finishMerge(self, missing_files):
        if missing_files == 0:
            self.app.showMessagerWindow("Merge completed, skin sent to your downloads folder.")
         
        self.base_skin_path = None
        self.merge_skin_path = None

        self.base_skin_keymodes = None
        self.merge_skin_keymodes = None

        self.selected_keymode = None
        self.merge_filepaths = []

        self.app.key_select.configure(values=[])
        self.app.key_select.set("N/A")
    
        self.updateTextbox()
    

    @staticmethod
    def getFileName(file_path):
        return os.path.basename(file_path)
    
    
    @staticmethod
    def getTime():
        return datetime.now().strftime("%H-%M-%S")


    def disableTextbox(self):
        self.app.textbox.configure(state="disabled")
    
    
    def enableTextbox(self):
        self.app.textbox.configure(state="normal")


if __name__ == "__main__":
    app = SkinMerger()
    app.mainloop()


'''
COLORS
#ffffff - White
#000000 - Black
#1d1e1e - Textbox Color
#090909 - Box Color
'''
