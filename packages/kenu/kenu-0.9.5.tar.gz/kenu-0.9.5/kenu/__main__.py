import sys
import os
import urllib.request
import loadwave
import time
import requests

def main():
    arg = sys.argv[1]
    if ".knu" in arg:
        file_path = sys.argv[1]
        with open(file_path, "r") as f:
            lines = f.readlines()
        im = False
        try:
            # Loop through each line and execute the commands
            for line in lines:
                    line = line.strip()
                    if line.startswith("import") and line.endswith("kenu"):
                        if os.path.isfile(os.path.join(os.environ['APPDATA'], "kenucorp", "modules") + "\\kenu.knu"):
                            im = True
                          
                    elif line.startswith("os.downloadFile"):
                        if im:
                            if '(' in line and ',' in line:
                                start_index = line.find('(') + 1
                                end_index = line.find(',', start_index)
                                url = line[start_index:end_index]
                                start_index = line.find(',') + 1
                                end_index = line.find(')', start_index)
                                filepath = line[start_index:end_index]
                                urllib.request.urlretrieve(url, filepath)
                    elif line.startswith("os.cmd"):
                        if im:
                            if '(' in line:
                                start_index = line.find('(') + 1
                                end_index = line.find(')', start_index)
                                result = line[start_index:end_index]
                                if '"' in result:
                                    start_index = line.find('"') + 1
                                    end_index = line.find('"', start_index)
                                    result = line[start_index:end_index]
                                    os.system(result)
                                else:
                                    exec(f"os.system({result})")
                            else:
                                print("There was an error while saying that.")
                        else:
                            print("There was an error while saying that. Could you have forgotten to import a module?")
                    elif line.startswith("print(") and line.endswith(")"):
                        if im:
                            if '"' in line:
                                start_index = line.find('"') + 1
                                end_index = line.find('"', start_index)
                                result = line[start_index:end_index]
                                exec(f"print('{result}')")
                            elif '(' in line:
                                start_index = line.find('(') + 1
                                end_index = line.find(')', start_index)
                                result = line[start_index:end_index]
                                exec(f"print({result})")
                            else:
                                print("I have found an error. " + line + "\n^^^^^^")
                            
                        else:
                            print("There was an error while saying that. Could you have forgotten to import a module?")
                    elif line.startswith("!"):
                            # Check if line starts with "!", which indicates a variable assignment
                            if im:
                                variable_name, value = line[1:].split("=")
                                value = value.strip()
                                # Check if value is enclosed in quotes
                                if value.startswith('"') and value.endswith('"'):
                                    value = value[1:-1]
                                    exec(f"{variable_name} = '{value}'")
                                else:
                                    exec(f"{variable_name} = {value}")
                            else:
                                print("There was an error while saying that. Could you have forgotten to import a module?")
                    elif "" in line:
                        pass
                    else:
                        print("Invalid command: " + line)
        except:
            pass
    elif sys.argv[1] == "gonder":
            kisi = sys.argv[2]
            print(f"{kisi}'ye hemen kenu atıyorum abi.")
    elif sys.argv[1] == "upload":
            modul = sys.argv[2]
            uploadModule(modul, os.path.join(os.environ['APPDATA'], "kenucorp", "modules"))
    elif arg == "install":
        modul = sys.argv[2]
        if modul == "kenu":
            new_folder = os.path.join(os.environ['APPDATA'], "kenucorp", "modules")
            os.makedirs(new_folder, exist_ok=True)
            print("Loading...")
            filepath = os.path.join(os.environ['APPDATA'], "kenucorp", "modules") + f"\\{modul}.knu"
            kenan = downloadModule(modul, filepath)
            if kenan:
                print("\nThe module downloaded successfully.")
            else:
                print("\nNo such module found.")
        else:
            new_folder = os.path.join(os.environ['APPDATA'], "kenucorp", "modules")
            os.makedirs(new_folder, exist_ok=True)
            print("Loading...")
            filepath = os.path.join(os.environ['APPDATA'], "kenucorp", "modules") + "\\" + modul + "\\" + modul + ".py"
            kenan = downloadModule(modul, filepath)
            if kenan:
                print("\nThe module downloaded successfully.")
            else:
                print("\nNo such module found.")
@loadwave.process 
def downloadModule(module, filepath):
    try:
        if("kenu" in module):
            urllib.request.urlretrieve("https://kenucorp.com/modules/" + module + ".knu", filepath)
        else:
            name = os.path.join(os.environ['APPDATA'], "kenucorp", "modules") + f"\\{module}"
            if not os.path.exists(name):
                os.makedirs(name)
            urllib.request.urlretrieve(f"https://kenucorp.com/modules/" + module + "/" + module + ".py", f"{name}\{module}.py")
            urllib.request.urlretrieve(f"https://kenucorp.com/modules/{module}/{module}requirements.txt", f"{name}\\requirements.txt")
            with open(name + "\\requirements.txt", 'r') as file:
                line = file.readline()
                if(line != ""):
                    uploadmodules(name)
        time.sleep(2.7)
        return True
    except Exception as e:
        print(e)
        return False

@loadwave.process
def uploadmodules(modulename):
    with open(modulename + "\\requirements.txt", 'r') as file:
        line = file.readline().strip()
        while line:
            os.system("pip install " + line)
            line = file.readline().strip()

@loadwave.process 
def uploadModule(module, filepath):
    modulefilepath = filepath + f"\\{module}"
    url = 'https://kenucorp.com/modules/upload.php'
    dosya = open(f'{module}.py', 'r')
    icerik = dosya.read()
    veri = icerik
    dosya.close()
    modules = []
    with open("requirements.txt", 'r') as file:
        line = file.readline().strip()
        while line:
            modules.append(line)
            line = file.readline().strip()
    modname = module
    veriler = {'veri': veri, 'modname': modname, 'modules': '\n'.join(modules)}
    response = requests.post(url, data=veriler)
    return response.text