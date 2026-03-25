#!/usr/bin/env python3
"""Test the dashboard API endpoints."""
import sys, time, threading, requests
sys.path.insert(0, '/home/kingjames/agents/artifacts/build-an-agent-representation-broker-to-match-agen')
from agent_broker import AgentBroker
from flask import Flask, jsonify
broker = AgentBroker()
app = Flask(__name__)

@app.route('/')
def dash():
    return '<h1>Agent-Task Dashboard</h1><div id="s"></div><pre id="d"></pre><script>async function l(){var s=await fetch("/status").then(r=>r.json());document.getElementById("s").textContent="Agents: "+s.agent_count+" | Tasks: "+s.task_count;document.getElementById("d").textContent=JSON.stringify(s,null,2)}setInterval(l,2000);l()</script>'

@app.route('/status')
def st():
    return jsonify(broker.get_status())

@app.route('/agents', methods=['POST'])
def reg():
    d = __import__('flask').request.get_json()
    return jsonify({'success': broker.register_agent(d.get('agent_id'), d.get('capabilities', []))})

@app.route('/tasks', methods=['POST'])
def sub():
    d = __import__('flask').request.get_json()
    return jsonify({'success': broker.submit_task(d.get('task_id'), d.get('requirements', []))})

@app.route('/agents/<aid>/tasks')
def at(aid):
    return jsonify({'agent_id': aid, 'tasks': broker.get_matched_tasks(aid)})

@app.route('/tasks/<tid>/agents')
def ta(tid):
    return jsonify({'task_id': tid, 'agents': broker.get_matched_agents(tid)})

def run_srv():
    app.run(port=5001, debug=False, use_reloader=False)

def test():
    t = threading.Thread(target=run_srv, daemon=True); t.start(); time.sleep(1.5)
    try:
        r = requests.get("http://localhost:5001/status"); assert r.ok; print("✓ GET /status")
        r = requests.post("http://localhost:5001/agents", json={"agent_id":"test","capabilities":["python"]}); assert r.ok and r.json().get("success"); print("✓ POST /agents")
        r = requests.post("http://localhost:5001/tasks", json={"task_id":"task1","requirements":["python"]}); assert r.ok; print("✓ POST /tasks")
        r = requests.get("http://localhost:5001/agents/test/tasks"); assert "task1" in r.json().get("tasks",[]); print("✓ GET /agents/test/tasks")
        r = requests.get("http://localhost:5001/tasks/task1/agents"); assert "test" in r.json().get("agents",[]); print("✓ GET /tasks/task1/agents")
        r = requests.get("http://localhost:5001/"); assert "Dashboard" in r.text; print("✓ GET / (dashboard)")
        print("\nAll tests passed!"); return 0
    except Exception as e: print(f"\n✗ {e}"); return 1

if __name__ == "__main__":
    sys.exit(test())
