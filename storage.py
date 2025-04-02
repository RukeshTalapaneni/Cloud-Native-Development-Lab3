from google.cloud import storage
import time
import json

storage_client = storage.Client()

def get_list_of_files(bucket_name):
    """Lists all the blobs in the bucket."""
    print("\n")
    print("get_list_of_files: "+bucket_name)
    allowed_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')

    blobs = storage_client.list_blobs(bucket_name)
    print(blobs)
    files = []
    for blob in blobs:
        print(f"blob::::::: {blob}")
        if blob.name and blob.name.lower().endswith(allowed_extensions):
            image = blob.name
            unique_name = image.split('.')[0]
            json_data = download_file(bucket_name,unique_name)
            json_data = json.loads(json_data)
            print(f"json:::::::: {json_data['title']} ::desc {json_data['description']}")
            if json_data:
                files.append( {
                'image': image,
                'title': json_data['title'],
                'description': json_data['description'],
            })

    return json.dumps(files, indent=3)

def upload_file(bucket_name, file):
    """Send file to bucket."""
    print("\n")
    print("upload_file: "+bucket_name+"/"+file.filename)

    filename = f"{int(time.time())}_{file.filename}"
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)
    blob.upload_from_file(file, content_type=file.content_type)
    
    return [blob.public_url, filename]

def upload_json(bucket_name, file_name, content):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_string(json.dumps(content), content_type="application/json")

def download_file(bucket_name, file_name):
    """ Retrieve an object from a bucket and saves locally"""  
    print("\n")
    print("download_file: "+bucket_name+"/"+file_name)
    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(file_name)
    json_content = blob.download_as_text()
    return json.loads(json_content)

def getfile(imagename, bucket_name):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(imagename)
    file_data = blob.download_as_bytes()
    return file_data