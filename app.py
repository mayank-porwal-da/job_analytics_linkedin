from flask import Flask,render_template, request,redirect
import pandas as pd


df = pd.read_csv('master_data_file.csv')


def function_for_oneskill(lis):
    try:
        s1 = df[df.skills.str.contains(f'{lis[0]}',case = False)]
        level = s1.Level.mode()[0]
        industry = s1.Industry.mode()[0]
        job_count = s1.shape[0]
        category= s1.clusters.mode()[0]
    except:
        level,industry,job_count = 'Not found','',''
    return [level, industry, job_count,category]

def function_for_twoskill(lis):
    try:
        s1 = df[df.skills.str.contains(f'{lis[0]}',case = False)]
        s2 = df[df.skills.str.contains(f'{lis[1]}',case = False)]
        data_with_bothskills = pd.merge(s1,s2, how='inner', on = ["Job_ID","Company","Job_name","Location","Applicants","involvement","Level","Employees","Link","Followers","Industry","skills","Company_ID","Details_ID","clusters"])
        level = data_with_bothskills.Level.mode()[0]
        industry = data_with_bothskills.Industry.mode()[0]
        job_count = data_with_bothskills.shape[0]
        category= data_with_bothskills.clusters.mode()[0]
        
    except:
        level ,industry,job_count,category = 'Not found','','',''
    return [level,industry,job_count,category]

def function_for_threeskill(lis):
    try:

        s1 = df[df.skills.str.contains(f'{lis[0]}',case = False)]
        s2 = df[df.skills.str.contains(f'{lis[1]}',case = False)]
        s3 = df[df.skills.str.contains(f'{lis[2]}',case = False)]
        intersect_s1_s2 = pd.merge(s1,s2, how='inner', on = ['Job_ID', 'Company', 'Job_name', 'Location', 'Applicants',
       'involvement', 'Level', 'Employees', 'Link', 'Followers', 'Industry',
       'skills', 'Company_ID', 'Details_ID', 'clusters'])
        innerjoin_three_skill_data = pd.merge(intersect_s1_s2,s3, how='inner', on = ['Job_ID', 'Company', 'Job_name', 'Location', 'Applicants',
       'involvement', 'Level', 'Employees', 'Link', 'Followers', 'Industry',
       'skills', 'Company_ID', 'Details_ID', 'clusters'])
        level = innerjoin_three_skill_data.Level.mode()[0]
        industry = innerjoin_three_skill_data.Industry.mode()[0]
        job_count = innerjoin_three_skill_data.shape[0]
        category= innerjoin_three_skill_data.clusters.mode()[0]
        
    except:
        level ,industry, job_count = 'Not found','',''
    return [level,industry,job_count,category]



app = Flask(__name__) # We are initializing the flask app

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")
    # Html files are always kept in template folder;

@app.route("/")
def hello():
    return redirect("http://google.com/", code=302)

@app.route("/result", methods = ['POST','GET'])
def result():
    output = request.form.to_dict()
    skills = output['name']
    lis = skills.split(sep=',')

    if len(lis)==3:
        result = function_for_threeskill(lis)
    elif len(lis)==2:
        result = function_for_twoskill(lis)
    elif len(lis)==1:
        result = function_for_oneskill(lis)
    else:
        result = ['nothing','nothing','nothing','nothing']
    
    return render_template("index.html", result=result) # here lis is putted into argument name;

if __name__ == '__main__':
    app.run(debug= True,port=5001)
