import os
from flask import Flask, redirect, request, Response
from storage import get_list_of_files, upload_file, upload_json, download_file, getfile
from gemini import generate_image_description
import json
import io

bucket_name = os.environ.get("BUCKET_NAME")

app = Flask(__name__)

@app.route('/')
def index():
    index_html="""
    <body style="background-color: blue; color: white">
<form method="post" enctype="multipart/form-data" action="/upload" method="post">
  <div>
    <label for="file">Upload an image to generate the Title and Description using Gemini</label>
    <input type="file" id="file" name="form_file" accept="image/jpeg"/>
  </div>
  <div>
    <button>Upload</button>
  </div>
</form>"""    

    for file in json.loads(get_list_of_files(bucket_name)):
          index_html += f"""
<li style="list-style-type: upper-roman">
<div style="text-align: center">
    <h2 class="title-container">
      <b> Title : </b>  <span>{file['title']}</span>
    </h2>
    <div class="image-container">
        <img width="200" height="200" src="/images/{file['image']}" />
    </div>
    <div class="description-container">
      <b> Description : </b>  <span>{file['description']}</span>
    </div>
    </div>
</li><br>
</body>
"""

    return index_html

@app.route('/images/<imagename>')
def download_file_from_bucket(imagename):
    file_data = getfile(imagename, bucket_name)
    return Response(io.BytesIO(file_data), mimetype='image/jpeg')

@app.route('/upload', methods=["POST"])
def upload():
    if request.method == "POST":
        if "form_file" not in request.files:
            return "No file uploaded", 400

        file = request.files["form_file"]
        if file.filename == "":
            return "No selected file", 400

        # Upload the file and get its public URL
        print(f"Uploading::::: {type(file)}")
        upload_data = upload_file(bucket_name, file)
        json_filename = upload_data[1].split('.')[0]
        if len(upload_data) :
           print("chck:::::")
           text = generate_image_description("https://storage.cloud.google.com/"+bucket_name+"/"+upload_data[1])
           print(f"Generated description: {text}")
           if "title" in text:
               upload_json(bucket_name, json_filename, text)

        # file_url = upload_file(bucket_name, file)
        # return f"File uploaded successfully: <a href='{file_url}' target='_blank'>{file_url}</a>"

    return redirect("/")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
