/* Test the exact dashboard JS and render its charts without a browser.
   npm install @napi-rs/canvas (Node 20+). This is not a browser end-to-end test. */
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const {createCanvas,GlobalFonts}=require('@napi-rs/canvas');
const font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';
if(fs.existsSync(font)){GlobalFonts.registerFromPath(font,'system-ui');GlobalFonts.registerFromPath(font,'sans-serif')}
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'evaluation_dashboard.html'),'utf8');
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const chartIds=['hist','box','rank','heat','agree','diff','scatter'];
const elements={};
function element(id){if(elements[id])return elements[id];let canvas=chartIds.includes(id)?createCanvas(id==='scatter'?1258:599,id==='scatter'?295:255):null;
return elements[id]={value:'',textContent:'',innerHTML:'',hidden:false,style:{},clientWidth:id==='scatter'?1258:599,clientHeight:id==='scatter'?295:255,
 add(){},listeners:{},addEventListener(k,f){this.listeners[k]=f},classList:{toggle(){}},setAttribute(){},getBoundingClientRect(){return {left:0,top:0}},
 getContext(){return canvas.getContext('2d')},get canvas(){return canvas},set width(v){canvas.width=v},set height(v){canvas.height=v}};}
const document={getElementById:element,querySelectorAll:()=>chartIds.map(element),createElement:()=>({click(){}})};
const win={devicePixelRatio:1,addEventListener(){}};
const ctx=vm.createContext({document,window:win,Option:function(t,v){return {text:t,value:v}},
 innerWidth:1400,innerHeight:1200,setTimeout,console,Blob,URL});vm.runInContext(script,ctx);
const run=s=>vm.runInContext(s,ctx),checks=[];
function test(name,f){f();checks.push({name,status:'passed'})}
test('Unfiltered count and row-weighted average',()=>{assert.equal(win.dashboardState.count,9000);assert.ok(Math.abs(win.dashboardState.average-55.26035111111111)<1e-8)});
test('Model selection applies to every selected row',()=>{element('model').value='Candidate A';run('render()');assert.equal(win.dashboardState.count,2250)});
test('Category selection combines with model filter',()=>{element('category').value='reasoning';run('render()');assert.equal(win.dashboardState.count,450)});
test('Date range combines with model and category',()=>{element('start').value='2026-10-07';element('end').value='2026-10-07';run('render()');assert.equal(win.dashboardState.count,5);assert.equal(win.dashboardState.judgeCount,5)});
test('Reset restores all 9000 records',()=>{element('reset').onclick();assert.equal(win.dashboardState.count,9000)});
test('Histogram bins include score 100 in last bin',()=>{const actual=run('DATA.filter(r=>r.score>=90&&r.score<=100).length');run('band=9;render()');assert.equal(win.dashboardState.count,actual);element('reset').onclick()});
test('Clicking a category chart updates the filter',()=>{run("hits.rank.find(h=>h.tip.startsWith('Reasoning')).action()");assert.equal(win.dashboardState.category,'reasoning');assert.equal(win.dashboardState.count,1800);element('reset').onclick()});
test('Candidate heatmap selection combines two filters',()=>{run("hits.heat.find(h=>h.tip.startsWith('Candidate B / Code')).action()");assert.equal(win.dashboardState.count,450);assert.equal(win.dashboardState.model,'Candidate B');element('reset').onclick()});
test('Empty range is safe and shows no-data state',()=>{element('start').value='2026-10-07';element('end').value='2026-07-10';run('render()');assert.equal(win.dashboardState.count,0);assert.equal(element('qAverage').textContent,'No data');element('reset').onclick()});
test('Judge page uses inclusive 10-point tolerance',()=>{element('judgeTab').onclick();assert.equal(win.dashboardState.view,'judges');assert.equal(element('jRate').textContent,'62.0%');assert.equal(run('JUDGES.filter(r=>r.score_difference<=10).length'),5576)});
test('CSV export invokes a download handler on both pages',()=>{element('export').onclick();element('scoreTab').onclick();element('export').onclick()});
test('No p-values, confidence intervals or statistical tests in dashboard',()=>{assert.ok(!/p-values|confidence intervals|statistical tests/i.test(html))});

function drawText(c,text,x,y,size=14,color='#adc3dc',weight='normal'){c.fillStyle=color;c.font=`${weight} ${size}px sans-serif`;c.textAlign='left';c.fillText(text,x,y)}
function panel(c,x,y,w,h){c.fillStyle='#10243d';c.beginPath();c.roundRect(x,y,w,h,10);c.fill();c.strokeStyle='#29405d';c.stroke()}
function preview(judges){run(`tab('${judges?'judges':'quality'}')`);const H=judges?1240:1275,W=1400,big=createCanvas(W,H),c=big.getContext('2d');c.fillStyle='#071527';c.fillRect(0,0,W,H);
 drawText(c,'i@work / AI EVALUATION LAB',36,42,13,'#70c1ff','bold');drawText(c,judges?'Judge Agreement Analysis Dashboard':'Model Evaluation Score Dashboard',36,84,31,'#edf5ff','bold');drawText(c,'Find quality gaps. Compare candidates. Decide what to improve next.',36,113,15);
 drawText(c,'SYNTHETIC LAB DATA',1090,55,13,'#ffcc80','bold');drawText(c,'No benchmark or production claims',1090,78,12,'#ffcc80');
 drawText(c,'MODEL QUALITY    /    JUDGE AGREEMENT',36,151,13,'#70c1ff','bold');panel(c,36,170,1328,85);
 [['Model version','All candidates'],['Category','All categories'],['From','2026-07-10'],['To','2026-10-07']].forEach(([k,v],i)=>{drawText(c,k,54+i*230,193,11);drawText(c,v,54+i*230,227,14,'#edf5ff')});drawText(c,'Reset filters   |   Export CSV',1035,221,13,'#70c1ff');
 drawText(c,'Unfiltered view / 90 days / filters and chart selections are available in the HTML file',36,277,12);
 const kpis=judges?[['Agreement rate','jRate','Within 10 points, inclusive'],['Average score gap','jGap','Absolute point difference'],['Compared evaluations','jCount','Two simulated judges'],['Large disagreements','jDisagree','Score difference > 10']]:[['Evaluations','qCount','2,250 distinct examples'],['Average quality score','qAverage','0-100 rubric score'],['Scores at or above 80','qTarget','Illustrative target'],['Evaluation days','qDays','2026-07-10 to 2026-10-07']];
 kpis.forEach(([label,id,note],i)=>{const x=36+i*336;panel(c,x,296,320,118);drawText(c,label.toUpperCase(),x+17,321,11);drawText(c,element(id).textContent,x+17,365,32,'#70c1ff','bold');drawText(c,note,x+17,395,11)});
 panel(c,36,430,1328,65);const insight=element(judges?'judgeInsight':'qualityInsight').textContent;let words=insight.split(' '),lines=[''];for(const word of words){let last=lines.length-1;if((lines[last]+' '+word).length>147)lines.push(word);else lines[last]+=(lines[last]?' ':'')+word}lines.forEach((t,i)=>drawText(c,t,54,454+19*i,13,'#a7e5ec'));
 const specs=judges?[['agree','Agreement by category','Higher agreement means more similar ratings, not proof of correctness.',36,512,648,330],['diff','Judge score differences','Count by 10-point score gap ranges.',716,512,648,330],['scatter','Judge comparison','All 9,000 selected evaluations. Diagonal: equal scores. Dashed: 10-point tolerance.',36,858,1328,335]]:[['hist','Score distribution','Count in each 10-point score band; final bin includes 100.',36,512,648,330],['box','Scores by category','Middle-half box, median line, minimum-to-maximum whiskers.',716,512,648,330],['rank','Category performance comparison','Average quality ranking. Dashed line: selected evaluations average.',36,858,648,330],['heat','Compare candidates by category','Average quality score per candidate and category.',716,858,648,330]];
 for(const [id,title,sub,x,y,w,h] of specs){panel(c,x,y,w,h);drawText(c,title,x+22,y+28,18,'#edf5ff','bold');drawText(c,sub,x+22,y+51,11);c.drawImage(element(id).canvas,x+22,y+64,w-44,h-72)}
 drawText(c,'Preview render from dashboard chart code. This is not a screenshot from Tableau Desktop.',36,H-24,12,'#ffcc80');
 fs.writeFileSync(path.join(root,judges?'judge_agreement_preview.png':'dashboard_preview.png'),big.toBuffer('image/png'));
}
preview(false);preview(true);
fs.writeFileSync(path.join(root,'docs/dashboard_logic_test_results.json'),JSON.stringify({status:'passed',environment:'Node VM with canvas and DOM test doubles; not a browser',checks},null,2)+'\n');
console.log(`${checks.length} dashboard logic checks passed. Two preview renders created.`);
