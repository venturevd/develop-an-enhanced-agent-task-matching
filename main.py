from flask import Flask, render_template_string, jsonify, request
from agent_broker import AgentBroker
import sys
app = Flask(__name__); b = AgentBroker(); fb = {}; sc = {}
@app.route('/')
def d(): return render_template_string('<h1>Enhanced Dashboard</h1><div id=s></div><pre id=d></pre><script>async function l(){var s=await fetch("/status").then(r=>r.json());document.getElementById("s").textContent=`Agents: ${s.agent_count} Tasks: ${s.task_count}`;document.getElementById("d").textContent=JSON.stringify(s,null,2)}setInterval(l,2e3);l()</script>')
@app.route('/status')
def st(): s=b.get_status(); s['feedback_count']=sum(len(x)for x in fb.values()); s['performance']=sc; return jsonify(s)
@app.route('/agents', methods=['POST'])
def ra(): d=request.get_json(); return jsonify({'success': b.register_agent(d.get('agent_id'), d.get('capabilities', []))})
@app.route('/tasks', methods=['POST'])
def rt(): d=request.get_json(); return jsonify({'success': b.submit_task(d.get('task_id'), d.get('requirements', []))})
@app.route('/feedback', methods=['POST'])
def rf():
    d=request.get_json(); a,t,r=d.get('agent_id'),d.get('task_id'),d.get('rating')
    if a not in b.agents or t not in b.tasks or t not in b.agents[a]['tasks']: return jsonify({'error':'Invalid assignment'}),400
    try: r=float(r)
    except: return jsonify({'error':'Rating must be numeric'}),400
    if not 1<=r<=5: return jsonify({'error':'Rating 1-5'}),400
    fb.setdefault(a,{})[t]=r; sc[a]=sum(fb[a].values())/len(fb[a]); return jsonify({'success':True,'average':sc[a]})
@app.route('/agents/<a>/tasks')
def at(a): t=b.get_matched_tasks(a); return jsonify({'agent_id':a,'tasks':sorted(t,key=lambda t: fb.get(a,{}).get(t,0),reverse=True)})
@app.route('/tasks/<t>/agents')
def ta(t): a=b.get_matched_agents(t); return jsonify({'task_id':t,'agents':sorted(a,key=lambda a: fb.get(a,{}).get(t,0),reverse=True)})
if __name__ == '__main__':
    if '--help' in sys.argv: print("Enhanced Dashboard with Dynamic Feedback.\n  python3 main.py        Start http://localhost:5001\n  POST /feedback: {agent_id,task_id,rating}\nSorts by per-task ratings."); sys.exit(0)
    print("Enhanced Dashboard: http://localhost:5001"); app.run(port=5001, debug=False)
