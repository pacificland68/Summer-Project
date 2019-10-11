from __future__ import division
from requests_html import HTMLSession
from django.http import HttpResponse
import json
import ssl
from bs4 import BeautifulSoup
import json
import csv
import sys
import os
import re
from urllib.request import urlopen
# from requests import get
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken

from ..models import  Property, Save, recommend
import pymysql
import csv
import types 
import datetime
from sklearn.externals import joblib
import math
import random
import locale

def getUrl(request):
    ssl._create_default_https_context = ssl._create_unverified_context
    session = HTMLSession()
    url = request.GET.get('url', None)
    # url = 'https://property.adzuna.co.uk/land/ad/1109200382?se=RoBAGnLFSPK44igGu1hGJw&utm_medium=api&utm_source=786524e3&v=3DD598B759BA66A1E689EB250E5E96B77F01CB35'
    r = session.get(url)
    # soup = BeautifulSoup(r.html.links)
    # jsonD = json.dumps(r.html.text)
    # jsonL = json.loads(jsonD)
    
        
    return HttpResponse(r.html.links)
    
    # return(requests.request(method='GET', url=url, headers=headers))

def getCR(request, value):
    path = os.path.dirname(__file__)
    county = ""
    region = ""
    csv_file = open(path+'/uk_towns_and_counties.csv','rt')
    data_dict = csv.DictReader(csv_file)
    for row in data_dict:
        if row['town'] == value:
            county = row['county']
    
    csv_file = open(path+'/uk-counties-to-regions.csv','rt')
    data_dict = csv.DictReader(csv_file)
    for row in data_dict:
        if row['County'] == county:
            region = row['Region']
    
    return HttpResponse(county+","+region)

def getImg(request):
    ssl._create_default_https_context = ssl._create_unverified_context
    # session = HTMLSession()
    url = request.GET.get('p', None)
    # r = session.get(url)
    # jsonD = json.dumps(r.html.text)
    # r = session.get("https://www.zoopla.co.uk/for-sale/details/photos/"+id)
    # sel = '#main-content > div.ui-layout > div.dp-grid-wrapper > div.dp-gallery-wrapper > div > div > ul > li.dp-gallery__list-item.dp-gallery__list-item--active > a > img'
    # results = r.html.find(sel)
    # soup = BeautifulSoup(r.html.text, 'html.parser')
    # items = soup.find_all('img')
    # strstr(r.html.text,sStr)  

    html = urlopen(url)
    page = html.read()
    soup = BeautifulSoup(page, "html.parser")
    imglist = soup.find_all('img', {'class': 'dp-gallery__image'})  #发现html中带img标签的数据，输出格式为<img xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx，存入集合
    lenth = len(imglist)  #计算集合的个数
    collection = ''
    for i in range(lenth):
        collection += imglist[i].attrs['src']+';'

    # Soup = BeautifulSoup(r.html.text, 'lxml')
    # images = Soup.findAll('img')
    # all_a = Soup.find('img', class_='dp-gallery__image')

    return HttpResponse(collection)

@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """
    
    serializer = UserSerializer(request.auth)
    return Response(serializer.data)


class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """
 
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def save_user(request):
    username = request.GET.get('username', 'none')
    request.session['username']=username

    h1=request.session.get('username', 'none')
    return HttpResponse(h1)

def get_user(request):
    # h1=request.session.get('username')
    session = HTMLSession()
    h2=request.session.get('username', 'nonee')
    return HttpResponse(h2)

def signout_user(request):
    del request.session['username']
    return HttpResponse('ok')

def insert_properties(request):
    ssl._create_default_https_context = ssl._create_unverified_context
    t = 1

    while(t<50):
        html = urlopen('http://api.zoopla.co.uk/api/v1/property_listings.xml?area=southampton&api_key=2s676u9633nt8yea6rqmuxha&page_size=100&page_number='+str(t)+'&listing_status=sale')
        page = html.read()
        soup = BeautifulSoup(page, "html.parser")
        listing_id = soup.find_all('listing_id')
        post_town = soup.find_all('post_town') 
        outcode = soup.find_all('outcode')
        property_type = soup.find_all('property_type')
        first_published_date = soup.find_all('first_published_date')
        last_published_date = soup.find_all('last_published_date')
        num_bathrooms = soup.find_all('num_bathrooms')
        num_bedrooms = soup.find_all('num_bedrooms')
        num_floors = soup.find_all('num_floors')
        num_recepts = soup.find_all('num_recepts')
        price = soup.find_all('price')
        total = soup.find_all('result_count')

        for i in range(0, len(listing_id)):
            tt=0
            if property_type[i].get_text() == "Terraced house":
                tt=0
            elif property_type[i].get_text() == "End terrace house":
                tt=1
            elif property_type[i].get_text() == "Semi-detached house":
                tt=2
            elif property_type[i].get_text() == "Detached house":
                tt=3
            elif property_type[i].get_text() == "Mews house":
                tt=4
            elif property_type[i].get_text() == "Flat":
                tt=5
            elif property_type[i].get_text() == "Maisonette":
                tt=6
            elif property_type[i].get_text() == "Detached bungalow":
                tt=7
            elif property_type[i].get_text() == "Town house":
                tt=8
            elif property_type[i].get_text() == "Cottage":
                tt=9
            elif property_type[i].get_text() == "Farm/Barn":
                tt=10
            elif property_type[i].get_text() == "Mobile/static":
                tt=11
            elif property_type[i].get_text() == "Land":
                tt=12
            elif property_type[i].get_text() == "Studio":
                tt=13
            elif property_type[i].get_text() == "Block of flats":
                tt=14
            elif property_type[i].get_text() == "Office":
                tt=15

            p = Property(listing_id=listing_id[i].get_text(),
                        post_town=post_town[i].get_text(),
                        district=outcode[i].get_text().replace('SO', ''),
                        property_type=tt,
                        sector='sale',
                        # first_published_date_year=first_published_date[i].get_text()[0:4],
                        # first_published_date_month=first_published_date[i].get_text()[5:7],
                        # first_published_date_day=first_published_date[i].get_text()[8:10],
                        last_published_date_year=last_published_date[i].get_text()[0:4],
                        last_published_date_month=last_published_date[i].get_text()[5:7],
                        last_published_date_day=last_published_date[i].get_text()[8:10],
                        num_bathrooms=num_bathrooms[i].get_text(),
                        num_bedrooms=num_bedrooms[i].get_text(),
                        num_floors=num_floors[i].get_text(),
                        num_recepts=num_recepts[i].get_text(),
                        price=price[i].get_text()
                        )
            p.save()

        if t == round(int(total[0].get_text())/100):
            break
        t += 1


    t = 1

    while(t<50):
        html = urlopen('http://api.zoopla.co.uk/api/v1/property_listings.xml?area=southampton&api_key=2s676u9633nt8yea6rqmuxha&page_size=100&page_number='+str(t)+'&listing_status=rent')
        page = html.read()
        soup = BeautifulSoup(page, "html.parser")
        listing_id = soup.find_all('listing_id')
        post_town = soup.find_all('post_town') 
        outcode = soup.find_all('outcode')
        property_type = soup.find_all('property_type')
        first_published_date = soup.find_all('first_published_date')
        last_published_date = soup.find_all('last_published_date')
        num_bathrooms = soup.find_all('num_bathrooms')
        num_bedrooms = soup.find_all('num_bedrooms')
        num_floors = soup.find_all('num_floors')
        num_recepts = soup.find_all('num_recepts')
        price = soup.find_all('price')
        total = soup.find_all('result_count')

        for i in range(0, len(listing_id)):
            tt=0
            if property_type[i].get_text() == "Terraced house":
                tt=0
            elif property_type[i].get_text() == "End terrace house":
                tt=1
            elif property_type[i].get_text() == "Semi-detached house":
                tt=2
            elif property_type[i].get_text() == "Detached house":
                tt=3
            elif property_type[i].get_text() == "Mews house":
                tt=4
            elif property_type[i].get_text() == "Flat":
                tt=5
            elif property_type[i].get_text() == "Maisonette":
                tt=6
            elif property_type[i].get_text() == "Detached bungalow":
                tt=7
            elif property_type[i].get_text() == "Town house":
                tt=8
            elif property_type[i].get_text() == "Cottage":
                tt=9
            elif property_type[i].get_text() == "Farm/Barn":
                tt=10
            elif property_type[i].get_text() == "Mobile/static":
                tt=11
            elif property_type[i].get_text() == "Land":
                tt=12
            elif property_type[i].get_text() == "Studio":
                tt=13
            elif property_type[i].get_text() == "Block of flats":
                tt=14
            elif property_type[i].get_text() == "Office":
                tt=15

            p = Property(listing_id=listing_id[i].get_text(),
                        post_town=post_town[i].get_text(),
                        district=outcode[i].get_text().replace('SO', ''),
                        property_type=tt,
                        sector='rent',
                        # first_published_date_year=first_published_date[i].get_text()[0:4],
                        # first_published_date_month=first_published_date[i].get_text()[5:7],
                        # first_published_date_day=first_published_date[i].get_text()[8:10],
                        last_published_date_year=last_published_date[i].get_text()[0:4],
                        last_published_date_month=last_published_date[i].get_text()[5:7],
                        last_published_date_day=last_published_date[i].get_text()[8:10],
                        num_bathrooms=num_bathrooms[i].get_text(),
                        num_bedrooms=num_bedrooms[i].get_text(),
                        num_floors=num_floors[i].get_text(),
                        num_recepts=num_recepts[i].get_text(),
                        price=price[i].get_text()
                        )
            p.save()

        if t == round(int(total[0].get_text())/100):
            break
        t += 1
    

    return HttpResponse('ok')

def save(request):
    ssl._create_default_https_context = ssl._create_unverified_context

    username = request.GET.get('username', None)
    listing_id = request.GET.get('listing_id', None)

    html = urlopen('http://api.zoopla.co.uk/api/v1/property_listings.xml?api_key=2s676u9633nt8yea6rqmuxha&listing_id='+listing_id)
    page = html.read()
    soup = BeautifulSoup(page, "html.parser")
    listing_id = soup.find_all('listing_id')
    property_type = soup.find_all('property_type')
    post_town = soup.find_all('post_town') 
    outcode = soup.find_all('outcode')
    first_published_date = soup.find_all('first_published_date')
    last_published_date = soup.find_all('last_published_date')
    num_bathrooms = soup.find_all('num_bathrooms')
    num_bedrooms = soup.find_all('num_bedrooms')
    num_floors = soup.find_all('num_floors')
    num_recepts = soup.find_all('num_recepts')
    price = soup.find_all('price')
    total = soup.find_all('result_count')

    tt=0
    if property_type[0].get_text() == "Terraced":
        tt=0
    elif property_type[0].get_text() == "End of terrace":
        tt=1
    elif property_type[0].get_text() == "Semi-detached":
        tt=2
    elif property_type[0].get_text() == "Detached":
        tt=3
    elif property_type[0].get_text() == "Mews house":
        tt=4
    elif property_type[0].get_text() == "Flat":
        tt=5
    elif property_type[0].get_text() == "Maisonette":
        tt=6
    elif property_type[0].get_text() == "Bungalow":
        tt=7
    elif property_type[0].get_text() == "Town house":
        tt=8
    elif property_type[0].get_text() == "Cottage":
        tt=9
    elif property_type[0].get_text() == "Farm/Barn":
        tt=10
    elif property_type[0].get_text() == "Mobile/static":
        tt=11
    elif property_type[0].get_text() == "Land":
        tt=12
    elif property_type[0].get_text() == "Studio":
        tt=13
    elif property_type[0].get_text() == "Block of flats":
        tt=14
    elif property_type[0].get_text() == "Office":
        tt=15

    p = Save(
        username=username,
        listing_id=listing_id[0].get_text(),
        outcode=outcode[0].get_text().replace('SO', ''),
        property_type=tt,
        first_published_date_year=first_published_date[0].get_text()[0:4],
        first_published_date_month=first_published_date[0].get_text()[5:7],
        first_published_date_day=first_published_date[0].get_text()[8:10],
        last_published_date_year=last_published_date[0].get_text()[0:4],
        last_published_date_month=last_published_date[0].get_text()[5:7],
        last_published_date_day=last_published_date[0].get_text()[8:10],
        num_bathrooms=num_bathrooms[0].get_text(),
        num_bedrooms=num_bedrooms[0].get_text(),
        num_floors=num_floors[0].get_text(),
        num_recepts=num_recepts[0].get_text(),
        price=price[0].get_text()
    )
    p.save()
    return HttpResponse('ok')

def check_save(request):
    username = request.GET.get('username', None)
    listing_id = request.GET.get('listing_id', None)

    check=''
    cart = Save.objects.filter(username=username, listing_id=listing_id)
    if len(cart)>0:
        check='y'
    else:
        check='n'
    return HttpResponse(check)

def delete_save(request):
    username = request.GET.get('username', None)
    listing_id = request.GET.get('listing_id', None)

    cart = Save.objects.filter(username=username, listing_id=listing_id)
    cart.delete()

    return HttpResponse('ok')

def cosine(request):
    username = request.GET.get('username', None)
    cart = Save.objects.filter(username=username)

    result=[]
    oringle=[]
    final = []
    suit=set()
    recommend_content=''
    for data in cart:
        path = os.path.dirname(__file__)
        csv_file = open(path+'/cosine.csv','rt')
        data_dict = csv.DictReader(csv_file)
        for row in data_dict:
            result.append(row[data.listing_id])
        # quick_sort(result, 0, len(result)-1)
        for d in range(len(result)):
            if float(result[d]) < 1 and float(result[d]) > 0.999999519:
                suit.add(d)
                if len(suit) == 10:
                    break
                # final.append(result[d])
                # path = os.path.dirname(__file__)
                # csvv = open(path+'/cosine.csv','rt')
                # da = csv.DictReader(csvv)
                # inn=-1
                # for r in da:
                #     inn += 1
                #     if r[data.listing_id]==result[d]:
                #         suit.add(inn)
            

    for s in suit:
        recommend_content += str(s)+','

    rec = recommend.objects.filter(username=username)
    rec.delete()

    rec = recommend.objects.filter(username=username)
    if len(rec)>0:
        rec[0].recommend = recommend_content
        rec[0].save()
    else:
        p = recommend(
            username=username,
            recommend=recommend_content
        )    
        p.save()
    
    return HttpResponse(suit)

def show_recommend(request):
    username = request.GET.get('username', None)

    # get array of listing_id from result2.csv file
    path = os.path.dirname(__file__)
    csv_file = open(path+'/results2.csv','rt')
    data_dict = csv.DictReader(csv_file)
    result = []
    results = ''
    d=''
    for row in data_dict:
        result.append(row['listing_id'])

    # get index of recommend records from database
    cart = recommend.objects.filter(username=username)
    r = cart[0].recommend.split(',')
    for i in range(len(r)):
        if(r[i] != ''):
            results += result[int(r[i])] + ','
        # results.append(result[int(r[i])])


    return HttpResponse(results)

def show_random_recommend(request):
    path = os.path.dirname(__file__)
    csv_file = open(path+'/results2.csv','rt')
    data_dict = csv.DictReader(csv_file)
    result = []
    suit=''
    results = ''
    d=''
    for row in data_dict:
        result.append(row['listing_id'])
    for i in range(10):
        r = random.randint(0,2000)
        suit += result[r]+','
    return HttpResponse(suit)

def quick_sort(array, left, right):
    if left <= right:
        return
    low = left
    high = right
    key = array[low]
    while left > right:
        while left > right and array[right] < key:
            right -= 1
        array[left] = array[right]
        while left > right and array[left] >= key:
            left += 1
        array[right] = array[left]
    array[right] = key
    quick_sort(array, low, left - 1)
    quick_sort(array, left + 1, high)

def adz1(request):
    ssl._create_default_https_context = ssl._create_unverified_context
    # location1 = request.GET.get('location1', None)
    # location2 = request.GET.get('location2', None)
    # location3 = request.GET.get('location3', None)
    url = request.GET.get('urll', None)

    # url = 'https://api.adzuna.com:443/v1/api/property/gb/search/1?app_id=786524e3&app_key=79b1b0c7d58ba6229d66f1611190550c&location0=UK&location1='+location1+'&location2='+location2+'&location3='+location3+'&category=to-rent&results_per_page=50'
    html = urlopen(url)
    page = html.read()

    return HttpResponse(page)

def adz2(request):
    ssl._create_default_https_context = ssl._create_unverified_context
    index = request.GET.get('index', None)
    location1 = request.GET.get('location1', None)
    location2 = request.GET.get('location2', None)
    location3 = request.GET.get('location3', None)

    url = 'https://api.adzuna.com:443/v1/api/property/gb/search/'+index+'?app_id=786524e3&app_key=79b1b0c7d58ba6229d66f1611190550c&location0=UK&location1='+location1+'&location2='+location2+'&location3='+location3+'&category=to-rent&results_per_page=50'
    html = urlopen(url)

    return HttpResponse(html)

def prediction(request):
    path = os.path.dirname(__file__)
    ssl._create_default_https_context = ssl._create_unverified_context
    postcode = request.GET.get('postcode', None)
    typee = request.GET.get('typee', None)
    old = request.GET.get('old', None)
    duration = request.GET.get('duration', None)

    #devide postcode
    district=postcode[2:4]
    sector=postcode[5:6]
    u1=ord(postcode[6:7])-64
    u2=ord(postcode[7:8])-64

    t=datetime.date.today().strftime('%y%m%d') #180201
    # day=(t%10000)%100
    # month=(t%10000)/100
    # year=t/10000
    # day=t[4:6]
    day1=1
    day2=30
    month=t[2:4]
    year=t[0:2]

    #prediction
    rfc2 = joblib.load(path+'/rfc2.pkl')
    result1 = rfc2.predict([[int(day1),int(month),int(year),int(district),int(sector),int(u1),int(u2),int(str(typee)),int(str(old)),int(str(duration))]])
    result2 = rfc2.predict([[int(day2),int(month),int(year),int(district),int(sector),int(u1),int(u2),int(str(typee)),int(str(old)),int(str(duration))]])
    resultt = 0
    for i in range(1,31):
        resultt += rfc2.predict([[int(i),int(month),int(year),int(district),int(sector),int(u1),int(u2),int(str(typee)),int(str(old)),int(str(duration))]])
    resultt = resultt/30
    result = str(math.expm1(result1))+','+str(math.expm1(result2))+','+str(math.expm1(resultt))
    return HttpResponse(result)

def estimate(request):
    path = os.path.dirname(__file__)
    ssl._create_default_https_context = ssl._create_unverified_context
    postcode = request.GET.get('postcode', None)
    typee = request.GET.get('typee', None)
    bedroom = request.GET.get('bedroom', None)
    bathroom = request.GET.get('bathroom', None)
    floor = request.GET.get('floor', None)
    reception = request.GET.get('reception', None)

    #devide postcode
    district=postcode[2:4]
    # sector=postcode[5:6]
    # u1=ord(postcode[6:7])-64
    # u2=ord(postcode[7:8])-64

    t=datetime.date.today().strftime('%y%m%d') #180201
    # day=(t%10000)%100
    # month=(t%10000)/100
    # year=t/10000
    day=t[4:6]
    # day1=1
    # day2=30
    month=t[2:4]
    year=t[0:2]

    #prediction
    #sale
    sale = joblib.load(path+'/rfc_sale.pkl')
    sale1 = sale.predict([[int(district),int(str(typee)),int(day),int(month),int(year),int(bathroom),int(bedroom),int(floor),int(reception)]])
    # sale2 = sale.predict([[int(district),int(str(typee)),int(day2),int(month),int(year),int(bathroom),int(bedroom),int(floor),int(reception)]])
    sale2 = 0
    r_s = 0
    # for i in range(1,31):
    #     r_s += sale.predict([[int(district),int(str(typee)),int(i),int(month),int(year),int(bathroom),int(bedroom),int(floor),int(reception)]])
    # r_s = r_s/30

    #rent
    # rent = joblib.load(path+'/rfc_rent.pkl')
    # rent1 = rent.predict([[int(district),int(str(typee)),int(day1),int(month),int(year),int(bathroom),int(bedroom),int(floor),int(reception)]])
    # rent2 = rent.predict([[int(district),int(str(typee)),int(day2),int(month),int(year),int(bathroom),int(bedroom),int(floor),int(reception)]])
    r_r = 0
    # for i in range(1,31):
    #     r_r += rent.predict([[int(district),int(str(typee)),int(i),int(month),int(year),int(bathroom),int(bedroom),int(floor),int(reception)]])
    # r_r = r_r/30

    min_s=0
    max_s=0
    min_r=0
    max_r=0
    # if sale1 > sale2:
    #     min_s=sale2
    #     max_s=sale1
    # else:
    #     min_s=sale1
    #     max_s=sale2
    # if rent1 > rent2:
    #     min_r=rent2
    #     max_r=rent1
    # else:
    #     min_r=rent1
    #     max_r=rent2

    result = str(math.expm1(min_s))+','+str(math.expm1(max_s))+','+str(math.expm1(min_r))+','+str(math.expm1(max_r))+','+str(math.expm1(sale1))+','+str(math.expm1(r_r))
    return HttpResponse(result)

def barchart(request):
    postcode = request.GET.get('postcode', None)
    path = os.path.dirname(__file__)
    d=[]
    p=[]
    result=[]
    for i in range(1):
        csv_file = open(path+'/ppd_data21.csv','rt')
        data_dict = csv.DictReader(csv_file)
        data=[0,0,0,0,0,0,0]
        price=[0,0,0,0,0,0,0]
        r1=0
        r2=0
        r3=0
        r4=0
        r5=0
        r6=0
        r7=0
        for row in data_dict:
            if row['District'] == postcode and row['Year'] == '2019':
                if row['Month'] == '1':
                    data[0] += 1
                    r1 += int(row['Price'])
                elif row['Month'] == '2':
                    data[1] += 1
                    r2 += int(row['Price'])
                elif row['Month'] == '3':
                    data[2] += 1
                    r3 += int(row['Price'])
                elif row['Month'] == '4':
                    data[3] += 1
                    r4 += int(row['Price'])
                elif row['Month'] == '5':
                    data[4] += 1
                    r5 += int(row['Price'])
                elif row['Month'] == '6':
                    data[5] += 1
                    r6 += int(row['Price'])
                elif row['Month'] == '7':
                    data[6] += 1
                    r7 += int(row['Price'])
        d.append(data)
        price[0] = r1/data[0]
        price[1] = r2/data[1]
        price[2] = r3/data[2]
        price[3] = r4/data[3]
        price[4] = r5/data[4]
        price[5] = r6/data[5]
        price[6] = r7/data[6]
        p.append(price)
    j={'d':d, 'p':p}
    result.append(j)

    return HttpResponse(json.dumps(result), content_type="application/json")

def pyramidd(request):
    postcode = request.GET.get('postcode', None)
    price = request.GET.get('price', None)
    district=postcode[2:4]
    path = os.path.dirname(__file__)
    d=[]
    result=[]
    csv_file = open(path+'/Estimate_sale.csv','rt')
    data_dict = csv.DictReader(csv_file)
    data=[0,0,0,0,0]
    max = 0
    min = 0
    if district == '19':
        max = 1200000
        min = 99950
    elif district == '16':
        max = 1200000
        min = 100000
    elif district == '30':
        max = 925000
        min = 100000
    elif district == '17':
        max = 900000
        min = 100000
    elif district == '15':
        max = 830000
        min = 99950
    elif district == '14':
        max = 780000
        min = 110000
    elif district == '18':
        max = 650000
        min = 90000
    elif district == '30':
        max = 400000
        min = 100000

    for row in data_dict:
        if row['district'] == district:
            if float(row['price'])-min > float(max-min)*0.8:
                data[0] += 1
            elif float(row['price'])-min < float(max-min)*0.8 and float(row['price']) > float(max-min)*0.6:
                data[1] += 1
            elif float(row['price'])-min < float(max-min)*0.6 and float(row['price']) > float(max-min)*0.4:
                data[2] += 1
            elif float(row['price'])-min < float(max-min)*0.4 and float(row['price']) > float(max-min)*0.2:
                data[3] += 1
            elif float(row['price'])-min < float(max-min)*0.2:
                data[4] += 1
    # d.append(data)
    

    color=['#F9E79F', '#A3E4D7', '#FF0000', '#D7BDE2', '#E6B0AA']
    if float(price) > float(max-min)*0.8:
        color=['#FF0000','#F9E79F','#A3E4D7','#D7BDE2','#E6B0AA']
    elif float(price) < float(max-min)*0.8 and float(price) > float(max-min)*0.6:
        color=['#FF0000','#F9E79F','#A3E4D7','#D7BDE2','#E6B0AA']
    elif float(price) < float(max-min)*0.6 and float(price) > float(max-min)*0.4:
        color=['#F9E79F','#A3E4D7','#FF0000','#D7BDE2','#E6B0AA']
    elif float(price) < float(max-min)*0.4 and float(price) > float(max-min)*0.2:
        color=['#F9E79F', '#A3E4D7', '#D7BDE2', '#FF0000','#E6B0AA']
    elif float(price) < float(max-min)*0.2:
        color=['#F9E79F', '#A3E4D7', '#D7BDE2', '#E6B0AA', '#FF0000']
    #{"action": "Website visits", "value": 5654}

    locale.setlocale(locale.LC_ALL, '')
    for i in range(5):
        if int(price) > int(max*(1-(0.2*(i+1)))) and int(price) < int(max*(1-(0.2*i))):
            j={"name": str('£'+locale.format("%.2f", int(max*(1-(0.2*(i+1)))), 1))+'-'+str('£'+locale.format("%.2f", int(max*(1-(0.2*i))), 1)),"value":data[i], "label": str(i+1), "check": "Your property is here"}
        else:
            j={"name": str('£'+locale.format("%.2f", int(max*(1-(0.2*(i+1)))), 1))+'-'+str('£'+locale.format("%.2f", int(max*(1-(0.2*i))), 1)),"value":data[i], "label": str(i+1), "check": ""}
        result.append(j)
    
    return HttpResponse(json.dumps(result), content_type="application/json")

def getsave(request):
    ssl._create_default_https_context = ssl._create_unverified_context
    username = request.GET.get('username', None)

    cart = Save.objects.filter(username=username).values()
    # data_json = simplejson.dumps(data_dict)
    cart = list(cart)
    # my_json_string = json.dumps(cart)
    # j={"results":cart}
    # data = []
    # data.append(my_json_string)
    return HttpResponse(json.dumps(cart), content_type="application/json")

def ValuesQuerySetToDict(vqs):
    return [item for item in vqs]