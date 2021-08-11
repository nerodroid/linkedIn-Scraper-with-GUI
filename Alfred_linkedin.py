
from linkedin_api import Linkedin
import urllib
# Authenticate using any Linkedin account credentials


import pandas as pd
from time import sleep
import csv

#last_page=False
def start(username,passwd):
    api = Linkedin(username, passwd)
    session = api.client.session
    return api,session

def get_companyname(x):
    x=urllib.parse.unquote(x)
    x=x.split('?')[0]
    if x.count('/') > 4:
        return x.split('/')[4]
    else:
        return x.split('/')[-1]

def get_employees(dt,curr,comp,comp_id,loc,title,outputfile2):

    sleep(5)

    #curl = "https://www.linkedin.com/voyager/api/search/cluster?count=49&guides=List(v-%%3EPEOPLE,facetCurrentCompany-%%3E%s,facetGeoRegion-%%3E%s%%3A0)&keywords=%s&origin=FACETED_SEARCH&q=guided&start=%i" % (comp_id,loc,title,curr)
    #try:
    #    res = session.get(curl)
    #    dt=res.json()
    #except:
    #    #print(c['Linkedin Company ID'])
    #    print(comp_id)
    #    return ""
    dt=dt
    try:
        data = dt["elements"][0]
        data = data["elements"]
    except:
        data=[]
    if len(data) != 49:
        last_page = True
    eoutput=[]
    for p in data:

        sprofile=p['hitInfo']['com.linkedin.voyager.search.SearchProfile']
        
        miniprofile=sprofile['miniProfile']
        pname=miniprofile['firstName']+" "+miniprofile['lastName']
        if not pname:
            pname="Linkedin Member"
        ptitle=sprofile['miniProfile']['occupation']
        ploc=sprofile['location']
        
        purn=sprofile['id']
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
            "Company Name":comp,
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
    


def main_func(username,passwd,loc,title,lurl):
    from linkedin_api import Linkedin
    #api = Linkedin(username, passwd)
    outputfile1 = "linkedinoutput1.csv"
    outputfile2 = "linkedinoutput2.csv"
    
    opcolumns2 = ['conmpany_id',
                  'Name',
                  'Profile URN',
                  'Public ID',
                  'Profile URL',
                  'Job Title',
                  'Location',
                  'Picture URL']
    opcolumns1 = [#'company_id',
                  'Icon',
                  'Name',
                  'Link',
                  'Industry',
                  'Location',
                  'Followers',
                  'Abount Us',
                  'Website',
                  'Headquarters',
                  'Year Founded',
                  'Company Type',
                  'Company Size',
                  'Specialities',
                  'Office Locations',
                  'Employees Count',
                  'Linkedin Company ID']
    with open(outputfile1, 'w', newline="") as op1:
        writer = csv.writer(op1)
        writer.writerow(opcolumns1)
        print (opcolumns1)
    op1.close()

    with open(outputfile2, 'w', newline="") as op2:
        writer = csv.writer(op2)
        writer.writerow(opcolumns2)
    op2.close()
    output = []

    api,session = start(username,passwd)
    for c in lurl.split('\n'):
        last_page=False
        comp=get_companyname(c)

        sleep(2)
        

        try:
            data=api.get_company(comp.strip())
        except:
            req_data={
            #"company_id":cid,
            "Icon":"",
            "Name":comp,
            "Link":"https://www.linkedin.com/company/"+comp,
            "Industry":"",
            "Location":"",
            "Followers":"",
            "Abount Us":"",
            "Website":"",
            "Headquarters":"",
            "Year Founded":"",
            "Company Type":"",
            "Company Size":"",
            "Specialities":"",
            "Office Locations":"",
            "Employees Count":"",
            "Linkedin Company ID":""
            }
            output.append(req_data)
            with open(outputfile1, 'a',newline="",encoding="utf-8") as op1:
                writer = csv.writer(op1)
                writer.writerow(list(req_data.values()))
            op1.close()
            print(req_data)
            continue
        try:
            logo1url=data['logo']['image']['com.linkedin.common.VectorImage']['rootUrl']
            logo2url=data['logo']['image']['com.linkedin.common.VectorImage']['artifacts'][-1]['fileIdentifyingUrlPathSegment']
            logourl=logo1url+logo2url
        except:
            logourl=""
        name=data['name']
        link=data['url']
        compid=link.split('/')[-1]
        try:
            industry=data['companyIndustries'][0]['localizedName']
        except:
            industry=""
        try:
            _location=data['confirmedLocations'][0]
            location=_location['geographicArea']+","+_location['city']+","+_location['country']
        except:
            location=""
        try:
            followers=data['followingInfo']['followerCount']
        except:
            followers=""
        try:
            aboutus=data['description']
        except:
            aboutus=""
        try:
            website=data['companyPageUrl']
        except:
            website=""
        try:
            _headquarter=data['headquarter']
            try:
                garea=_headquarter['geographicArea']
            except:
                garea=""
            headquarter=garea+","+_headquarter['city']+_headquarter['country']
        except:
            headquarter=""
        try:
            yrfounded=data['foundedOn']['year']
        except:
            yrfounded=""
        try:
            companytype=data['companyType']['localizedName']
        except:
            companytype=""
        try:
            companysize=data['staffCountRange']['start']
            try:
                end=data['staffCountRange']['end']
            except:
                end=""
            if end:
                companysize=str(companysize)+" - "+str(end)
            else:
                companysize=str(companysize)+" +"
        except:
            companysize=""
        try:
            specialities=", ".join(data['specialities'])
        except:
            specialities=""
        try:
            _loc=data['confirmedLocations'][0]
            try:
                pcode=str(_loc["postalCode"])
            except:
                pcode=""
            try:
                line1=_loc['line1']
            except:
                line1=""
            try:
                garea=_loc["geographicArea"]
            except:
                garea=""
            officelocation=line1+", "+_loc["city"]+", "+garea+", "+pcode+", "+_loc["country"]
        except:
            officelocation=""
        empcount=data['staffCount']

        req_data={
            #"company_id":cid,
            "Icon":logourl,
            "Name":name,
            "Link":link,
            "Industry":industry,
            "Location":location,
            "Followers":followers,
            "Abount Us":aboutus,
            "Website":website,
            "Headquarters":headquarter,
            "Year Founded":yrfounded,
            "Company Type":companytype,
            "Company Size":companysize,
            "Specialities":specialities,
            "Office Locations":officelocation,
            "Employees Count":empcount,
            "Linkedin Company ID":compid
        }
        print(req_data)
        with open(outputfile1, 'a',newline="",encoding="utf-8") as op1:
            writer = csv.writer(op1)
            writer.writerow(list(req_data.values()))
        op1.close()
        output.append(req_data)
        sleep(2)
        
        try:
            comp_id=req_data["Linkedin Company ID"]

        except:
            continue
        curr = 0
        last_page=False
        while not last_page:

            curl = "https://www.linkedin.com/voyager/api/search/cluster?count=49&guides=List(v-%%3EPEOPLE,facetCurrentCompany-%%3E%s,facetGeoRegion-%%3E%s%%3A0)&keywords=%s&origin=FACETED_SEARCH&q=guided&start=%i" % (comp_id,loc,title,curr)
            try:
                res = session.get(curl)
                dt=res.json()
            except:
                #print(c['Linkedin Company ID'])
                #print(comp_id)
                dt=""
            
            try:
                data = dt["elements"][0]
                data = data["elements"]
            except:
                data=[]
            if len(data) != 49:
                last_page = True
            output2=get_employees(dt,curr,name,comp_id,loc,title,outputfile2)

            curr = curr + 49

