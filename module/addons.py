class Progress_bar():    
    def print (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
        # Print New Line on Complete
        if iteration == total: 
            print()

import os, shutil
class Dirs_files():
    def append_new_line(file_name, text_to_append):
        """Append given text as a new line at the end of file"""
        # if os.path.exists(file_name):
        #     os.remove(file_name)
        # Open the file in append & read mode ('a+')
        with open(file_name, "a+",encoding='utf-8') as file_object:
            # Move read cursor to the start of file.
            file_object.seek(0)
            # If file is not empty then append '\n'
            data = file_object.read(100)
            if len(data) > 0:
                file_object.write("\n")
            # Append text at the end of file
            file_object.write(text_to_append)

    def create_folder_if_inexistent(path):
        isExist = os.path.exists(path)

        if not isExist:
            os.makedirs(path)
            return True
        else:
            shutil.rmtree(path)
            os.makedirs(path)
            return False