import cv2
from datetime import timedelta
from flask import Flask, jsonify, redirect, render_template, request, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static/'
app.config['UPLOAD_IMAGE_FOLDER'] = 'upload_images/'
app.config['RESULT_IMAGE_FOLDER'] = 'result_images/'

# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)

img_count = 0
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'JPEG','JPG', 'PNG', 'bmp'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1] in ALLOWED_EXTENSIONS

def process(img):
    return img

@app.route('/error')
def process_error():
   return jsonify({"error": 1001, "msg": "上传的文件类型错误，需上传以png、PNG、jpg、JPG、bmp结尾的图片文件"})

@app.route('/home', methods=['POST', 'GET'])
def home():
    global img_count
    if request.method == 'POST':
        f = request.files['img']
        #处理错误文件格式
        if not (f and allowed_file(f.filename)):
            return redirect(url_for('process_error'))
        
        #保存上传的图片 
        base_path = os.path.dirname(__file__) 
        upload_fold = os.path.join(base_path, app.config['STATIC_FOLDER'], app.config['UPLOAD_IMAGE_FOLDER'])
        if not os.path.exists(upload_fold):
            os.makedirs(upload_fold)
        upload_path = os.path.join(upload_fold, secure_filename(str(img_count)+'.jpg'))
        f.save(upload_path)
        img_count += 1
        
        #处理图片
        img = cv2.imread(upload_path)
        result_text = 'test'
        
        #保存处理后的图片
        result_fold = os.path.join(base_path, app.config['STATIC_FOLDER'], app.config['RESULT_IMAGE_FOLDER'])
        if not os.path.exists(result_fold):
            os.makedirs(result_fold)
        cv2.imwrite(os.path.join(result_fold, str(img_count-1)+'_result.jpg'), img)
        
        return render_template('result.html', result_text=result_text, result_file=app.config['RESULT_IMAGE_FOLDER']+str(img_count-1)+'_result.jpg')
    return render_template('home.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=11007, debug=True)
