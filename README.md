# Enhanced Agent-Task Matching Dashboard

Real-time dashboard with dynamic feedback for agent-task matching.

## Setup
pip install flask --break-system-packages
pip install -e /home/kingjames/agents/artifacts/build-an-agent-representation-broker-to-match-agen --break-system-packages

## Usage
python3 main.py  # http://localhost:5001

## API
- GET  /                    Dashboard (auto-refresh)
- GET  /status              Status with performance metrics
- POST /agents              Register agent ({"agent_id","capabilities"})
- POST /tasks               Submit task ({"task_id","requirements"})
- POST /feedback            Rate assignment ({"agent_id","task_id","rating":1-5})
- GET  /agents/<id>/tasks   Tasks sorted by agent's per-task rating
- GET  /tasks/<id>/agents   Agents sorted by rating for task

## Example
curl -XPOST http://localhost:5001/agents -H'Content-Type: application/json' -d'{"agent_id":"a1","capabilities":["python"]}'
curl -XPOST http://localhost:5001/tasks -H'Content-Type: application/json' -d'{"task_id":"t1","requirements":["python"]}'
curl http://localhost:5001/agents/a1/tasks
curl -XPOST http://localhost:5001/feedback -H'Content-Type: application/json' -d'{"agent_id":"a1","task_id":"t1","rating":5}'
