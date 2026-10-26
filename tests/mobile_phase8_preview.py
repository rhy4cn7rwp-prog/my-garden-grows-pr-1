"""Review deployment checks in isolated browser storage, never a player's browser."""
import os,json
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(root)));Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for width,height,top,bottom in [(320,440,20,0),(375,548,20,0),(428,746,47,34)]:
   page=browser.new_page(viewport={'width':width,'height':height},is_mobile=True,has_touch=True,ignore_https_errors=bool(os.environ.get('PREVIEW_URL')))
   page.set_default_timeout(8000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   page.add_init_script("document.addEventListener('DOMContentLoaded',()=>{document.documentElement.style.setProperty('--viewport-safe-top','"+str(top)+"px');document.documentElement.style.setProperty('--viewport-safe-bottom','"+str(bottom)+"px');syncGameViewport()})")
   page.emulate_media(reduced_motion='reduce')
   page.goto(os.environ.get('PREVIEW_URL',f'http://127.0.0.1:{server.server_port}/phase-8/'))
   def tap(name):page.get_by_role('button',name=name,exact=True).tap()
   def original():return page.evaluate("[localStorage.getItem('mgg10'),localStorage.getItem('mgg10-backup'),localStorage.getItem('mgg-pr-1:mgg10'),localStorage.getItem('mgg-pr-1:mgg10-backup')]")
   assert page.evaluate('view')=='clubhouse'
   assert original()==[None,None,None,None]
   assert page.evaluate("JSON.parse(localStorage.getItem('mgg-phase-8:mgg10')).cash")==50
   # A real pre-existing farm: rewards, garden, inventory and mid-payment market.
   fixture=page.evaluate('''()=>{const s=Game.initial();s.cash=1500;for(const id of ['ball','bike','camera'])Game.purchaseDream(s,id);s.day=9;s.season=2;s.seeds.carrot=7;s.plots[0]={id:'carrot',age:1,watered:true,left:0,quality:100};s.inventory.carrot=s.display.carrot=20;s.owned.scale=1;s.bagCount=9;Game.openMarket(s);Game.newCustomer(s,'Ruby');Game.greet(s,'good');s.customer.want={carrot:1};s.basket={carrot:1};while(Game.nextMathLine(s))Game.answerMathLine(s,Game.nextMathLine(s),Game.lineTotal(s,Game.nextMathLine(s)));Game.ring(s,Game.totalOrder(s));s.change=Game.changeDue(s);Game.pauseMarketClock(s);s.marketElapsedMs=123456;Game.syncMarketClock(s);return JSON.stringify(s)}''')
   # Install once before bootstrap, after the outgoing page's pagehide save.
   page.add_init_script("if(!sessionStorage.getItem('__prFixtureSet')){const raw="+json.dumps(fixture)+";localStorage.clear();localStorage.setItem('mgg10',raw);localStorage.setItem('mgg10-backup',raw);localStorage.setItem('mgg-pr-1:mgg10',raw);localStorage.setItem('mgg-pr-1:mgg10-backup',raw);sessionStorage.setItem('__prFixtureSet','1')}")
   page.reload();assert original()==[fixture,fixture,fixture,fixture]
   differences=page.evaluate('(raw)=>{const expected=Game.recover(raw);return Object.keys(state).filter(k=>JSON.stringify(state[k])!==JSON.stringify(expected[k])).map(k=>({key:k,current:state[k],expected:expected[k]}))}',fixture)
   assert not differences,differences
   assert page.evaluate('marketAwaitingResume') is True
   page.wait_for_function('clubhouseRoom.bookTableImage?.naturalWidth && clubhouseRoom.bookImage?.naturalWidth')
   assert page.locator('.clubhouse-guidebook').is_visible()
   page.locator('.clubhouse-guidebook').tap()
   for number in range(1,7):
    assert page.locator('.guidebook-pages output').inner_text()==f'{number} of 6'
    page.locator('.guidebook-illustration').evaluate('''async el=>{await Promise.all([...el.querySelectorAll('img')].map(i=>i.decode()));await Promise.all([...el.querySelectorAll('image')].map(el=>new Promise((resolve,reject)=>{const i=new Image();i.onload=resolve;i.onerror=reject;i.src=el.href.baseVal})));}''')
    assert page.locator('.guidebook-dialog').evaluate('e=>e.scrollHeight<=e.clientHeight+1')
    if number<6:tap('Next →')
   tap('Close How to Play');assert original()==[fixture,fixture,fixture,fixture]
   saved=page.evaluate('JSON.stringify(state)');page.wait_for_timeout(1100);assert page.evaluate('JSON.stringify(state)')==saved
   tap('Resume Market');assert page.evaluate('view')=='market'
   assert page.evaluate('state.step')=='pay'
   assert page.locator('.market-active-customer').count()==1
   assert page.locator('.market-active-customer').get_attribute('data-customer')=='Ruby'
   assert page.locator('.market-active-customer clipPath polygon').count()==1
   page.evaluate('finish()');assert page.evaluate('state.step')=='thanks'
   assert page.evaluate('state.bagCount')==8 and page.evaluate('state.inventory.carrot')==19
   assert original()==[fixture,fixture,fixture,fixture]
   # PR progress persists; later changes to public-game records cannot replace it.
   page.evaluate('pauseHiddenMarket()');progress=page.evaluate("localStorage.getItem('mgg-phase-8:mgg10')")
   page.evaluate("()=>{const source=JSON.parse(localStorage.getItem('mgg10'));source.cash=999;localStorage.setItem('mgg10',JSON.stringify(source))}")
   updated_original=original();page.reload()
   assert page.evaluate('(raw)=>JSON.stringify(state)===JSON.stringify(Game.recover(raw))',progress)
   assert original()==updated_original
   assert page.evaluate('state.cash')!=999
   # Corrupt PR primary recovers its independent backup without reading live data.
   backup=page.evaluate("localStorage.getItem('mgg-phase-8:mgg10-backup')")
   page.add_init_script("if(!sessionStorage.getItem('__prBrokenSet')){localStorage.setItem('mgg-phase-8:mgg10','{broken');sessionStorage.setItem('__prBrokenSet','1')}");page.reload()
   assert page.evaluate('(raw)=>JSON.stringify(state)===JSON.stringify(Game.recover(raw))',backup)
   assert original()==updated_original
   assert not errors,errors
   print(f'PASS Phase8 artwork/book, six pages, original saves untouched, farm copy, market recovery/sale and independent refresh/backup {width}x{height}',flush=True)
   page.close()
  browser.close()
finally:server.shutdown()
