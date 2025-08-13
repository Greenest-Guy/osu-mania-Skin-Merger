from logic import SkinMergerLogic
from CTkToolTip import CTkToolTip
from version import __version__
from customtkinter import *
from PIL import Image
import os


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
                                    dark_image=Image.open(
                                        os.path.join(dir_path, "BG.png")),
                                    size=(900, 400))

        CTkLabel(self, image=background_image, text="").place(x=0, y=0)

        # BUTTON Base Skin
        base_skin_button = CTkButton(self, width=140, height=25, bg_color="#090909", text="Base Skin", command=self.FM.selectBaseSkin,
                                     fg_color="#ffffff", hover_color="#b1b1b1", text_color="#000000", font=("", 16))

        base_skin_button.place(x=135-base_skin_button.cget("width")/2, y=65)

        CTkToolTip(base_skin_button,
                   message="The merge skin will be added to this skin")

        # BUTTON Merge Skin
        merge_skin_button = CTkButton(self, width=140, height=25, bg_color="#090909", text="Merging Skin", command=self.FM.selectMergeSkin,
                                      text_color="#000000", fg_color="#ffffff", hover_color="#b1b1b1", font=("", 16))

        merge_skin_button.place(x=135-merge_skin_button.cget("width")/2, y=126)

        CTkToolTip(merge_skin_button,
                   message="Keycount from this skin gets added to the base skin")

        # OPTION MENU Key Select
        self.key_select = CTkOptionMenu(self, values=["N/A"], width=65, height=25, text_color="#000000", bg_color="#090909", font=(
            "", 16), fg_color="#ffffff", button_color="#bebebe", button_hover_color="#929292", command=self.FM.updateTextbox)

        self.key_select.place(x=135-self.key_select.cget("width")/2, y=248)

        CTkToolTip(
            self.key_select, message="The keycount being added to the base skin from the merge skin")

        # OPTION MENU Merge Option
        self.merge_option = CTkOptionMenu(self, values=["New Skin", "Overwrite Skin"], width=140, height=25, text_color="#000000", bg_color="#090909", font=(
            "", 16), fg_color="#ffffff", button_color="#bebebe", button_hover_color="#929292", command=self.updateToolTip)

        self.merge_option.place(x=135-self.merge_option.cget("width")/2, y=187)

        self.merge_option_tip = CTkToolTip(
            self.merge_option, message="Create a new merged skin in your downloads folder")

        # BUTTON Merge
        merge_button = CTkButton(self, width=120, height=25, bg_color="#090909", text="Merge",
                                 text_color="#000000", fg_color="#ffffff", hover_color="#b1b1b1", font=("", 16), command=self.FM.mergeLogic)

        merge_button.place(x=135-merge_button.cget("width")/2, y=310)

        CTkToolTip(
            merge_button, message="Merge the selected keycount from the merge skin to the base skin")

        # Textbox
        self.textbox = CTkTextbox(self, width=598, height=323, font=("", 16))
        self.textbox.place(x=267, y=39)
        self.textbox.configure(state="disabled")

    def updateToolTip(self, merge_option):
        if merge_option == "New Skin":
            self.merge_option_tip.configure(
                message="Create the merged skin in your downloads folder")

        else:
            self.merge_option_tip.configure(
                message="WARNING: Overwriting will modify your base skin permanently")

        # Error Window Pop-up

    def showErrorWindow(self, message: str, log=None):
        if hasattr(self, "error_box"):
            self.error_box.destroy()

        self.error_box = CTkFrame(
            self, width=300, height=120, fg_color="#2a0000", corner_radius=12, bg_color="#1d1e1e")
        self.error_box.place(relx=0.5, rely=0.5, anchor="center")

        error_label = CTkLabel(self.error_box, text=message,
                               text_color="#ffcccc", wraplength=280, font=("", 14))
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

        self.message_box = CTkFrame(
            self, width=300, height=120, fg_color="#00002a", corner_radius=12, bg_color="#1d1e1e")
        self.message_box.place(relx=0.5, rely=0.5, anchor="center")

        error_label = CTkLabel(self.message_box, text=message,
                               text_color="#ccccff", wraplength=280, font=("", 14))
        error_label.pack(pady=(15, 5), padx=10)

        close_button = CTkButton(self.message_box, text="Close", width=100, fg_color="#4c4cff",
                                 hover_color="#0000cc", corner_radius=32, command=self.message_box.destroy)
        close_button.pack(pady=(0, 10))


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
