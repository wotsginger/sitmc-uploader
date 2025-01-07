from flask import Flask, request, render_template, flash, redirect, url_for, jsonify
import os
import random
import string

app = Flask(__name__)
app.secret_key = ''

# 指定存储目录
IMAGE_UPLOAD_FOLDER = '/mnt/Images'
SCHEM_UPLOAD_FOLDER = '/mnt/schematics'
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png'}
ALLOWED_SCHEM_EXTENSIONS = {'schem', 'schematic'}

# 创建上传目录
os.makedirs(IMAGE_UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SCHEM_UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename, allowed_extensions):
    """检查文件扩展名是否被允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def generate_random_filename(extension, upload_folder):
    """生成唯一的随机文件名"""
    while True:
        random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        filename = f"{random_code}.{extension}"
        # 检查文件是否已存在
        if not os.path.exists(os.path.join(upload_folder, filename)):
            return filename


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 检查是否有文件上传
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        # 检查文件名
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        file_extension = file.filename.rsplit('.', 1)[1].lower()

        # 判断文件类型并保存
        if allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
            random_filename = generate_random_filename(file_extension, IMAGE_UPLOAD_FOLDER)
            file.save(os.path.join(IMAGE_UPLOAD_FOLDER, random_filename))
            flash('Image uploaded successfully!')
        elif allowed_file(file.filename, ALLOWED_SCHEM_EXTENSIONS):
            random_filename = generate_random_filename(file_extension, SCHEM_UPLOAD_FOLDER)
            file.save(os.path.join(SCHEM_UPLOAD_FOLDER, random_filename))
            flash('Schematic file uploaded successfully!')
        else:
            flash('Invalid file type')
            return redirect(request.url)

        # 返回生成的文件名
        return jsonify({"filename": random_filename})

    return render_template('upload.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=45000, debug=True)

