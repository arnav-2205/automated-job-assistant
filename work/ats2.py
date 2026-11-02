import json,re,urllib.request,concurrent.futures as cf
GH="persistentsystems gslab synechron amberflux crossbeam ibm cybage quicksand harness-inc harness veeam bmc coinbase robinhood airbnb lyft dropbox figma notion asana brex ramp plaid gusto mercury anduril scaleai openai anthropic vercel supabase retool airtable rippling deel carta intercom elastic newrelic grafanalabs confluent cockroachlabs singlestore fivetran dbtlabs snyk mongodb gitlab jfrog sentry postmanlabs juspay zoho lenskart urbancompany chargebee thoughtworks agoda thumbtack tekion wiz sumup coursera udemy duolingo toast squarespace".split()
LV="plaid wealthfront netflix kpmg sedna atlan rapido jumbotail ola zomato swiggy upgrad sharechat lendingkart juspay pinelabs ather tekion".split()
ASH="notion ramp openai cohere linear sierra decagon replit mercor elevenlabs perplexity cursor clay vanta deel supabase".split()
KW=re.compile(r"intern|fresher|graduate|trainee|associate software|software engineer i\b|sde[- ]?1|sde i\b|new grad|entry|junior|early career|engineer 1|engineer i\b|apprentice",re.I)
LOC=re.compile(r"pune|india|remote|bengaluru|bangalore|mumbai|hyderabad|gurgaon|noida",re.I)
def get(u):
    try: return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"}),timeout=15))
    except Exception: return None
def gh(c):
    d=get(f"https://boards-api.greenhouse.io/v1/boards/{c}/jobs")
    if d is None: return [("_dead",c)]
    return [("greenhouse",c,j["title"],j["location"]["name"],j["absolute_url"]) for j in d.get("jobs",[]) if KW.search(j["title"]) and LOC.search(j["location"]["name"]) and re.search("engineer|developer|software|sde|intern",j["title"],re.I)]
def lv(c):
    d=get(f"https://api.lever.co/v0/postings/{c}?mode=json")
    if d is None: return [("_dead",c)]
    return [("lever",c,j["text"],j.get("categories",{}).get("location",""),j["hostedUrl"]) for j in d if KW.search(j["text"]) and LOC.search(j.get("categories",{}).get("location","") or "") and re.search("engineer|developer|software|sde|intern",j["text"],re.I)]
def ash(c):
    d=get(f"https://api.ashbyhq.com/posting-api/job-board/{c}")
    if d is None: return [("_dead",c)]
    return [("ashby",c,j["title"],j.get("location",""),j["jobUrl"]) for j in d.get("jobs",[]) if KW.search(j["title"]) and LOC.search(j.get("location","") or "") and re.search("engineer|developer|software|sde|intern",j["title"],re.I)]
with cf.ThreadPoolExecutor(12) as ex: res=list(ex.map(gh,GH))+list(ex.map(lv,LV))+list(ex.map(ash,ASH))
live=[x for r in res for x in r if x[0]!="_dead"]
print("live:",sum(1 for r in res if not(r and r[0][0]=="_dead")),"of",len(res))
for x in sorted(live,key=lambda x:(not re.search("pune",x[3],re.I),x[1])): print(x)
