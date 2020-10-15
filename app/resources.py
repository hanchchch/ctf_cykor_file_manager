from pathlib import Path
import os

CUR_PATH = Path.cwd().absolute()

def icon_html(icon):
    with open('icons/'+icon+'.html') as f:
        html = f.read()
    return html

def get_filetype(filename):
    suf = Path(filename).absolute().suffix
    if suf == '':
        return 'bin'
    elif suf in ['.txt']:
        return 'text'
    elif suf in ['.png','.jpg']:
        return 'image'
    else:
        return 'etc'

def set_file(filename, filetype):
    return {
        'name':filename,
        'type':filetype,
    }

def list_files(directory):
    dir_path = CUR_PATH.joinpath(directory)
    dirs = []
    files = []
    try:
        lists = os.listdir(dir_path)
    except FileNotFoundError:
        lists = []

    for name in lists:
        if os.path.isfile(dir_path.joinpath(name)):
            files.append(name)
        else:
            dirs.append(name)

    return {'dirs':dirs, 'files':files}

