import os,time,glob,traceback,io,contextlib
from playwright.sync_api import sync_playwright
PROFILE=os.path.expanduser("~/.job-apply/browser-profile")
with sync_playwright() as p:
    ctx=p.chromium.launch_persistent_context(PROFILE,headless=False,viewport={"width":1366,"height":850})
    G={"ctx":ctx,"pages":{}}
    print("ready",flush=True)
    while True:
        for f in sorted(glob.glob("work/q/*.py")):
            code=open(f,encoding="utf-8").read(); os.remove(f)
            buf=io.StringIO()
            with contextlib.redirect_stdout(buf):
                try: exec(code,G)
                except Exception: traceback.print_exc(file=buf)
            open(f.replace(".py",".out"),"w",encoding="utf-8").write(buf.getvalue())
        time.sleep(0.5)
