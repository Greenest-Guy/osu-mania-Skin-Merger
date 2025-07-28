'''
Github: https://github.com/Greenest-Guy
'''

import os


class iniParser:
    # returns the file as a string
    @staticmethod
    def getContents(file_path): 
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()

        return content


    # returns a list containing the files lines
    @staticmethod
    def getLines(file_path): 
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.readlines()
        
        return content


    # returns line number
    @staticmethod
    def getLine(file_path, line): 
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.readlines()

        return content[line - 1]
    

    @staticmethod
    def startsWith(line, starting: str):
        return line.lower().strip().startswith(starting.lower())


    # find skin.ini from dir path
    def findSkinini(dir_path):
        try:
            for file in os.listdir(dir_path):
                if os.path.isfile(os.path.join(dir_path, file)) and file.lower() == "skin.ini":
                    return os.path.join(dir_path, file)
                
        except Exception as e:
            return None
    

    # gets the value associated with a line
    @staticmethod
    def getLineValue(line): 
        return line[(line.index(':')+1):].strip()


    # gets the key associated with a line
    @staticmethod
    def getKeyValue(line):
        return line[:line.index(':')]
    

    # gets the first instance of a value associated with a key
    @staticmethod
    def getValue(file_path, key):
        for line in iniParser.getLines(file_path):
            if iniParser.startsWith(line, f"{key}:"):
                return iniParser.getLineValue(line)


    # returns a list of all catagories
    @staticmethod
    def getCatagories(file_path): 
        catagories = []
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.readlines()
        
        for line in content:
            line = line.strip()
            if iniParser.startsWith(line, '[') and line.endswith(']') and line not in catagories:
                catagories.append(line)

        return catagories
    
    # returns directory path
    @staticmethod
    def getDirPath(file_path):
        return os.path.dirname(file_path)
    

    # returns a list of all image paths (relating to notes or keys)
    @staticmethod
    def getImages(file_path): 
        images = []

        for line in iniParser.getLines(file_path):
            if (iniParser.startsWith(line, "NoteImage") or iniParser.startsWith(line, "KeyImage")) and iniParser.getLineValue(line) not in images:
                images.append(iniParser.getLineValue(line))
        
        return images


    # returns a list of all image paths
    @staticmethod
    def getImagesPath(file_path):
        images = []
        for image in iniParser.getImages(file_path):
            images.append(os.path.join(iniParser.getDirPath(file_path), image.replace('/', os.sep)) + '.png')
        
        return images
    

    @staticmethod
    def getSectionImages(file_path, chunk):
        images = []

        for line in chunk.splitlines():
            if (iniParser.startsWith(line, "NoteImage") or iniParser.startsWith(line, "KeyImage")) and iniParser.getLineValue(line) not in images:
                images.append((os.path.join(file_path, iniParser.getLineValue(line)) + ".png").replace('/', os.sep))
        
        return images


    @staticmethod
    def getNewSectionImages(chunk):
        new_chunk = []

        for line in chunk.splitlines():
            if iniParser.startsWith(line, "NoteImage") or iniParser.startsWith(line, "KeyImage"):
                new_chunk.append(f"{iniParser.getKeyValue(line)}: merge_files{os.sep}{os.path.basename(iniParser.getLineValue(line))}")
            
            else:
                new_chunk.append(line)
        
        return "\n".join(new_chunk)


    # edits a key value
    @staticmethod
    def editValue(file_path, value_name, new_value):
        lines = iniParser.getLines(file_path)
        
        for index, line in enumerate(lines):
            if iniParser.startsWith(line, value_name + ":"):
                lines[index] = f"{iniParser.getKeyValue(line)}: {new_value}\n"
        
        with open(file_path, 'w', encoding="utf-8") as file:
            file.writelines(lines)


    # returns a list of all keycounts in a skin.ini file
    @staticmethod
    def getKeys(file_path):
        keys = []

        for line in iniParser.getLines(file_path):
            if iniParser.startsWith(line, "keys: "):
                key = int(iniParser.getLineValue(line))
                if key not in keys:
                    keys.append(key)
        
        keys.sort()
        
        return keys


    # seperates each [Mania] block into a dictionary with the key being the keycount that [Mania] block is associated with and the value being the block itself
    @staticmethod
    def dictKeyChunks(file_path):
        key_chunks = {}
        lines = iniParser.getLines(file_path)

        current_chunk = []
        current_key = None

        # add non [Mania] Section(s)
        for line in lines:
            line = line.strip()
            if not iniParser.startsWith(line, "[mania]"):
                current_chunk.append(line)

            else:
                break

        key_chunks[-1] = "\n".join(current_chunk)
        current_chunk = []

        for line in lines:
            line = line.strip()

            # if [Mania] line, append this line to current_chunk
            if iniParser.startsWith(line, "[mania]"):
                # if both current_chunk isnt empty and current_key isnt None, add the entire chunk to the dictionary and reset both variables
                if (current_chunk and current_key is not None) and current_key not in key_chunks:
                    key_chunks[current_key] = "\n".join(current_chunk)
                    current_chunk = []
                    current_key = None
                    
                current_chunk.append(line)

            # if line starts with "keys: " extract key value and set current_key
            elif iniParser.startsWith(line, "keys:"):
                current_key = int(iniParser.getLineValue(line))
                current_chunk.append(line)
            
            # if a chunk is already started add line to chunk
            elif current_chunk:
                current_chunk.append(line)
            
        # add last pending chunk
        if current_chunk and current_key is not None:
            key_chunks[current_key] = "\n".join(current_chunk)


        return key_chunks

    
    @staticmethod
    def replaceKeySection(skin_file_path, section, num):
        sections = iniParser.dictKeyChunks(skin_file_path)
        
        if num not in sections:
            sections[num] = iniParser.getNewSectionImages(section[num])
            sections = dict(sorted(sections.items()))
        
        elif num in sections:
            sections[num] = iniParser.getNewSectionImages(section[num])
        
        new_file = ""

        for i in sections:
            new_file += sections[i] + "\n"

        with open(skin_file_path, 'w', encoding="utf-8") as file:
            file.write(new_file)
