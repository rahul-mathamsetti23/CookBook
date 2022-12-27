from pymongo import MongoClient
from flask import Flask, render_template,request, make_response,g
import io
import  csv
from azure.storage.blob import BlockBlobService
from azure.storage.blob import PublicAccess
from azure.storage.blob import ContentSettings
from datetime import datetime


app=Flask(__name__)

block_blob_service = BlockBlobService(account_name='blobstorage12', account_key='n4+kY6GIWWlxNEkSprxx6HDj4Ba8ajBpL7qFxQe3b4lQ3uJwGHkWFoTW8btrJm3oBmM3u7IeLVSreR+JEhvH2A==')
block_blob_service.create_container('container1', public_access=PublicAccess.Container)
connection = MongoClient("mongodb://azuremongodb:WDxJD58w7vSWxET91ibthDP6pTSNzSRWHiLTChYPNHyr1TgcywtfWoFr9Ig0wBDTKk0WfGZNiDq1Oa2lw0P2uA==@azuremongodb.documents.azure.com:10255/?ss$

db = connection.Cooking.items

items = {}
@app.route("/", methods=["POST","GET"])
def start():
    return render_template("index.html")
@app.route("/uploadcsv", methods=["POST","GET"])  			## upload the csv file into the mongoDB
def uploadcsv():
    a=request.files['file']
    filename=a.filename
    csvnme=filename.split('.')
    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    print(stream)
    data = csv.reader(stream)
    
    generator = block_blob_service.list_blobs('container1')

    for blob in generator:
        print(blob.name)
        if blob.name==csvnme[0]:
            obj1= block_blob_service.make_blob_url('container1', blob.name, protocol='https')
            print(obj1)
	    line=1
    for i in data:
        if line==1:
            weightlist=i
            line=2
            continue
        elif line==2:
            ingred=i
            line=9
            continue
        else:
            category=i

    items = {"Author": "ADARSH"}
    count1 = 0
    count2=0
    ingredlist=''
    weights_list=''
    for ingredient in ingred:
        ingredlist = ingredlist+" "+ingred[i]
        count1=count1+1
    for weight in weightlist:
        weights_list=weights_list+" " +weightlist[j]
        count2=count2+1
    items['ingredients']=ingredlist
    items['weights']=weights_list
    items['url']=obj1
    items['name']=csvnme[0]
    items['category']=category[0]
    db.insert(items)
    return render_template("index.html")

@app.route("/view", methods=["POST","GET"])			## Viewing all the files if the If condition is false that is blank input.
def view():
    start=datetime.now()
    image_name=request.form['imgenme']
    url=[]
    ingred=[]
    weight=[]
    category=[]
    name=[]
    res=db.find()
    list=[]
    k=0
    for food in res :
        if image_name:
                list=food['ingredients'].split()
                for i in range(len(list)):
                        if list[i]==image_name:
                                url.append(food['url'])
                                ingred.append(food['ingredients'])
                                weight.append(food['weights'])
                                category.append(food['category'])
                                name.append(food['name'])
                
                if food['category']==image_name and k<10:
                        url.append(food['url'])
                        ingred.append(food['ingredients'])
                        weight.append(food['weights'])
                        category.append(food['category'])
                        name.append(food['name'])
                        k=k+1
	else:
                url.append(food['url'])
                ingred.append(food['ingredients'])
                weight.append(food['weights'])
                category.append(food['category'])
                name.append(food['name'])
        
    diff=datetime.now()-start   


    return render_template("image.html",diff=diff,url=url,ingred=ingred,weight=weight,category=category,name=name)

@app.route('/upload', methods=['POST'])				##uploading file into Container
def upload():
        f= request.files['file']
        file_name=f.filename
        name=file_name.split('.')
        f.save('home/adarsh/flaskapp/'+file_name)
        location ='home/adarsh/flaskapp/'+file_name
        block_blob_service.create_blob_from_path('container1',name[0],location,content_settings=ContentSettings(content_type='image/jpg'))
        return 'uploaded'

connection.close()


if __name__=='__main__':
    # app.run(host='0.0.0.0', port=int(8080), threaded=True, debug=True)
    app.run(debug=True)

