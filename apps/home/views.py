# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import base64
import io
import string

import cv2
import numpy as np
import pymongo
import pytesseract
import json
from bson import ObjectId
from django import template
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from easyocr import Reader
from PIL import Image
from ultralytics import YOLO
from django.core.files import File
from io import BytesIO
from django.views import View
# from googletrans import Translator
from datetime import date
from django.shortcuts import render
from datetime import date
from docx import Document
import fitz
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from django.utils.html import escape
import datetime
from reportlab.lib.pagesizes import A4


def my_view(request):
    kmsdata = [{file_id: 0, name: 'FGA11', file_status: "Work in Progress", updatingDate: "03/20/2024", transition: "root" }]

    context = {
        'kmsdata': kmsdata
    }

    return render(request, 'kms.html', context)
# import shortuuid

import uuid




# client = pymongo.MongoClient("mongodb://mongodb_new_ocr:27017/")
# client = pymongo.MongoClient("mongodb://localhost:27017/")
# # print("mongodcliet",client)
# db = client["userdata"]
# db_forms = client["forms"]
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse

def download_pdf(request):
    attach = request.GET.get('attach', 'Unknown File')
    linkFile = request.GET.get('linkfile', 'Unknown')
    approved = request.GET.get('approved', 'Unknown')
    customerName = request.GET.get('customerName', 'Unknown')
    birth = request.GET.get('birth', 'Unknown')
    panNumber = request.GET.get('panNumber', 'Unknown')
    adharNumber = request.GET.get('adharNumber', 'Unknown')
    shortDescription = request.GET.get('shortDescription', 'Unknown')
    detailsItem = request.GET.get('detailsitem', 'Unknown')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="description.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    wrap_width = 440

    lines = []
    line = ""
    for word in shortDescription.split():
        if p.stringWidth(line + " " + word) < wrap_width:
            line += " " + word
        else:
            lines.append(line.lstrip())
            line = word
    if line:
        lines.append(line.lstrip())

    details_lines = []
    line = ""
    for word in detailsItem.split():
        if p.stringWidth(line + " " + word) < wrap_width:
            line += " " + word
        else:
            details_lines.append(line.lstrip())
            line = word
    if line:
        details_lines.append(line.lstrip())

    p.setFont("Helvetica", 12)
    p.setKeywords(['data', 'description', 'metadata'])
    p.setCreator('Your Application Name')
    p.drawString(80, 720, 'Attach: ' + attach)
    p.drawString(80, 690, 'LinkFile: ' + linkFile)
    p.drawString(80, 660, 'Approved: ' + approved)
    p.drawString(80, 630, 'Customer Name: ' + customerName)
    p.drawString(80, 600, 'Birthday: ' + birth)
    p.drawString(80, 570, 'PanNumber: ' + panNumber)
    p.drawString(80, 540, 'AdharNumber: ' + adharNumber)
    p.drawString(80, 510, 'Short Description:')
    
    y_position = 490
    for line in lines:
        p.drawString(80, y_position, line)
        y_position -= 20

    y_position -= 20
    p.drawString(80, y_position, 'Details:')
    
    y_position -= 20
    for line in details_lines:
        p.drawString(80, y_position, line)
        y_position -= 20

    p.save()
    
    return response


# from django.shortcuts import render
# from django.http import JsonResponse
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['userdata']
collection = db['userCollection']

def mongodb_test(request):
    return render(request, 'home/mongodb_test.html')

# @login_required(login_url="/login/")
def save_to_mongo(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        status = data.get('status')
        fileName = data.get('file_name')
        print('status', status)
        result = collection.insert_one({'status': status, 'file_name': fileName})
        if result:
            return JsonResponse({"message": "Success"})
        else:
            return JsonResponse({"message" : "Failed"})
    
    return render(request, 'home/mongodb_test.html')

def send_custom_data(request):
    # print('d')
    if request.method == 'POST':
        data = json.loads(request.body)
        print('data', data)
        status = data.get('status')
        fileName = data.get('file_name')
        fileId = data.get('file_id')  
        assign =  data.get('assigned')
        label =  data.get('labeled')
        createDate =  data.get('create_date')
        createBy =  data.get('create_by')
        modifiedDate =  data.get('modified_date')
        modifiedBy = data.get( 'modified_by')
        priority = data.get( 'priorityed')
        system =  data.get('systemed')
        approvedBy = data.get('approved_by')
        currentTime =  data.get('current_time')
        target_date =  data.get('target_date')
        editable_data = data.get('editableData')
        print('status', status)
        result = collection.insert_one({'status': status, 
            'file_name': fileName,
            'fileId':fileId,  
            'assign': assign,
            'label': label,
            'createDate': createDate,
            'createBy': createBy,
            'modifiedDate': modifiedDate,
            'modifiedBy': modifiedBy,
            'priority': priority,
            'system': system,
            'approvedBy':approvedBy,
            'approvedDate': currentTime,
            'target_date': target_date,
            'editable_data': editable_data
        })
        if result:
            return JsonResponse({"message": "Success"})
        else:
            return JsonResponse({"message" : "Failed"})
# @login_required(login_url="/login/")
def find_in_mongo(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('content')
        print('content', text)
        result = collection.find_one({'text': text})
        if result:
            return HttpResponse('success')
        else:
            return HttpResponse('Failed')
def unique_id(request):
    unique_id = str(uuid.uuid4())[:10]  # Generate a unique ID and take the first 8 characters
    print ('unique_id', unique_id)
    if request.method == 'GET':
        return HttpResponse(unique_id)
    return render(request, 'home/index.html', {'unique_id': unique_id})

from .detect import get_data
from .mongo_update import insert_record


from .models import Employee

# def extract_metadata(request):
#     print('extra_meta_data')
#     if request.method == 'POST':
#         uploaded_file = request.FILES['file']
#         file_type = uploaded_file.name.split('.')[-1].lower()

#         if file_type == 'docx':
#             doc = Document(uploaded_file)
#             created_date = doc.core_properties.created
#             author = doc.core_properties.author
#         elif file_type == 'pdf':
#             pdf_document = fitz.open(uploaded_file)
#             metadata = pdf_document.metadata
#             created_date = metadata.get('creationDate')
#             author = metadata.get('author')
#         elif file_type in ['jpg', 'jpeg', 'png']:
#             image = Image.open(uploaded_file)
#             created_date = image.info.get('DateTimeOriginal')
#             author = image.info.get('Artist')
#         else:
#             created_date = date.today()
#             author = 'root'

#         return JsonResponse({'created_date': created_date, 'author': author})
    
#     return render(request, 'home/index.html')

def get_data(request):
    data = list(collection.find({}))
    print(data)
    return JsonResponse(data, safe=False)

@login_required(login_url="/login/")
def add_employee(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        role = request.POST.get('role')
        Employee.objects.create(name=name, role=role)
    
    employees = Employee.objects.all()
    return render(request, 'userManagement.html', {'employees': employees})
# ------- Admin --------------------
# @login_required(login_url="/login/")
# def get_todays_date(request):
#     today = date.today()
#     return render(request, 'index.html', {'today': today})

# @login_required(login_url="/login/")
# def kmsDataView(request):
#     kmsdata = [{'file_id': 0, 'name': 'FGA11', 'file_status': "Work in Progress", 'updatingDate': "03/20/2024", 'transition': "root" }]

#     context = {
#         'kmsdata': kmsdata
#     }

#     return render(request, 'kms.html', context)

@login_required(login_url="/login/")
def index(request):
    context = {"segment": "index"}

    html_template = loader.get_template("home/index.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split("/")[-1]

        if load_template == "admin":
            return HttpResponseRedirect(reverse("admin:index"))
        context["segment"] = load_template

        html_template = loader.get_template("home/" + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        html_template = loader.get_template("home/page-404.html")
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template("home/page-500.html")
        return HttpResponse(html_template.render(context, request))


# ----------------------- Adhaar / Pan -------------------------

@login_required(login_url="/login/")
def imagetoText(request):
    if request.method == "POST" and "image" in request.FILES.keys():
        image = request.FILES["image"]
        image = Image.open(image)
        # image = cv2.imread(image)
        imageBytes = io.BytesIO()
        image.save(imageBytes, format="JPEG")
        bytes = imageBytes.getvalue()
        # bytes = imageBytes.encode()
        # bytes = str(bytes)
        bytes = base64.b64encode(bytes).decode()
        # bytes = base64.b64encode(imageBytes.getvalue())
        arrImg = np.array(image)

        frame = cv2.cvtColor(arrImg, cv2.COLOR_RGB2BGR)

        model = YOLO("/code/apps/home/weights/best.pt")
        threshold = 0.35
        class_name_dict = {3: "adhaar_no", 1: "dob", 2: "gender", 0: "user_name"}
        print("YOLO done")

        reader = Reader(
            ["en"], gpu=False, model_storage_directory="ocr_models"
        )  # load languages for easyocr.

        data = get_data(frame, class_name_dict, model, threshold, reader)
        data["adhaar_no"] = data["adhaar_no"].replace(" ", "")
        u_name = data["user_name"]
        u_name = " ".join([string.capwords(i) for i in u_name.split(" ")])
        data["user_name"] = u_name
        print(data)
        print("done")

        # text = pytesseract.image_to_string(image)
        return JsonResponse({"status": "success", "text": data, "bytes": str(bytes)})
        # return render(
        #     request,
        #     "imagetotext.html",
        #     {"status": "success", "text": data, "bytes": str(bytes)},
        # )
    return render(request, "home/index.html")


@login_required(login_url="/login/")
def imagetoTextPan(request):
    if request.method == "POST" and "imagepan" in request.FILES:
        image = request.FILES["imagepan"]
        image = Image.open(image)
        imageBytes = io.BytesIO()
        image.save(imageBytes, format="JPEG")
        bytes = imageBytes.getvalue()
        # bytes = imageBytes.encode()
        # bytes = str(bytes)
        bytes = base64.b64encode(bytes).decode()
        # bytes = base64.b64encode(imageBytes.getvalue())
        arrImg = np.array(image)
        frame = cv2.cvtColor(arrImg, cv2.COLOR_RGB2BGR)

        model = YOLO("/code/apps/home/weights/pan.pt")
        threshold = 0.35
        class_name_dict = {3: "pan_no", 1: "fathers_name", 2: "dob", 0: "user_name"}

        reader = Reader(
            ["en"], gpu=False, model_storage_directory="ocr_models"
        )  # load languages for easyocr.

        data = get_data(frame, class_name_dict, model, threshold, reader)
        f_name = data["fathers_name"]
        f_name = " ".join([string.capwords(i) for i in f_name.split(" ")])
        data["fathers_name"] = f_name
        u_name = data["user_name"]
        u_name = " ".join([string.capwords(i) for i in u_name.split(" ")])
        data["user_name"] = u_name
        # print(data)

        # text = pytesseract.image_to_string(image)
        return JsonResponse({"status": "success", "text": data, "bytes": str(bytes)})
        # return render(
        #     request,
        #     "imagetotext.html",
        #     {"status": "success", "text": data, "bytes": str(bytes)},
        # )
    return render(request, "home/index.html")


@login_required(login_url="/login/")
def insert_into_database(request):
    if request.method == "POST":
        print(len(request.POST["id"]))
        if len(request.POST["id"]) == 0:
            occ_adhar = []
            occ_pan = []
            if len(request.POST["adharNo"]) > 0:
                occ = list(db.userdata.find({"adhaar_no": request.POST["adharNo"]}))
                if len(occ) > 0:
                    occ_adhar += occ
            # print(list(db.userdata.find({})))
            if len(request.POST["panNo"]) > 0:
                occ = list(db.userdata.find({"pan_no": request.POST["panNo"]}))
                if len(occ) > 0:
                    occ_pan += occ
            ret = []
            print(occ_adhar)
            if len(occ_adhar) > 0:
                ret.append("adhar exists")
            if len(occ_pan) > 0:
                ret.append("pan exists")

            # print(ret)
            if len(ret) > 0:
                ret_val = 1
            else:
                ret_val = 0
            print(ret_val)
            if ret_val == 0:
                user_name = request.POST["name"]
                adhaar_no = request.POST["adharNo"]
                gender = request.POST["gender"]
                dob = request.POST["dob"]
                pan_no = request.POST["panNo"]
                fathers_name = request.POST["fatherName"]
                data1 = {
                    "user_name": user_name.strip(),
                    "adhaar_no": adhaar_no.strip().replace(" ", ""),
                    "gender": gender.strip(),
                    "dob": dob.strip(),
                    "pan_no": pan_no.strip(),
                    "fathers_name": fathers_name.strip(),
                }
                ret_dict = insert_record(data1, db)
                ret_dict["_id"] = str(ret_dict["_id"])
            else:
                ret_dict = {}
                print(ret_dict)
            return JsonResponse(
                {"status": "success", "vals": ret_dict, "ret_val": ret_val}
            )
        elif len(request.POST["id"]) > 0:
            doc_id = request.POST["id"]
            print(doc_id)
            req = {k: v[0] for k, v in dict(request.POST).items()}
            del req["id"]
            del req["csrfmiddlewaretoken"]
            inp = {
                "user_name": req["name"].strip(),
                "adhaar_no": req["adharNo"].strip().replace(" ", ""),
                "gender": req["gender"].strip(),
                "dob": req["dob"].strip(),
                "pan_no": req["panNo"].strip(),
                "fathers_name": req["fatherName"].strip(),
            }
            db.userdata.update_one({"_id": ObjectId(doc_id)}, {"$set": inp})
            print(req)
            req["_id"] = doc_id
            return JsonResponse({"status": "success", "ret_val": 0, "vals": req})

    # return ret_dict


@login_required(login_url="/login/")
def verify_exists(request):
    if request.method == "POST":
        occ_adhar = []
        occ_pan = []
        if len(request.POST["adharNo"]) > 0:
            occ = list(db.userdata.find({"adhaar_no": request.POST["adharNo"]}))
            if len(occ) > 0:
                occ_adhar += occ
        # print(list(db.userdata.find({})))
        print(request.POST.keys())
        if len(request.POST["panNo"]) > 0:
            print(request.POST["panNo"])
            occ = list(db.userdata.find({"pan_no": request.POST["panNo"]}))
            if len(occ) > 0:
                occ_pan += occ
        ret = []
        print(occ_adhar)
        ret_val = 0
        if len(occ_adhar) > 0:
            ret.append("adhar exists")
            ret_val = 1
        if len(occ_pan) > 0:
            ret_val = 1
            ret.append("pan exists")

        # print(ret)
        # if len(ret) > 0:
        #     ret_val = 1
        # else:
        # ret_val = 0
        print(ret_val)
        return JsonResponse({"status": "success", "ret_val": ret_val})


@login_required(login_url="/login/")
def search_database(request):
    if request.method == "POST":
        print(request)
        if request.POST["searchCard"] == "adhar":
            print("adhar")
            occ = list(
                db.userdata.find({"adhaar_no": request.POST["searchDoc"].strip()})
            )
            if len(occ) > 0:
                occ = occ[0]
                occ["_id"] = str(occ["_id"])
            else:
                occ = {}

        elif request.POST["searchCard"] == "pan":
            occ = list(db.userdata.find({"pan_no": request.POST["searchDoc"].strip()}))
            if len(occ) > 0:
                occ = occ[0]
                occ["_id"] = str(occ["_id"])
            else:
                occ = {}
        print(occ)
        return JsonResponse({"status": "success", "userinfo": occ})


@login_required(login_url="/login/")
def update_database(request):
    if request.method == "POST":
        doc_id = request.POST["_id"]
        req = request.POST
        del req["_id"]
        print("updatedb")
        print(request.POST)

        return JsonResponse({"status": "success"})


@login_required(login_url="/login/")
def delete_record(request):
    if request.method == "POST":
        db.userdata.delete_one({"_id": ObjectId(request.POST["recid"])})
        return render(request, "home/index.html")


# class AdharAutocomplete(View):
    # def get(self, request):
@login_required(login_url='/login/')
def AdharAutocomplete(request):
    if request.method == 'GET':
        query_data = request.GET.get('term', '').upper()
        card_type = request.GET.get('cardType', '')
        print(card_type)
        query_string = {'$regex' : f'^{query_data}'}
        if card_type == "adhar":
            data_list = list(db.userdata.find({"adhaar_no": query_string},{"adhaar_no": 1}))
            data_list = data_list[:min(10, len(data_list))]
            result = [data['adhaar_no'] for data in data_list]
            print(result)
        elif card_type == "pan":
            data_list = list(db.userdata.find({"pan_no": query_string},{"pan_no": 1}))
            data_list = data_list[:min(10, len(data_list))]
            result = [data['pan_no'] for data in data_list]
        else:
            result = []
        # print(query_data)
        return JsonResponse(result, safe=False)

# --------------------- Selection OCR -----------------------

@login_required(login_url="/login/")
def select_text(request):
    if request.method == "POST":
        if "imgBytes" in request.POST.keys():
            decoded_data = base64.b64decode(request.POST["imgBytes"])
            # img_file = open('/media/image.jpeg', 'wb')
            # img_file.write(decoded_data)
            # img_file.close() 
            # f_name = default_storage.save("image.jpg", decoded_data)
            im = Image.open(BytesIO(decoded_data))
            im_width, im_height = im.size
            # h_ratio = im_width/ 4032
            # w_ratio = im_height / 3024
            # arrImg = np.array(im) 
            # print(arrImg.shape)
            left = int(request.POST["thb_left"])
            right = int(request.POST["thb_right"])
            top = int(request.POST["thb_top"])
            bottom = int(request.POST["thb_bottom"])
            # print(left, top, right, bottom)
            # left = round(left * w_ratio) - 10
            # right = round(right * w_ratio) + 10
            # top = round(top * h_ratio) - 10
            # bottom = round(bottom*h_ratio) + 10
            im.save("/test.jpg")
            im_crop = im.crop((left, top, right, bottom))    
            imageBytes = io.BytesIO()
            im_crop.save(imageBytes, format="JPEG")
            arrImg = np.array(im_crop)
            bytes = imageBytes.getvalue()
            bytes = base64.b64encode(bytes).decode()

            cropped_bytes = str(bytes) 
            reader = Reader(
                ["en"], gpu=False, model_storage_directory="ocr_models"
            )  
            frame = cv2.cvtColor(arrImg, cv2.COLOR_RGB2BGR)
            result = reader.readtext(frame, detail=0, paragraph=True, y_ths = -0.1)
            # print([r[0][:-2] for r in result])
            r_string = " ".join([r[1] for r in result])
            # for r in result:
                # print(r[1])
            return render(request, "home/select-text.html", {"status": True, "bytes": cropped_bytes , "result" : r_string})
        return render(request, "home/select-text.html", {"status": False})
    return render(request, "home/select-text.html", {"status": False})


@login_required(login_url="/login/")
def image_upload(request):
    if request.method == "POST":
        image = request.FILES["image"]
        image = Image.open(image)
        imageBytes = io.BytesIO()
        image.save(imageBytes, format="JPEG")
        bytes = imageBytes.getvalue()
        # bytes = imageBytes.encode()
        # bytes = str(bytes)
        bytes = base64.b64encode(bytes).decode()
        # bytes = base64.b64encode(imageBytes.getvalue())
        arrImg = np.array(image)
        frame = cv2.cvtColor(arrImg, cv2.COLOR_RGB2BGR)
        return render(
            request, "home/select-text.html", {"status": True, "bytes": str(bytes), "width": image.size[0], "height": image.size[1]}
        )

# @login_required(login_url="/login/")
# def select_ocr(request):
#     if request.method == "POST":
#         decoded_data = base64.b64decode(request.POST["imgBytes"])
#         arrImg = np.array(decoded_data)
#         return JsonResponse({"status": "success"})

@login_required(login_url="/login/")
def select_cropper(request):
    if 'recent_images' in request.session:
        recent_images = request.session['recent_images']
        print(request.session['recent_images'])
        return render(request, "home/select-text-cropper.html", {"recent_images": request.session['recent_images']})
    # else:
    #     recent_images = []
    return render(request, "home/select-text-cropper.html")
    recent_images = []
    return render(request, "home/select-text-cropper.html")



@login_required(login_url="/login/")
def select_ocr(request):
    if request.method == "POST":
        img64 = request.POST["imageBytes"].split(",")[1]
        lang = request.POST.get('selectedLanguage')
        print('Selected Language:', lang)
        if lang == 'en':
            if 'origImageBytes' in request.POST:
                print('origImageBytes')
                # print(f"Orig image: {request.POST['origImageBytes']}")
                if 'recent_images' in request.session:
                    request.session['recent_images'] += [request.POST['origImageBytes'],]
                    # print(len(request.session["recent_images"]))
                    if len(request.session["recent_images"]) > 5:
                        request.session["recent_images"] = request.session['recent_images'][:-1]
                    # print(len(request.session["recent_images"]))
                else:
                    request.session['recent_images'] = [request.POST['origImageBytes'],]
            # print(request.session['recent_images'])
            decoded_data = base64.b64decode(img64)
            im = Image.open(BytesIO(decoded_data))
            arrImg = np.array(im)
            reader = Reader(
            [lang], gpu=False, model_storage_directory="ocr_models"
                )  
            frame = cv2.cvtColor(arrImg, cv2.COLOR_RGB2BGR)
            # frame = Image.fromarray(arrImg)
            result = reader.readtext(frame, paragraph=True, y_ths = -0.1)
            # print(result)
            r_string = " ".join([r[1] for r in result])
        else :
            print('other language-------------------------->', lang)
            decoded_data = base64.b64decode(img64)
            language = ''
            if lang == 'hi':
                 language = 'hin'
                 print(language)
            else:
                if lang == 'mr':
                    language = "mar"
                    print(language)
            # Convert the decoded image data to a PIL Image object
            img = Image.open(BytesIO(decoded_data))

            # Use pytesseract to extract text from the image
            extracted_text = pytesseract.image_to_string(img, lang=language)
            r_string = extracted_text
        # r_string = result[0]
        return render(request, "home/select-ocr-done.html", {"imageBytes": img64, "result": r_string})

@login_required(login_url="/login/")
def pdf_ocr(request):
    if request.method == "POST":
        lang = request.POST.get('lang')
        print('pdf------------>')

    if 'file' in request.FILES:
        file = request.FILES['file']
        
        if file.name.endswith('.pdf'):
            pdf_data = file.read()
            pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
            
            extracted_text = ""
            
            language = lang
            if lang == 'hi':
                 language = 'hin'
                 print(language)
            else:
                if lang == 'mr':
                    language = "mar"
                    print(language)
            for page_num in range(pdf_document.page_count):
                page = pdf_document.load_page(page_num)
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                
                extracted_text += pytesseract.image_to_string(img, lang=language) + "\n"
        else:
            img = Image.open(file)
            extracted_text = pytesseract.image_to_string(img, lang=lang)
        
        return render(request, "home/select-ocr-pdf-done.html", {"result": extracted_text})
    
    # return JsonResponse({'error': 'No file found'}, status=400)

@login_required(login_url="/login/")
def KMS(request):
    return render(request, "home/kms.html")

@login_required(login_url="/login/")
def MyQueue(request):
    return render(request, "home/myQueue.html")

@login_required(login_url="/tool/")
def tool(request):
    return render(request, "home/tools.html")

@login_required(login_url="/login/")
def UserManagement(request):
    return render(request, "home/userManagement.html")

@login_required(login_url="/login/")
def Dashboard(request):
    data = list(collection.find({}))
    for item in data:
        if '_id' in item:
            item['_id'] = str(item['_id'])
    json_data = json.dumps(data)
    # print (data)
    return render(request, 'home/dashboard.html', {'json_data': json_data})
    # return render(request, "home/dashboard.html")

# ------------------ Speech to Text -----------------------
@login_required(login_url="/login/")
def speech_to_text(request):
    return render(request, "home/speech-to-text.html")

@login_required(login_url="/login/")
def speech_to_text_new(request):
    return render(request, "home/speech-to-text-new.html")


@login_required(login_url="/login/")
def mahadiscomreg(request):
    if request.method == "POST":
        data = {}
        data["consumerType"] = request.POST["consumerType"]
        data["consumerNo"] = request.POST["consumerNo"]
        data["bu"] = request.POST["bu"]
        data["actType"] = request.POST["actType"]
        data["firstName"] = request.POST["firstName"]
        data["middleName"] = request.POST["middleName"]
        data["lastName"] = request.POST["lastName"]
        data["adhaar_no"] = request.POST["uid"]
        data["gender"] = request.POST["gender"]
        data["maritalStatus"] = request.POST["maritalStatus"]
        data["dob"] = request.POST["dob"]
        data["securityQuestion"] = request.POST["securityQuestion"]
        data["securityAnswer"] = request.POST["securityAnswer"]
        data["address1"] = request.POST["address1"]
        data["address2"] = request.POST["address2"]
        data["city"] = request.POST["city"]
        data["state"] = request.POST["state"]
        data["country"] = request.POST["country"]
        data["pincode"] = request.POST["pincode"]
        db_forms["mahadiscom"].insert_one(data)

    return render(request, 'home/mahadiscomreg.html')


@login_required(login_url="/login/")
def fir(request):
    if request.method == "POST":
        data = {}
        data["dist"] = request.POST["dist"]
        data["ps"]  =  request.POST["ps"]
        data["year"] = request.POST["year"]
        data["firNo"] = request.POST["firNo"]
        data["firDate"] = request.POST["firDate"]
        data["act1"] = request.POST["act1"]
        data["act2"] = request.POST["act2"]
        data["act3"] = request.POST["act3"]
        data["act4"] = request.POST["act4"]
        data["sections1"] = request.POST["sections1"]
        data["sections2"] = request.POST["sections2"]
        data["sections3"] = request.POST["sections3"]
        data["address"] = request.POST["address"]
        data["day"] = request.POST["day"]
        data["dateFrom"] = request.POST["dateFrom"]
        data["dateTo"] = request.POST["dateTo"]
        data["timePeriod"] = request.POST["timePeriod"]
        data["timeFrom"] = request.POST["timeFrom"]
        data["timeTo"] = request.POST["timeTo"]
        data["recvDate"] = request.POST["recvDate"]
        data["recvTime"] = request.POST['recvTime']
        data["refNo"] = request.POST['refNo']
        data["refTime"] = request.POST["refTime"]
        data["infoType"] = request.POST["infoType"]
        data["writtenOral"] = request.POST["writtenOral"]
        data["direction"] = request.POST["direction"]
        data["beatNo"] = request.POST["beatNo"]
        db_forms["fir"].insert_one(data)
    return render(request, 'home/firform.html')