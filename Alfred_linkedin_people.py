from linkedin_api import Linkedin
import pandas as pd

import time,csv
import datetime

today=datetime.datetime.today()
data=pd.read_excel("people profile_SPECS.xlsx",sheet_name="Desired output",header=1)

req_fields=list(data.columns)
fin_output=[]

def start(username,passwd):
    api = Linkedin(username, passwd)
    session = api.client.session
    return api,session

def main_func(lids,username,passwd):
    with open("People_data.csv",'w',newline="") as f:
        writer = csv.writer(f)
        writer.writerow(req_fields)
    f.close()
    for lid in lids.split('\n'):
        output_dic={}
        #lid=row['LinkedIN ID']
        output_dic['LinkedIN ID']=lid
        #lurl=row['LinkedIN']
        output_dic['LinkedIN']="https://www.linkedin.com/in/"+str(lid)
        api,session=start(username,passwd)
        pdata=api.get_profile(public_id=lid)
        output_dic['First name']=pdata['firstName']
        output_dic['Last name']=pdata['lastName']
        output_dic['Full name']=output_dic['First name']+" "+output_dic['Last name']
        
        try:
            output_dic['Industry']=pdata['industryName']
        except:
            output_dic['Industries']=''
        try:
            output_dic['Title']=pdata['headline']
        except:
            output_dic['Title']=""
        output_dic['Location']=pdata['locationName']
        output_dic['Avatar']="https://www.linkedin.com/in/"+str(lid)+"/detail/photo"
        
        try:
            output_dic['Summary']=pdata['summary']
        except:
            output_dic['Summary']=""
        
        #### Contact Info ####
        
        cdata=api.get_profile_contact_info(lid)
        try:
            output_dic['Email']=cdata['email_address']
        except:
            output_dic['Email']
        try:
            websites=cdata['websites']
        except:
            websites=[]
        for i,website in enumerate(websites):
            output_dic['Website '+str(i+1)]=website['url']
        try:
            phones=cdata['phone_numbers']
        except:
            phones=[]
        for i,phone in enumerate(phones):
            output_dic['Phone '+str(i+1)]=phone['number']
            output_dic['Phone '+str(i+1)+' type']=phone['type']
        try:
            
            output_dic['Twitter']=' '.join(cdata['twitter'])
        except:
            output_dic['Twitter']=''
        try:
            messengers=cdata['ims']
        except:
            messengers=[]
        if not messengers:
            messengers=[]
        for i,messenger in enumerate(messengers):
            output_dic['Messenger '+str(i+1)]=messenger['id']
            output_dic['Messenger '+str(i+1)+" type"]=messenger['provider']
        
        try:
            birthday=str(cdata['birthdate']['day'])
        except:
            birthday=""
        try:
            birthmonth=str(cdata['birthDate']['month'])
        except:
            birthmonth= ""
        
            
        output_dic['Birthday']=birthday+"-"+birthmonth
            
        pview=session.get('https://www.linkedin.com/voyager/api/identity/profiles/{}/profileView'.format(str(lid)))
        p=pview.json()
        
        ###SCHOOLS###
        schools=p['educationView']['elements']

        for i,sc in enumerate(schools):

            try:
                scname=sc['schoolName'] 
            except:
                scname=sc['school']['schoolName']
            
           
            output_dic['Education '+str(i+1)]=scname
            try:
                grade=sc['grade']
                output_dic['Education Grade '+str(i+1)]=grade
            except:
                output_dic['Education Grade '+str(i+1)]=''
            try:
                degree=sc['degreeName']
                output_dic['Education Degree '+str(i+1)]=degree
            except:
                output_dic['Education Degree '+str(i+1)]=''
            try:
                desc=sc['description']
                output_dic['Education Description '+str(i+1)]=desc
            except:
                output_dic['Education Description '+str(i+1)]=''
            try:
                timeperiod=sc['timePeriod']
                output_dic['Education Start '+str(i+1)]=timeperiod['startDate']['year']
            except:
                output_dic['Education Start '+str(i+1)]=''
            try:
                timeperiod=sc['timePeriod']
                output_dic['Education End '+str(i+1)]=timeperiod['endDate']['year']
            except:
                output_dic['Education End '+str(i+1)]=''
            try:
                fos=sc['fieldOfStudy']
                output_dic['Education FOS '+str(i+1)]=fos
            except:
                output_dic['Education FOS '+str(i+1)]=''
                
        ### COMPANIES ###
        comps=p['positionGroupView']['elements']
        new_j=0
        for i,_comp in enumerate(comps):
            
            for j,comp in enumerate(_comp['positions']):
                
                output_dic['Organization '+str(new_j+1)]=comp['companyName']
                try:
                    output_dic['Organization Title '+str(new_j+1)]=comp['title']
                except:
                    output_dic['Organization Title '+str(new_j+1)]=''
                try:
                    try:
                        startmonth=str(comp['timePeriod']['startDate']['month'])
                    except:
                        startmonth=''
                    output_dic['Organization Start '+str(new_j+1)]=startmonth+"-"+str(comp['timePeriod']['startDate']['year'])
                except:
                    output_dic['Organization Start '+str(new_j+1)]=''
                try:
                    try:
                        endmonth=str(comp['timePeriod']['endDate']['month'])
                    except:
                        endmonth=''
                    output_dic['Organization End '+str(new_j+1)]=endmonth+"-"+str(comp['timePeriod']['endDate']['year'])
                except:
                    output_dic['Organization End '+str(new_j+1)]=''
                
                dur_time=comp['timePeriod']

                try:
                    start_mon=dur_time['startDate']['month']
                except:
                    start_mon=0
                try:
                    start_yr=dur_time['startDate']['year']
                except:
                    start_yr=''
                try:
                    end_mon=dur_time['endDate']['month']
                except:
                    end_mon=''
                try:
                    end_yr=dur_time['endDate']['year']
                except:
                    end_yr=''
                if end_yr and end_mon:
                    months=end_mon-int(start_mon)
                    years=end_yr-start_yr
                    if months<1:
                        months=12+months
                        years=years-1

                    duration=str(years)+" years, "+str(months)+" months"
                elif end_yr:
                    duration=str(end_yr-start_yr)+" years"
                else:
                    c_yr=today.year
                    c_month=today.month
                    months=c_month-start_mon
                    years=c_yr-start_yr
                    if months<1:
                        months=12+months
                        years=years-1
                    duration=str(years)+" years, "+str(months)+" months"
                output_dic['Org. '+str(new_j+1)+' duration']=duration
                try:
                    output_dic['Organization Location '+str(new_j+1)]=comp['locationName']
                except:
                    output_dic['Organization Location '+str(new_j+1)]=''
                try:
                    output_dic['Organization Description '+str(new_j+1)]=comp['description']
                except:
                    output_dic['Organization Description '+str(new_j+1)]=''
                try:
                    output_dic['Organization LI ID '+str(new_j+1)]=comp['companyUrn']
                except:
                    output_dic['Organization LI ID '+str(new_j+1)]=''
                try:
                    output_dic['Organization LI URL '+str(new_j+1)]='https://www.linkedin.com/company/'+comp['companyUrn'].split(':')[-1]
                except:
                    output_dic['Organization LI URL '+str(new_j+1)]=''
                new_j+=1
        
        ### LAnguages ####
        langs=p['languageView']['elements']
        languages=[]
        for lang in langs:
            languages.append(lang['name'])
        output_dic['Languages']=','.join(languages)
        
        ### Skills ####
        try:
            sview=pdata['skills']
        except:
            sview=[]
        skills=[]
        for skill in sview:
            skills.append(skill['name'])
        output_dic['Skills']=','.join(skills)
        
        ### Volunteer Experience ####
        vols=p['volunteerExperienceView']['elements']
        volunteers=[]
        for i, vol in enumerate(vols):
            output_dic["Volunteer Experience "+str(i+1)]=vol['role']+" at " +vol['companyName']
        
        #### Cerifications ####
        certs=p['certificationView']['elements']
        certifications=[]
        for cert in certs:
            certifications.append(cert['name'])
        output_dic['Certification']=','.join(certifications)

        #### Projects ####
        projs=p['projectView']['elements']
        projects=[]
        for proj in projs:
            projects.append(proj['title'])
        output_dic['Projects']=','.join(projects)
        
        ### Courses ###
        
        cours=p['courseView']['elements']
        courses=[]
        for cour in cours:
            courses.append(cour['name'])
        output_dic['Courses']=','.join(courses)
        
        ### Organizations ###
        
        orgs=p['organizationView']['elements']
        organizations=[]
        for org in orgs:
            organizations.append(org['name'])
        output_dic['Organizations']=','.join(organizations)
        
        ### Honors ###
        
        hons=p['honorView']['elements']
        honors=[]
        for hon in hons:
            honors.append(hon['title'])
        output_dic['Honors']=','.join(honors)
        netinfo=session.get('https://www.linkedin.com/voyager/api/identity/profiles/{}/networkinfo'.format(str(lid)))
        netdata=netinfo.json()
        output_dic['Followers']=netdata['followersCount']
        output_dic['Connections']=netdata['connectionsCount']
        
        ### Following Companies ###
        fcomp=session.get('https://www.linkedin.com/voyager/api/identity/profiles/{}/following?count\u003D10\u0026entityType\u003DCOMPANY\u0026q\u003DfollowedEntities'.format(str(lid)))
        fcompdata=fcomp.json()

        fcname=[]
        fcurl=[]
        for fc in fcompdata['elements']:
            fcname.append(fc['entity']['com.linkedin.voyager.entities.shared.MiniCompany']['name'])
            fcurl.append('https://www.linkedin.com/company/'+fc['followingInfo']['entityUrn'].split(':')[-1])
        
        output_dic['Interests/ followed companies Names']='\n'.join(fcname)
        output_dic['Interests/ followed companies URLs']='\n'.join(fcurl)
        
        ### Following group names
        fgroup=session.get('https://www.linkedin.com/voyager/api/identity/profiles/{}/following?count\u003D10\u0026entityType\u003DGROUP\u0026q\u003DfollowedEntities'.format(str(lid)))
        fgroupdata=fgroup.json()

        fgname=[]
        fgurl=[]
        for fg in fgroupdata['elements']:
            fgname.append(fg['entity']['com.linkedin.voyager.entities.shared.MiniGroup']['groupName'])
            fgurl.append('https://www.linkedin.com/groups/'+fg['followingInfo']['entityUrn'].split(':')[-1])
        
        output_dic['Interests/ followed groups Names']='\n'.join(fgname)
        output_dic['Interests/ followed groups URLs']='\n'.join(fgurl)
        
        ### Following School names
        fschool=session.get('https://www.linkedin.com/voyager/api/identity/profiles/{}/following?count\u003D10\u0026entityType\u003DSCHOOL\u0026q\u003DfollowedEntities'.format(str(lid)))
        fschooldata=fschool.json()

        fsname=[]
        fsurl=[]
        for fs in fschooldata['elements']:
            fsname.append(fs['entity']['com.linkedin.voyager.entities.shared.MiniSchool']['schoolName'])
            fsurl.append('https://www.linkedin.com/school/'+fs['followingInfo']['entityUrn'].split(':')[-1])
        
        output_dic['Interests/ followed schools Names']='\n'.join(fsname)
        output_dic['Interests/ followed schools URLs']='\n'.join(fsurl)
        
        ### Following Inflencer names
        finfluencer=session.get('https://www.linkedin.com/voyager/api/identity/profiles/{}/following?count\u003D10\u0026entityType\u003DINFLUENCER\u0026q\u003DfollowedEntities'.format(str(lid)))
        finfluencerdata=finfluencer.json()

        finame=[]
        fiurl=[]
        for fi in finfluencerdata['elements']:
            finame.append(fi['entity']['com.linkedin.voyager.entities.shared.MiniInfluencer']['name'])
            fiurl.append(fi['followingInfo']['entityUrn'].split(':')[-1])
        
        output_dic['Interests/ followed influencers Names']='\n'.join(finame)
        output_dic['Interests/ followed influencers URLs']='\n'.join(fiurl)
        new_output_dic={}
        for k in req_fields:
            try:
                new_output_dic[k]=output_dic.get(k)
            except:
                new_output_dic[k]=""
        print(output_dic)
        with open("People_data.csv",'a',newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(list(new_output_dic.values()))
        f.close()
        fin_output.append(output_dic)
        time.sleep(10)

