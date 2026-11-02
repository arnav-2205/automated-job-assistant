import json, time, random, os, urllib.parse
from playwright.sync_api import sync_playwright
PROFILE=os.path.expanduser("~/.job-apply/browser-profile")
queries=["Full Stack Developer","Software Engineer Intern","SDE Intern","React Next.js Developer","Node.js Developer"]
ids={}
with sync_playwright() as p:
    c=p.chromium.launch_persistent_context(PROFILE,headless=False,viewport={"width":1366,"height":850})
    pg=c.pages[0]
    for q in queries:
        url=f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(q)}&location={urllib.parse.quote('Pune, India')}&f_TPR=r604800"
        pg.goto(url,wait_until="domcontentloaded",timeout=60000); time.sleep(random.uniform(5,7))
        if any(k in pg.url for k in ("checkpoint","authwall","login")): print("BLOCKED",pg.url); break
        for _ in range(2):
            pg.mouse.move(300,500); pg.mouse.wheel(0,1500); time.sleep(random.uniform(1.5,2.5))
        found=pg.evaluate("""()=>[...new Set([...document.querySelectorAll('[componentkey^="job-card-component-ref-"]')].map(e=>e.getAttribute('componentkey').replace('job-card-component-ref-','')))]""")
        print(q,len(found))
        for i in found[:9]: ids.setdefault(i,q)
    out={}
    for n,(jid,q) in enumerate(ids.items()):
        try:
            pg.goto(f"https://www.linkedin.com/jobs/view/{jid}/",wait_until="domcontentloaded",timeout=60000); time.sleep(random.uniform(3,5))
            t=pg.evaluate("document.querySelector('main')?document.querySelector('main').innerText:document.body.innerText")
            out[jid]=dict(q=q,url=f"https://www.linkedin.com/jobs/view/{jid}/",text=t[:3500],title=pg.title())
        except Exception as e: print("err",jid,str(e)[:60])
    json.dump(out,open("work/li_jobs.json","w",encoding="utf-8"),indent=1,ensure_ascii=False)
    print("total",len(out))
    c.close()
