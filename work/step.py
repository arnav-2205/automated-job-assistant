import time
def modal(pg):
    return pg.evaluate("""()=>{const b=[...document.querySelectorAll('button')].find(e=>/^(Next|Review|Submit application)$/.test(e.innerText.trim()));if(!b)return 'NO BUTTON';let n=b;for(let i=0;i<12&&n.parentElement;i++){n=n.parentElement;if(n.querySelector('h1,h2,h3')&&n.innerText.length>150)break}return '[btn='+b.innerText.trim()+'] '+n.innerText.split("Skip to search")[0].slice(0,2500)}""")
def click(pg,label):
    pg.evaluate("""(l)=>{[...document.querySelectorAll('button')].find(e=>e.innerText.trim()===l).click()}""",label); time.sleep(2.5)
