from default_assets import DEFAULT_ASSETS
from key_layouts import KEYLAYOUTS
from IniParser import IniParser
from tkinter import filedialog
from datetime import datetime
import shutil
import os


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
            self.base_skin_path = filedialog.askdirectory(
                title="Select Base Skin Folder")
            self.base_skin_keymodes = IniParser.getKeys(
                IniParser.findSkinini(self.base_skin_path))

        except Exception as e:
            self.app.showErrorWindow("Not a valid skin folder", e)
            return None

        self.updateTextbox()

    def selectMergeSkin(self):
        try:
            self.merge_skin_path = filedialog.askdirectory(
                title="Select Merge Skin Folder")
            self.merge_skin_keymodes = IniParser.getKeys(
                IniParser.findSkinini(self.merge_skin_path))

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
        if self.base_skin_path is not None and self.base_skin_path != "" and IniParser.findSkinini(self.base_skin_path) != None:
            self.app.textbox.insert(
                "end", f"Selected Base Skin: {self.getFileName(self.base_skin_path)}\n")
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
            self.app.textbox.insert(
                "end", f"Selected Merge Skin: {self.getFileName(self.merge_skin_path)} \n")
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
        self.app.textbox.insert(
            "end", f"Selected Keymode to be Merged: {self.app.key_select.get()}")

        self.disableTextbox()

    def mergeNewSkin(self):
        keycount = int(self.app.key_select.get().strip('k'))
        mania_sections = IniParser.dictKeySections(
            IniParser.findSkinini(self.merge_skin_path))

        name = f"Merged-Skin-{self.getTime()}"

        # creates skin folder in downloads with files from base skin
        self.downloads_folder = os.path.join(
            os.path.expanduser("~"), "Downloads")

        new_skin_folder = os.path.join(self.downloads_folder, name)

        try:
            shutil.copytree(self.base_skin_path, new_skin_folder)

        except Exception as e:
            self.app.showErrorWindow(
                "Failed to copy base skin directory to downloads", e)
            return None

        # creates merge files folder
        merge_files_folder = os.path.join(new_skin_folder, "merge_files")

        if not os.path.exists(merge_files_folder):
            try:
                os.mkdir(merge_files_folder)

            except Exception as e:
                self.app.showErrorWindow(
                    "Failed to make merge files folder", e)
                return None

        # creates [num]_key folder
        key_folder = os.path.join(merge_files_folder, f"{keycount}_key")

        if os.path.exists(key_folder):
            shutil.rmtree(key_folder)

        os.mkdir(key_folder)

        # gets needed_files and puts them in merge files folder
        needed_files = IniParser.getSectionImages(
            self.merge_skin_path, mania_sections[keycount])

        missing_files = []
        for i in needed_files:
            found = False
            hd_image = IniParser.getHDImage(i)
            if os.path.exists(hd_image):
                shutil.copy(hd_image, key_folder)
                found = True

            if os.path.exists(i):
                shutil.copy(i, key_folder)
                found = True

            if IniParser.animationExists(hd_image) or IniParser.animationExists(i):
                if IniParser.animationExists(hd_image):
                    for animation in IniParser.getAnimations(hd_image):
                        shutil.copy(animation, key_folder)

                if IniParser.animationExists(i):
                    for animation in IniParser.getAnimations(i):
                        shutil.copy(animation, key_folder)

                found = True

            if os.path.exists(i):
                shutil.copy(i, key_folder)
                found = True

            if not found:
                missing_files.append(os.path.basename(i))

        if len(missing_files) == 1:
            self.app.showErrorWindow(
                f"Couldnt copy {len(missing_files)} file. Skin sent to your downloads folder.", ", ".join(missing_files))

        elif len(missing_files) > 1:
            self.app.showErrorWindow(
                f"Couldnt copy {len(missing_files)} files. Skin sent to your downloads folder.", ", ".join(missing_files))

        # edits skin.ini file
        skin_file_path = IniParser.findSkinini(new_skin_folder)
        IniParser.replaceKeySection(skin_file_path, mania_sections, keycount)

        # get possible default images merge_skin_path, destination_skin_path, keycount

        self.updateJudgements(skin_file_path, new_skin_folder, keycount)

        self.copyDefaultKeyImages(
            self.merge_skin_path, new_skin_folder, keycount)

        LNtypes = ["", "H", "L", "T"]

        for LNtype in LNtypes:
            self.copyDefaultNoteImages(
                self.merge_skin_path, new_skin_folder, keycount, type=LNtype)

        for asset_name, default_file_names in DEFAULT_ASSETS:
            base_filename = os.path.splitext(default_file_names[0])[0]

            self.copyDefaultAsset(self.merge_skin_path,
                                  new_skin_folder,
                                  keycount,
                                  asset_name,
                                  asset_name,
                                  default_file_names,
                                  base_filename)

        # Update Author
        IniParser.editValue(skin_file_path, "Author",
                            f"{IniParser.getValue(IniParser.findSkinini(self.base_skin_path), "Author")} + {IniParser.getValue(IniParser.findSkinini(self.merge_skin_path), "Author")}")

        self.finishMerge(len(missing_files))

        # Adds Tag to top (Skins merged using github.com/Greenest-Guy/osu-mania-Skin-Merger)
        IniParser.addTag(skin_file_path)

    def overwriteSkin(self):
        keycount = int(self.app.key_select.get().strip('k'))
        mania_sections = IniParser.dictKeySections(
            IniParser.findSkinini(self.merge_skin_path))

        merge_files_folder = os.path.join(self.base_skin_path, "merge_files")

        if not os.path.exists(merge_files_folder):
            try:
                os.mkdir(merge_files_folder)

            except Exception as e:
                self.app.showErrorWindow(
                    "Failed to make merge files folder", e)
                return None

        # creates [num]_key folder
        key_folder = os.path.join(merge_files_folder, f"{keycount}_key")

        if os.path.exists(key_folder):
            shutil.rmtree(key_folder)

        os.mkdir(key_folder)

        # gets needed_files and puts them in merge files folder
        needed_files = IniParser.getSectionImages(
            self.merge_skin_path, mania_sections[keycount])

        missing_files = []

        for i in needed_files:
            found = False
            hd_image = IniParser.getHDImage(i)
            if os.path.exists(hd_image):
                shutil.copy(hd_image, key_folder)
                found = True

            if os.path.exists(i):
                shutil.copy(i, key_folder)
                found = True

            if IniParser.animationExists(hd_image) or IniParser.animationExists(i):
                if IniParser.animationExists(hd_image):
                    for animation in IniParser.getAnimations(hd_image):
                        shutil.copy(animation, key_folder)

                if IniParser.animationExists(i):
                    for animation in IniParser.getAnimations(i):
                        shutil.copy(animation, key_folder)

                found = True

            if os.path.exists(i):
                shutil.copy(i, key_folder)
                found = True

            if not found:
                missing_files.append(os.path.basename(i))

        if len(missing_files) == 1:
            self.app.showErrorWindow(
                f"Couldnt copy {len(missing_files)} file. {os.path.basename(self.base_skin_path)} has been updated.", ", ".join(missing_files))

        elif len(missing_files) > 1:
            self.app.showErrorWindow(
                f"Couldnt copy {len(missing_files)} files. {os.path.basename(self.base_skin_path)} has been updated.", ", ".join(missing_files))

        # edits skin.ini file
        skin_file_path = IniParser.findSkinini(self.base_skin_path)
        IniParser.replaceKeySection(skin_file_path, mania_sections, keycount)

        # get possible default images merge_skin_path, destination_skin_path, keycount
        self.updateJudgements(skin_file_path, self.base_skin_path, keycount)

        self.copyDefaultKeyImages(
            self.merge_skin_path, self.base_skin_path, keycount)

        LNtypes = ["", "H", "L", "T"]

        for LNtype in LNtypes:
            self.copyDefaultNoteImages(
                self.merge_skin_path, self.base_skin_path, keycount, type=LNtype)

        for asset_name, default_file_names in DEFAULT_ASSETS:
            base_filename = os.path.splitext(default_file_names[0])[0]

            self.copyDefaultAsset(self.merge_skin_path,
                                  self.base_skin_path,
                                  keycount,
                                  asset_name,
                                  asset_name,
                                  default_file_names,
                                  base_filename)

        # Update Author
        base_skin_author = IniParser.getValue(
            IniParser.findSkinini(self.base_skin_path), "Author")
        IniParser.editValue(skin_file_path, "Author",
                            f"{base_skin_author} + {IniParser.getValue(IniParser.findSkinini(self.merge_skin_path), "Author")}")

        self.finishMerge(len(missing_files))

    def mergeLogic(self):
        # error checking
        if IniParser.findSkinini(self.base_skin_path) is None and IniParser.findSkinini(self.merge_skin_path) is None:
            self.app.showErrorWindow("Invalid base and merge skin")
            return None

        elif IniParser.findSkinini(self.base_skin_path) is None:
            self.app.showErrorWindow("Invalid base skin")
            return None

        elif IniParser.findSkinini(self.merge_skin_path) is None:
            self.app.showErrorWindow("Invalid merge skin")
            return None

        if self.base_skin_path == self.merge_skin_path:
            self.app.showErrorWindow(
                "Base skin and merge skin cannot be the same")
            return None

        if self.app.merge_option.get() == "New Skin":
            self.mergeNewSkin()

        elif self.app.merge_option.get() == "Overwrite Skin":
            self.overwriteSkin()

    def finishMerge(self, missing_files):
        if missing_files == 0:
            if self.app.merge_option.get() == "New Skin":
                self.app.showMessagerWindow(
                    "Merge completed, skin sent to your downloads folder!")

            elif self.app.merge_option.get() == "Overwrite Skin":
                self.app.showMessagerWindow(
                    f"Merge completed, {os.path.basename(self.base_skin_path)} has been updated!")

        self.base_skin_path = None
        self.merge_skin_path = None

        self.base_skin_keymodes = None
        self.merge_skin_keymodes = None

        self.selected_keymode = None
        self.merge_filepaths = []

        self.app.key_select.configure(values=[])
        self.app.key_select.set("N/A")

        self.updateTextbox()

    def updateJudgements(self, merged_file, destination_skin_path, keycount):
        sections = IniParser.dictKeySections(merged_file)

        section = sections[keycount]

        key_folder = f"{destination_skin_path}{os.sep}merge_files{os.sep}{keycount}_key"

        judgment_names = ["mania-hit0", "mania-hit50", "mania-hit100",
                          "mania-hit200", "mania-hit300", "mania-hit300g"]

        judgement_keys = ["Hit0", "Hit50",
                          "Hit100", "Hit200", "Hit300", "Hit300g"]

        if all(hit not in section for hit in judgement_keys):
            for hit in judgement_keys:
                section += f"\n{hit}: merge_files{os.sep}{keycount}_key{os.sep}mania-{hit.lower()}"

        else:
            return None

        missing_skins = 0

        for i in judgment_names:
            paths = [f"{self.merge_skin_path}{os.sep}{i}.png",
                     f"{os.path.dirname(self.merge_skin_path)}{os.sep}{i}@2x.png"]

            for path in paths:
                if os.path.exists(path):
                    shutil.copy(path, key_folder)

                elif IniParser.getAnimations(path) != None:
                    for animation in IniParser.getAnimations(path):
                        shutil.copy(animation, key_folder)

        sections[keycount] = section

        with open(merged_file, 'w', encoding="utf-8") as file:
            file.write("\n".join(sections.values()))

    def copyDefaultKeyImages(self, merge_skin_path, destination_skin_path, keycount):
        search = "KeyImage"

        key_folder = f"{destination_skin_path}{os.sep}merge_files{os.sep}{keycount}_key"

        key_layout = KEYLAYOUTS[keycount]

        sections = IniParser.dictKeySections(
            IniParser.findSkinini(destination_skin_path))

        section = sections[keycount]

        variations = ["1", "2", "S"]

        if search not in section:
            for i in variations:
                found = False

                file_paths = [f"{merge_skin_path}{os.sep}mania-key{i}.png",
                              f"{merge_skin_path}{os.sep}mania-key{i}@2x.png",
                              f"{merge_skin_path}{os.sep}mania-key{i}D.png",
                              f"{merge_skin_path}{os.sep}mania-key{i}D@2x.png"]

                for file in file_paths:
                    if os.path.exists(file):
                        shutil.copy(file, key_folder)
                        found = True

                    elif IniParser.getAnimations(file) != None:
                        for animation in IniParser.getAnimations(file):
                            shutil.copy(animation, key_folder)

                if not found:
                    self.app.showErrorWindow(
                        "mania-key not found")
                    return False

            for i in range(keycount):
                section += f"\nKeyImage{i}: merge_files/{keycount}_key/mania-key{key_layout[i]}"
                section += f"\nKeyImage{i}D: merge_files/{keycount}_key/mania-key{key_layout[i]}D"

            sections[keycount] = section

            destination_skinini = IniParser.findSkinini(destination_skin_path)

            with open(destination_skinini, 'w', encoding="utf-8") as file:
                file.write("\n".join(sections.values()))

            return True
        return False

    def copyDefaultNoteImages(self, merge_skin_path, destination_skin_path, keycount, type=""):
        search = f"NoteImage0{type}:"

        key_folder = f"{destination_skin_path}{os.sep}merge_files{os.sep}{keycount}_key"

        key_layout = KEYLAYOUTS[keycount]

        sections = IniParser.dictKeySections(
            IniParser.findSkinini(destination_skin_path))

        section = sections[keycount]

        if search not in section:

            found = False

            file_paths = [f"{merge_skin_path}{os.sep}mania-note1{type}.png",
                          f"{merge_skin_path}{os.sep}mania-note1{type}@2x.png",
                          f"{merge_skin_path}{os.sep}mania-note2{type}.png",
                          f"{merge_skin_path}{os.sep}mania-note2{type}@2x.png",
                          f"{merge_skin_path}{os.sep}mania-noteS{type}.png",
                          f"{merge_skin_path}{os.sep}mania-noteS{type}@2x.png",]

            for file in file_paths:
                if os.path.exists(file):
                    shutil.copy(file, key_folder)
                    found = True

                elif IniParser.getAnimations(file) != None:
                    for animation in IniParser.getAnimations(file):
                        shutil.copy(animation, key_folder)

            if not found and type == "T":
                for i in range(keycount):
                    section += f"\nNoteImage{i}{type}: merge_files/{keycount}_key/mania-note{key_layout[i]}H"

                sections[keycount] = section

                destination_skinini = IniParser.findSkinini(
                    destination_skin_path)

                with open(destination_skinini, 'w', encoding="utf-8") as file:
                    file.write("\n".join(sections.values()))

                return True

            if not found:
                self.app.showErrorWindow(
                    f"mania-note{type} not found")
                return False

            for i in range(keycount):
                section += f"\nNoteImage{i}{type}: merge_files/{keycount}_key/mania-note{key_layout[i]}{type}"

            sections[keycount] = section

            destination_skinini = IniParser.findSkinini(destination_skin_path)

            with open(destination_skinini, 'w', encoding="utf-8") as file:
                file.write("\n".join(sections.values()))

            return True
        return False

    def copyDefaultAsset(self, merge_skin_path, destination_skin_path, keycount, search_key, key,
                         expected_files, default_file_name):

        key_folder = f"{destination_skin_path}{os.sep}merge_files{os.sep}{keycount}_key"

        dest_skinini_path = IniParser.findSkinini(destination_skin_path)

        sections = IniParser.dictKeySections(dest_skinini_path)
        section = sections[keycount]

        search_key += ":"

        if search_key in section:
            return False

        found = False

        for file in expected_files:
            file = os.path.join(merge_skin_path, file)
            if os.path.exists(file):
                shutil.copy(file, key_folder)
                found = True

            elif IniParser.getAnimations(file) != None:
                for animation in IniParser.getAnimations(file):
                    shutil.copy(animation, key_folder)
                found = True

        if not found:
            section += f"\n{key}: _blank"

        if found:
            section += f"\n{key}: merge_files/{keycount}_key/{default_file_name}"

        sections[keycount] = section

        with open(dest_skinini_path, 'w', encoding="utf-8") as file:
            file.write("\n".join(sections.values()))

    def checkForAnimations():
        pass

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
