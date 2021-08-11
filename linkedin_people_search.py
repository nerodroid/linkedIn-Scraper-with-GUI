
from linkedin_api import Linkedin

# Authenticate using any Linkedin account credentials


import pandas as pd
from time import sleep
import csv

last_page = False
def start(username,passwd):
    api = Linkedin(username, passwd)
    session = api.client.session
    return api,session

def get_companyname(x):
    x=x.split('?')[0]
    if x.count('/') > 4:
        return x.split('/')[4]
    else:
        return x.split('/')[-1]

def get_employees(session,curr,ind_id,loc,qstring,outputfile2,data):

    #global last_page
    #sleep(5)

    #curl = "https://www.linkedin.com/voyager/api/search/blended?count=49&filters=List(geoRegion-%3E{}%3A0,industry-%3E{},resultType-%3EPEOPLE)&keywords={}&origin=FACETED_SEARCH&q=all&queryContext=List(spellCorrectionEnabled-%3Etrue,relatedSearchesEnabled-%3Etrue,kcardTypes-%3EPROFILE%7CCOMPANY%7CJOB_TITLE)&start={}".format(loc,str(ind_id),qstring,str(curr)) #%(loc) #% (loc,qstring,curr)
    #try:
    #    res = session.get(curl)
    #    dt=res.json()
    #except:
    #    #print(c['Linkedin Company ID'])

    #   return ""

    #try:
    #    data = dt["elements"][0]
    #    data = data["elements"]
    #except:
    #    data=[]
    #if len(data) != 49:
    #    last_page = True

    eoutput=[]
    for p in data:

        sprofile=p['image']['attributes'][0]
        
        miniprofile=p['image']['attributes'][0]['miniProfile']
        pname=miniprofile['firstName']+" "+miniprofile['lastName']
        if not pname:
            pname="Linkedin Member"
        ptitle=sprofile['miniProfile']['occupation']
        #ploc=sprofile['location']
        ploc=loc
        #purn=sprofile['id']
        purn=miniprofile['entityUrn']
        publicid=miniprofile['publicIdentifier']
        if publicid != "UNKNOWN":
            profileurl="https://www.linkedin.com/in/"+publicid
        else:
            profileurl="https://www.linkedin.com/in/"+purn
        try:
            furl=miniprofile['picture']['com.linkedin.common.VectorImage']['artifacts'][0]['fileIdentifyingUrlPathSegment']

            rurl=miniprofile['picture']['com.linkedin.common.VectorImage']['rootUrl']
            purl=rurl+furl
        except:
            purl=""
        pdetails={
            #"conmpany_id":inp_id,

            "Name":pname,
            "Profile URN":purn,
            "Public ID":publicid,
            "Profile URL":profileurl,
            "Job Title":ptitle,
            "Location":ploc,
            "Picture URL":purl
        }
        print(pdetails)
        with open(outputfile2, 'a',newline="",encoding="utf-8") as op2:
            writer = csv.writer(op2)
            writer.writerow(list(pdetails.values()))
        op2.close()
        eoutput.append(pdetails)
    return eoutput
    


def main_func(username,passwd,loc,qstring,ind_id):
    from linkedin_api import Linkedin
    #api = Linkedin(username, passwd)

    outputfile2 = "linkedinsearchpeopleoutput2.csv"

    opcolumns2 = ['Name',
                  'Profile URN',
                  'Public ID',
                  'Profile URL',
                  'Job Title',
                  'Location',
                  'Picture URL']


    with open(outputfile2, 'w', newline="") as op2:
        writer = csv.writer(op2)
        writer.writerow(opcolumns2)
    op2.close()

    api,session = start(username,passwd)

    curr=0
    last_page=False
    while not last_page:
        curl = "https://www.linkedin.com/voyager/api/search/blended?count=49&filters=List(geoRegion-%3E{}%3A0,industry-%3E{},resultType-%3EPEOPLE)&keywords={}&origin=FACETED_SEARCH&q=all&queryContext=List(spellCorrectionEnabled-%3Etrue,relatedSearchesEnabled-%3Etrue,kcardTypes-%3EPROFILE%7CCOMPANY%7CJOB_TITLE)&start={}".format(loc,str(ind_id),qstring,str(curr)) #%(loc) #% (loc,qstring,curr)
        try:
            res = session.get(curl)
            dt=res.json()
        except:
            #print(c['Linkedin Company ID'])

            continue

        try:
            data = dt["elements"][0]
            data = data["elements"]
        except:
            data=[]
        if len(data) != 49:
            last_page = True
            
        output2=get_employees(session,curr,ind_id,loc,qstring,outputfile2,data)

        curr = curr + 49

