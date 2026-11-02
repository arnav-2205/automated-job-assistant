import json, time, random, os, urllib.parse
from playwright.sync_api import sync_playwright
PROFILE=os.path.expanduser("~/.job-apply/browser-profile")
queries=["Full Stack Developer","Software Engineer Intern","React Developer","Node.js Developer","AI Engineer LLM","Backend Developer"]
known=set(json.load(open("work/li_jobs.json",encoding="utf-8")).keys())
ids={}
with sync_playwright() as p:
    c=p.chromium.launch_persistent_context(PROFILE,headless=False,viewport={"width":1366,"height":850})
    pg=c.pages[0]
    for q in queries:
        url=f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(q)}&location=India&f_WT=2&f_E=1%2C2&f_TPR=r604800"
        pg.goto(url,wait_until="domcontentloaded",timeout=60000); time.sleep(random.uniform(5,7))
        if any(k in pg.url for k in ("checkpoint","authwall","login")): print("BLOCKED",pg.url); break
        for _ in range(2):
            pg.mouse.move(300,500); pg.mouse.wheel(0,1500); time.sleep(random.uniform(1.5,2.5))
        found=pg.evaluate("""()=>[...new Set([...document.querySelectorAll('[componentkey^="job-card-component-ref-"]')].map(e=>e.getAttribute('componentkey').replace('job-card-component-ref-','')))]""")
        new=[i for i in found if i not in known]
        print(q,len(found),"new",len(new))
        for i in new[:8]: ids.setdefault(i,q)
    out={}
    for jid,q in ids.items():
        try:
            pg.goto(f"https://www.linkedin.com/jobs/view/{jid}/",wait_until="domcontentloaded",timeout=60000); time.sleep(random.uniform(3,5))
            t=pg.evaluate("document.querySelector('main')?document.querySelector('main').innerText:document.body.innerText")
            out[jid]=dict(q=q,url=f"https://www.linkedin.com/jobs/view/{jid}/",text=t[:3500],title=pg.title())
        except Exception as e: print("err",jid,str(e)[:60])
    json.dump(out,open("work/li_remote.json","w",encoding="utf-8"),indent=1,ensure_ascii=False)
    print("total",len(out)); c.close()
