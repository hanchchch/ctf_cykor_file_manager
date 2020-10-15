from flask import Flask, request, render_template, Response, redirect
from pathlib import Path
from resources import set_file, get_filetype, list_files
from resources import CUR_PATH

app = Flask(__name__)

@app.route('/<path:directory>', methods=['GET'])
def index(directory):
    try:
        lists = list_files(CUR_PATH.joinpath(directory))
    except NotADirectoryError:
        with open(CUR_PATH.joinpath(directory)) as f:
            contents = f.read()
        return Response(contents)
    files = []
    for d in lists['dirs']:
        files.append(set_file(d, 'dir'))
    for f in lists['files']:
        files.append(set_file(f, get_filetype(f)))

    return render_template('index.html', files=files, cur_path=directory)

@app.route('/')
def etc():
    return redirect('/files')

if __name__=="__main__":
    app.run(host='0.0.0.0', port=8080, debug=False)