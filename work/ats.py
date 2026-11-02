import json,re,urllib.request,concurrent.futures as cf
GH="rubrik postman pubmatic druva icertis browserstack thoughtspot mindtickle uptycs clevertap whatfix gupshup coupa zendesk freshworks sumologic nutanix cohesity hackerrank razorpaysoftwareprivatelimited phonepe groww zeta cred meesho amagi dream11 slice navi sprinklr eightfold highradius sigmoid datadog stripe cloudflare okta twilio elastic mongodb databricks atlassian gitlab hashicorp pagerduty samsara zscaler netskope appsflyer".split()
LV="meesho cred palantir mindtickle zeta paytm gojek spotify whoop highspot clari".split()
KW=re.compile(r"intern|fresher|graduate|trainee|associate software|software engineer i\b|sde[- ]?1|sde i\b|new grad|entry|junior|early career|sde intern|engineer 1|engineer i\b",re.I)
LOC=re.compile(r"pune|india|remote|bengaluru|bangalore|mumbai|hyderabad",re.I)
def get(u):
    try: return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"}),timeout=15))
    except Exception as e: return None
def gh(c):
    d=get(f"https://boards-api.greenhouse.io/v1/boards/{c}/jobs"); r=[]
    for j in (d or {}).get("jobs",[]):
        if KW.search(j["title"]) and LOC.search(j["location"]["name"]): r.append(("greenhouse",c,j["title"],j["location"]["name"],j["absolute_url"],j.get("updated_at","")[:10]))
    return r if d else [("_dead",c)]
def lv(c):
    d=get(f"https://api.lever.co/v0/postings/{c}?mode=json"); r=[]
    for j in d or []:
        l=j.get("categories",{}).get("location","") or ""
        if KW.search(j["text"]) and LOC.search(l): r.append(("lever",c,j["text"],l,j["hostedUrl"],""))
    return r if d is not None else [("_dead",c)]
with cf.ThreadPoolExecutor(10) as ex: res=list(ex.map(gh,GH))+list(ex.map(lv,LV))
live=[];dead=[]
for r in res:
    for x in r:
        (dead if x[0]=="_dead" else live).append(x)
print("dead boards:",[x[1] for x in dead])
for x in sorted(live,key=lambda x:(not re.search("pune",x[3],re.I),x[1])): print(x)
json.dump(live,open("work/ats_jobs.json","w"),indent=1)
