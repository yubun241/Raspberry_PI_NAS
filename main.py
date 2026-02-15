from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
import os
import shutil

UPLOAD_DIR = ""

app = FastAPI()

def safe_path(path: str):
    full_path = os.path.abspath(os.path.join(UPLOAD_DIR, path))

    if not full_path.startswith(os.path.abspath(UPLOAD_DIR)):
        raise HTTPException(status_code=403, detail="Forbidden")

    return full_path


# UI
@app.get("/", response_class=HTMLResponse)
def index(path: str = ""):

    current_dir = safe_path(path)

    if not os.path.exists(current_dir):
        return "Folder not found"

    items = os.listdir(current_dir)

    file_list = ""

    # ?????
    if path:
        parent = os.path.dirname(path)
        file_list += f"<li><a href='/?path={parent}'>? Back</a></li>"

    for item in items:

        item_path = os.path.join(current_dir, item)
        rel_path = os.path.join(path, item)

        if os.path.isdir(item_path):

            file_list += f"""
            <li>
            ? <a href='/?path={rel_path}'>{item}</a>
            <a href='/delete_folder?path={rel_path}'>Delete</a>
            </li>
            """

        else:

            file_list += f"""
            <li>
            ? {item}
            <a href='/download?path={rel_path}'>Download</a>
            <a href='/delete_file?path={rel_path}'>Delete</a>
            </li>
            """

    return f"""
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>

    <body>

    <h2>Mobile S3 Server</h2>

    <p>Current: /{path}</p>

    <h3>Upload File</h3>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="hidden" name="path" value="{path}">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>


    <h3>Create Folder</h3>
    <form action="/create_folder" method="post">
        <input type="hidden" name="path" value="{path}">
        <input type="text" name="folder_name">
        <input type="submit" value="Create">
    </form>


    <h3>Files</h3>
    <ul>
    {file_list}
    </ul>

    </body>
    </html>
    """


@app.post("/upload")
async def upload(file: UploadFile = File(...), path: str = Form("")):

    dir_path = safe_path(path)

    os.makedirs(dir_path, exist_ok=True)

    file_path = os.path.join(dir_path, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return RedirectResponse(url=f"/?path={path}", status_code=303)


@app.get("/download")
def download(path: str):

    file_path = safe_path(path)

    if not os.path.exists(file_path):
        raise HTTPException(404)

    return FileResponse(file_path)


@app.post("/create_folder")
def create_folder(folder_name: str = Form(...), path: str = Form("")):

    dir_path = safe_path(path)

    new_folder = os.path.join(dir_path, folder_name)

    os.makedirs(new_folder, exist_ok=True)

    return RedirectResponse(url=f"/?path={path}", status_code=303)


@app.get("/delete_file")
def delete_file(path: str):

    file_path = safe_path(path)

    if os.path.exists(file_path):
        os.remove(file_path)

    parent = os.path.dirname(path)

    return RedirectResponse(url=f"/?path={parent}", status_code=303)


@app.get("/delete_folder")
def delete_folder(path: str):

    dir_path = safe_path(path)

    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)

    parent = os.path.dirname(path)

    return RedirectResponse(url=f"/?path={parent}", status_code=303)
