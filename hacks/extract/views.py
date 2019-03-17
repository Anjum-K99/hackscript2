from django.shortcuts import render,redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from . import pdf
from .forms import DocumentForm,CommentForm
import convertapi
from .models import Document
from rossum.extraction import ElisExtractionApi
from django.http import JsonResponse
import json
# Create your views here.

def home(request):
    if request.method == 'POST' and request.FILES:
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            tp=form
            form.save()
            #nam = str(form.Meta().model.document).split('/')[-1]
            #request.FILES['filename'].name
            name = request.FILES['document'].name  
            convertapi.api_secret = 'Yg8lKOH0wLJn8OeI'
            name = name.replace(' ','_')
            path = r'C:\Users\Anjum k\Desktop\hacks\media\documents\\'+ name
            result = convertapi.convert('pdf', { 'File':path })
            result.file.save(r'C:\Users\Anjum k\Desktop\hacks\media\pdf.pdf')
            context=extract_data()
            return render(request,'extract/home.html',{ 'form': form} ,context)
            return context
    else:
        form = DocumentForm()
    return render(request,'extract/home.html',{ "form": form }) 

def about(request):
    return render(request,'extract/about.html',{})

def contact(request):
    return render(request,'extract/contact.html',{})

def comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'extract/contact.html',{})
    else:
        form = CommentForm()
    return render(request,'extract/contact.html',{ "form": form }) 
#convertapi.api_secret = 'Yg8lKOH0wLJn8OeI'
#result = convertapi.convert('pdf', { 'File': r'C:\Users\Anjum k\Desktop\Hackscript\Samples\PO_3.gif' })

def extract_data():
    api = ElisExtractionApi("3KcQ3xHbELYV7kTt2FCPHRFCNySS762mfL47cD1AXxNwqWrsd5Z1TptvWOmtfkBF")
    extraction = api.extract(r'C:\Users\Anjum k\Desktop\hacks\media\pdf.pdf',r'C:\Users\Anjum k\Desktop\hacks\media\result.json')

    inp=json.load(open(r'C:\Users\Anjum k\Desktop\hacks\media\result.json','r'))
    my_dict={}
    t =""
    flag=0
    #a = inp.get("full_text").get("content")
    #print(a)
    for i in inp.get("full_text").get("content"):
        if(i.find("PO")!=-1 or (i.lower()).find("purchase order")!=-1):
            t = "PO"
            break
        else:
            flag+= 1
    if(flag>0 and t==""):
        t = "INVOICE"

    a=len(inp["fields"])
    my_dict["doctype"]=t
    for i in range(a):
        if (inp["fields"][i].get("title"))=="Supplier Name":
            my_dict["suppliercompany"]=inp["fields"][i].get("value")
        elif (inp["fields"][i].get("title"))=="Supplier Address":
            my_dict["supplieraddress"]=inp["fields"][i].get("value")
        elif (inp["fields"][i].get("title"))=="Recipient Name":
            my_dict["billto"]=inp["fields"][i].get("value")
        elif (inp["fields"][i].get("title"))=="Recipient Name":
            my_dict["shipto"]=inp["fields"][i].get("value")
        elif ((inp["fields"][i].get("title"))=="Order Number" or (inp["fields"][i].get("title"))=="Invoice Identifier"):
            my_dict["ordernum"]=inp["fields"][i].get("value")
        elif (inp["fields"][i].get("title"))=="Issue Date":
            my_dict["issuedate"]=inp["fields"][i].get("value")
        elif (inp["fields"][i].get("title"))=="Total Amount":
            my_dict["totalamount"]=inp["fields"][i].get("value")
        elif (inp["fields"][i].get("title"))=="Tax Total":
            my_dict["total tax"]=inp["fields"][i].get("value")
        elif (inp["fields"][i].get("title"))=="Terms":
            my_dict["terms"]=inp["fields"][i].get("value")
    print(my_dict)
    # data=json.dumps(my_dict)
    print(JsonResponse(my_dict, status=200))
    return JsonResponse(my_dict, status=200)
    #return my_dict