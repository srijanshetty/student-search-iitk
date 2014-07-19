#!/bin/python

import pprint
import requests
from BeautifulSoup import BeautifulSoup, Comment
import re

def getRecord(rollNo):
    roll = str(rollNo)
    req = requests.get('http://oa.cc.iitk.ac.in:8181/Oa/Jsp/OAServices/IITk_SrchRes.jsp?typ=stud&numtxt=' + roll + '&sbm=Y')
    soup = BeautifulSoup(req.text)
    record = {}

    record['roll'] = roll

    image = 'http://oa.cc.iitk.ac.in:8181/Oa/Jsp/Photo/' + roll + '_0.jpg'
    record['image'] = image

    data = soup.findChildren('p')
    name = data[0].text.split(':')[1]
    record['name'] = name

    if not name:
        return None

    program = data[1].text.split(':')[1]
    record['program'] = program

    dept = data[2].text.split(':')[1]
    record['department'] = dept

    room = data[3].text.split(':')[1]
    record['room'] = room

    email = data[4].text.split(':')[1]
    record['email'] = email

    bloodData = data[5].text.split('<b>')[0]
    blood = bloodData.split(':')[1]
    record['blood'] = blood

    categoryData = data[5].text.split('<b>')[1]
    category = re.findall(u'(?<=>).+?(?=<)', categoryData)[0]
    record['category'] = category

    genderData = data[6].text.split(':')
    gender = genderData[1][0]
    record['gender'] = gender

    country = genderData[2]
    record['country'] = country

    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    addressSoup = BeautifulSoup(comments[1])
    permanentAddressData = addressSoup.findAll('p')[1].text
    phonePos = permanentAddressData.index('Phone no:')
    mobilePos = permanentAddressData.index('Mobile no:')

    address  = permanentAddressData[19:phonePos]
    record['address'] = address

    phone = permanentAddressData[(phonePos + 9):mobilePos]
    record['phone'] = phone

    mobile = permanentAddressData[(mobilePos + 9):]
    record['mobile'] = mobile

    return record

def getRollNo(rollNo):
    roll = str(rollNo)
    req = requests.get('http://oa.cc.iitk.ac.in:8181/Oa/Jsp/OAServices/IITk_SrchRes.jsp?typ=stud&numtxt=' + roll + '&sbm=Y')
    soup = BeautifulSoup(req.text)

    image = 'http://oa.cc.iitk.ac.in:8181/Oa/Jsp/Photo/' + roll + '_0.jpg'
    print 'Image :: ' + image

    data = soup.findChildren('p')
    name = data[0].text.split(':')[1]
    print 'Name :: ' + name

    program = data[1].text.split(':')[1]
    print 'Program :: ' + program

    dept = data[2].text.split(':')[1]
    print 'Department :: ' + dept

    room = data[3].text.split(':')[1]
    print 'Room :: ' + room

    email = data[4].text.split(':')[1]
    print 'E-mail :: ' + email

    bloodData = data[5].text.split('<b>')[0]
    blood = bloodData.split(':')[1]
    print 'Blood :: ' + blood

    categoryData = data[5].text.split('<b>')[1]
    category = re.findall(u'(?<=>).+?(?=<)', categoryData)[0]
    print 'Category :: ' + category

    genderData = data[6].text.split(':')
    gender = genderData[1][0]
    print 'Gender :: ' + gender

    country = genderData[2]
    print 'Country :: ' + country

    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    addressSoup = BeautifulSoup(comments[1])
    permanentAddressData = addressSoup.findAll('p')[1].text
    phonePos = permanentAddressData.index('Phone no:')
    mobilePos = permanentAddressData.index('Mobile no:')

    address  = permanentAddressData[19:phonePos]
    print 'Permanent Address :: ' + address

    phone = permanentAddressData[(phonePos + 9):mobilePos]
    print 'Phone Number :: ' + phone

    mobile = permanentAddressData[(mobilePos + 9):]
    print 'Mobile Number :: ' + mobile

arrayOfRecords = []
for i in range(11000, 14000):
    arrayOfRecords.append(getRecord(i))

fixedArray = filter(None, arrayOfRecords)
pprint.pprint(fixedArray)

# import argparse
# parser = argparse.ArgumentParser()
# parser.add_argument('-r', '--roll', help="search by providing a roll no", type=int)
# args = parser.parse_args()
#
# if args.roll:
#     getRollNo(11728)
