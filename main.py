import sys
from flask import Flask,jsonify,request
app=Flask(__name__);B=type('B',(),{})();B.a={};B.t={};B.fb={};B.lr=0.15
def reg(a,c):
 if a in B.a:return 0;B.a[a]={'c':{x:1.0 for x in c},'t':[],'s':0,'n':0};return 1
def sub(t,r):
 if t in B.t:return 0;B.t[t]={'r':r,'a':None,'st':'pending'};return 1
def _sc(a,t):return sum(a['c'].get(x,0)for x in t['r'])/len(t['r'])if t['r']else 0
def _s(a,t):return _sc(B.a[a],B.t[t])*0.7+B.fb.get(a,{}).get(t,2.5)/5.0*0.3
def m(r=0):
 o=[];_=[(t['st']!='pending'and not r)or[c:=sorted([(_s(aid,t),aid)for aid in B.a if all(x in B.a[aid]['c']for x in t['r'])],reverse=True),c and(c[0][1],t.update({'a':c[0][1],'st':'assigned'}),B.a[c[0][1]]['t'].append(tid),o.append({'task':tid,'agent':c[0][1],'score':round(c[0][0],3)}))]for tid,t in B.t.items()];return o
def fb(a,t,r):
 if a not in B.a or t not in B.t or not(1<=r<=5):return 0;B.fb.setdefault(a,{})[t]=r;x=B.a[a];_=[x['c'].update({re:(min(1.0,x['c'][re]+B.lr)if r>=4 else max(0.1,x['c'][re]-B.lr))})for re in B.t[t]['r']if re in x['c']];x['n']+=1;x['s']+=1 if r>=3 else 0;m(1);return 1
@app.route('/')
def i():return jsonify({'service':'Enhanced Agent-Task Matching','endpoints':['/status','/agents','/tasks','/feedback']})
@app.route('/status')
def st():s={'agents':len(B.a),'tasks':len(B.t),'assigned':sum(1 for x in B.t.values() if x['a'])};s['fb']=sum(len(x)for x in B.fb.values());return jsonify(s)
@app.route('/agents',methods=['POST'])
def ra():
 d=request.get_json()or{};a=d.get('agent_id');c=d.get('capabilities',[]);return jsonify({'error':'Invalid'})if not a or not isinstance(c,list)else(jsonify({'error':'Exists'}),409)if not reg(a,c)else(jsonify({'message':'Agent registered','agent_id':a}),201)
@app.route('/tasks',methods=['POST'])
def rt():
 d=request.get_json()or{};t=d.get('task_id');r=d.get('requirements',[]);return jsonify({'error':'Invalid'})if not t or not isinstance(r,list)else(jsonify({'error':'Exists'}),409)if not sub(t,r)else(jsonify({'message':'Task submitted','task_id':t}),201)
@app.route('/feedback',methods=['POST'])
def rf():
 d=request.get_json()or{};a,t,r=d.get('agent_id'),d.get('task_id'),d.get('rating');return jsonify({'error':'Missing'})if None in(a,t,r)else(jsonify({'error':'Num'}),400)if not isinstance(r,(int,float))else(jsonify({'error':'Invalid assignment'}),400)if not fb(a,t,float(r))else jsonify({'success':1})
@app.route('/agents/<a>')
def ag(a):
 if a not in B.a:return jsonify({'error':'Not found'}),404;x=B.a[a];return jsonify({'agent_id':a,'capabilities':{k:round(v,3)for k,v in x['c'].items()},'tasks':x['t'],'sr':round(x['s']/x['n'],3)if x['n']>0 else 0})
@app.route('/tasks/<t>')
def tg(t):
 if t not in B.t:return jsonify({'error':'Not found'}),404;x=B.t[t];return jsonify({'task_id':t,'requirements':x['r'],'agents':[x['a']]if x['a']else[],'status':x['st']})
if __name__=='__main__':
 if'--help'in sys.argv:print("Enhanced Agent-Task Matching\n python3 main.py [--port N]\n\nPOST /agents {agent_id,cap:[]}\nPOST /tasks {task_id,req:[]}\nPOST /feedback {a,t,r}\nGET /status /agents/<id> /tasks/<id>\n\nDynamic capability confidence, real-time reallocation.");sys.exit(0)
 p=int(sys.argv[sys.argv.index('--port')+1])if'--port'in sys.argv else 5001;h=sys.argv[sys.argv.index('--host')+1]if'--host'in sys.argv else'127.0.0.1';print(f"Broker: http://{h}:{p}");app.run(host=h,port=p,debug=False,use_reloader=False)
