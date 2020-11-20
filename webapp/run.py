import cv2
from flask import Flask, jsonify, redirect, render_template, request, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_IMAGE_FOLDER'] = 'static/upload_images/'
app.config['RESULT_IMAGE_FOLDER'] = 'static/result_images/'

img_count = 0
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1] in ALLOWED_EXTENSIONS

@app.route('/error')
def process_error():
   return jsonify({"error": 1001, "msg": "上传的文件类型错误，需上传以png、PNG、jpg、JPG、bmp结尾的图片文件"})

@app.route('/home', methods=['POST', 'GET'])
def home():
    global img_count
    if request.methods == 'POST':
        f = request.files['img']
        #处理错误文件格式
        if not (f and allowed_file(f.filename)):
            return redirect(url_for('process_error'))
        
        #保存上传的图片 
        base_path = os.path.dirname(__file__) 
        upload_fold = base_path + app.config['UPLOAD_IMAGE_FOLDER']
        if not os.path.exists(upload_fold):
            os.makedirs(upload_fold)
        upload_path = os.path.join(upload_fold, secure_filename(str(img_count)+'.jpg'))
        f.save(upload_path)
        img_count += 1
        #处理图片

        #user_input = ''.join(beam_search(upload_path))

        # 使用Opencv转换一下图片格式和名称
        #img = text_image(upload_path, user_input)
        img = imread(upload_path, mode="RGB")
        result_text = '111'
        result_fold = base_path + app.config['RESULT_IMAGE_FOLDER']
        if not os.path.exists(result_fold):
            os.makedirs(result_fold)
        cv2.imwrite(os.path.join(result_fold, str(img_count-1)+'_result.jpg'), img)
        
        return render_template('result.html', result_text=result_text, result_file=result_fold+str(img_count-1)+'_result.jpg')
    return render_template('home.html')

if __name__ == '__main__':
    #app.run(debug = True)
    app.run('0.0.0.0', port=5002)