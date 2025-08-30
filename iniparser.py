import os

'''
Github: https://github.com/Greenest-Guy

VARIABLE NAMING
    file_path --> Complete file path to a skin.ini file
    content -->  Complete contents of a skin.ini file
    dir_path --> Path to a directory
'''


class IniParser:
    # returns contents of file at file_path
    @staticmethod
    def getContents(file_path):
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()

        return content

    # returns a list of lines from the file at file_path

    @staticmethod
    def getLines(file_path):
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.readlines()

        return content

    # returns the line at index n (1-based) from file_path (skin.ini)

    @staticmethod
    def getLine(file_path, index):
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.readlines()

        if index < 1 or index > len(content):
            raise IndexError("Line index out of range.")

        return content[index - 1]

    # returns true or false by seeing if line starts with starting (case-insensitive and clears whitespace)

    @staticmethod
    def startsWith(line, starting: str):
        return line.lower().strip().startswith(starting.lower())

    # returns complete path to the skin.ini within a directory (non-recursive)

    @staticmethod
    def findSkinini(dir_path):
        try:
            for file in os.listdir(dir_path):
                if os.path.isfile(os.path.join(dir_path, file)) and file.lower() == "skin.ini":
                    return os.path.join(dir_path, file)

        except Exception:
            return None

    # returns the value from the key:value pair in line

    @staticmethod
    def getValueFromLine(line):
        if ':' not in line:
            return None

        return line[(line.index(':')+1):].strip()

    # returns the key from the key:value pair in line

    @staticmethod
    def getKeyFromLine(line):
        if ':' not in line:
            return None

        return line.split(':', 1)[0].strip()

    # returns the first instance of a value associated with key

    @staticmethod
    def getValue(file_path, key):
        for line in IniParser.getLines(file_path):
            if IniParser.startsWith(line, f"{key}:"):
                return IniParser.getValueFromLine(line)

    # returns keycount associated with a section

    @staticmethod
    def getSectionKeycount(section):
        for line in section.splitlines():
            if IniParser.startsWith(line, "keys:"):
                return IniParser.getValueFromLine(line)

    # returns a list of all categories within a skin.ini file

    @staticmethod
    def getCategories(file_path):
        categories = []
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.readlines()

        for line in content:
            line = line.strip()
            if IniParser.startsWith(line, '[') and line.endswith(']') and line not in categories:
                categories.append(line)

        return categories

    # returns the directory path of file_path

    @staticmethod
    def getDirPath(file_path):
        return os.path.dirname(file_path)

    # returns true or false regarding if line contains an image path (NoteImage, KeyImage, Hit0, Hit50, Hit100, Hit200, Hit300, Hit300g) # IniParser.isImageLine(line)

    @staticmethod
    def isImageLine(line):
        return (IniParser.startsWith(line, "NoteImage") or
                IniParser.startsWith(line, "KeyImage") or
                IniParser.startsWith(line, "Stage") or
                IniParser.startsWith(line, "WarningArrow") or
                (IniParser.startsWith(line, "Lighting") and not IniParser.startsWith(line, "LightingLWidth")) or
                (IniParser.startsWith(line, "Hit") and not IniParser.startsWith(line, "HitPosition")))

    # returns a list of all local image paths from a skin.ini file

    @staticmethod
    def getImages(file_path):
        images = []

        for line in IniParser.getLines(file_path):
            if IniParser.isImageLine(line) and IniParser.getValueFromLine(line) not in images:
                images.append(IniParser.getValueFromLine(line))

        return images

    # returns a list of all complete image paths from a skin.ini file

    @staticmethod
    def getImagesPath(file_path):
        images = []
        for image in IniParser.getImages(file_path):
            images.append(os.path.join(IniParser.getDirPath(
                file_path), image.replace('/', os.sep)) + '.png')

        return images

    # returns a list of all complete image paths from a skin.ini file at a specific section

    @staticmethod
    def getSectionImages(file_path, section):
        images = []

        for line in section.splitlines():
            if (IniParser.isImageLine(line)) and IniParser.getValueFromLine(line) not in images:
                images.append((os.path.join(file_path, IniParser.getValueFromLine(
                    line)) + ".png").replace('/', os.sep))

        return images

    # returns a list of the corrected image paths for the files in the merge_folder

    @staticmethod
    def getNewSectionImages(section):
        new_section = []
        key_count = IniParser.getSectionKeycount(section)

        for line in section.splitlines():
            if (IniParser.isImageLine(line)) and IniParser.getValueFromLine(line):
                new_section.append(
                    f"{IniParser.getKeyFromLine(line)}: merge_files{os.sep}{key_count}_key{os.sep}{os.path.basename(IniParser.getValueFromLine(line))}")

            else:
                new_section.append(line)

        return "\n".join(new_section)

    # returns the equivalent HD file path of an image

    @staticmethod
    def getHDImage(image_path):
        base, extension = os.path.splitext(image_path)
        return f"{base}@2x{extension}"

    # EDIT FUNCTION: Edits a value of a keyvalue pair within a skin.ini file

    @staticmethod
    def editValue(file_path, value_name, new_value):
        lines = IniParser.getLines(file_path)

        for index, line in enumerate(lines):
            if IniParser.startsWith(line, value_name + ":"):
                lines[index] = f"{IniParser.getKeyFromLine(line)}: {new_value}\n"

        with open(file_path, 'w', encoding="utf-8") as file:
            file.writelines(lines)

    # returns a list of all keycounts in a skin.ini file

    @staticmethod
    def getKeys(file_path):
        keys = []

        for line in IniParser.getLines(file_path):
            if IniParser.startsWith(line, "keys:"):
                key = int(IniParser.getValueFromLine(line))
                if key not in keys:
                    keys.append(key)

        keys.sort()

        return keys

    # seperates each [Mania] block into a dictionary with the key being the keycount that [Mania] block is associated with and the value being the block itself

    @staticmethod
    def dictKeySections(file_path):
        key_sections = {}
        lines = IniParser.getLines(file_path)

        current_section = []
        current_key = None

        # add non [Mania] Section(s)
        for line in lines:
            line = line.strip()
            if not IniParser.startsWith(line, "[mania]"):
                current_section.append(line)

            else:
                break

        key_sections[-1] = "\n".join(current_section)
        current_section = []

        for line in lines:
            line = line.strip()

            # if [Mania] line, append this line to current_section
            if IniParser.startsWith(line, "[mania]"):
                # if both current_section isnt empty and current_key isnt None, add the entire section to the dictionary and reset both variables
                if (current_section and current_key is not None) and current_key not in key_sections:
                    key_sections[current_key] = "\n".join(current_section)
                    current_section = []
                    current_key = None

                current_section.append(line)

            # if line starts with "keys: " extract key value and set current_key
            elif IniParser.startsWith(line, "keys:"):
                current_key = int(IniParser.getValueFromLine(line))
                current_section.append(line)

            # if a section is already started add line to section
            elif current_section:
                current_section.append(line)

        # add last pending section
        if current_section and current_key is not None:
            key_sections[current_key] = "\n".join(current_section)

        return key_sections

    # EDIT FUNCTION: replaces a key section within skin_file_path with section regarding key count num

    @staticmethod
    def replaceKeySection(file_path, section, num):
        sections = IniParser.dictKeySections(file_path)

        if num not in sections:
            sections[num] = IniParser.getNewSectionImages(section[num])
            sections = dict(sorted(sections.items()))

        elif num in sections:
            sections[num] = IniParser.getNewSectionImages(section[num])

        new_file = ""

        for i in sections:
            new_file += sections[i] + "\n"

        with open(file_path, 'w', encoding="utf-8") as file:
            file.write(new_file)

    # removes either @2x.png or .png from end
    @staticmethod
    def removeSuffix(path):
        return path.removesuffix("@2x.png").removesuffix(".png")

    # returns either @2x.png or .png that is at the end
    def getSuffix(path):
        if path.lower().endswith("@2x.png"):
            return "@2x.png"

        if path.lower().endswith(".png"):
            return ".png"

    @staticmethod
    def animationExists(path):
        suffix = IniParser.getSuffix(path)
        return os.path.exists(f"{IniParser.removeSuffix(path)}-0{suffix}")

    @staticmethod
    def getAnimations(file_path):
        suffix = IniParser.getSuffix(file_path)
        animations = []
        exists = True
        num = 0

        if IniParser.animationExists(file_path):
            while exists:
                animation = f"{IniParser.removeSuffix(file_path)}-{num}{suffix}"

                if os.path.exists(animation):
                    animations.append(animation)
                    num += 1

                else:
                    exists = False

            return animations

        return None

    # adds a tag to the top of file_path "//Skins merged using github.com/Greenest-Guy/osu-mania-Skin-Merger\n"
    @staticmethod
    def addTag(file_path):
        tag = "//Skins merged using github.com/Greenest-Guy/osu-mania-Skin-Merger\n"
        with open(file_path, 'r', encoding="utf-8") as f:
            original_content = f.read()

        if tag not in original_content:
            with open(file_path, 'w', encoding="utf-8") as file:
                file.write(tag)
                file.write(original_content)
