# Enhanced Agent-Task Matching Broker

Lightweight Flask service matching agents to tasks using dynamic capability confidence and real-time learning.

## Features
- Dynamic capability updates from feedback
- Real-time task reallocation
- Multi-criteria matching (70% capabilities, 30% performance)
- REST JSON API
- Single file, ≤50 LOC

## Installation
```bash
pip install flask
```

## Usage
```bash
python3 main.py --port 5001
```
Server: http://localhost:5001. Options: `--port N` (default 5001), `--host HOST` (default 127.0.0.1).

## API Endpoints
| Method | Endpoint       | Description                         |
|--------|----------------|-------------------------------------|
| GET    | /              | Service information                 |
| GET    | /status        | Broker status summary               |
| POST   | /agents        | Register agent (JSON: agent_id, capabilities[]) |
| POST   | /tasks         | Submit task (JSON: task_id, requirements[]) |
| POST   | /feedback      | Record rating (JSON: agent_id, task_id, rating 1-5) |
| GET    | /agents/<id>   | Agent details                       |
| GET    | /tasks/<id>    | Task details                        |

## Quick Demo
```bash
curl -X POST http://localhost:5001/agents -d '{"agent_id":"alice","capabilities":["python","ml"]}'
curl -X POST http://localhost:5001/tasks -d '{"task_id":"t1","requirements":["python","ml"]}'
curl -X POST http://localhost:5001/feedback -d '{"agent_id":"alice","task_id":"t1","rating":5}'
curl http://localhost:5001/status
```

Matching score = (capability_coverage * 0.7) + (feedback_bonus * 0.3). Feedback updates capability confidence (increase if rating >=4, else decrease) and reallocates pending tasks.

## Notes
- Confidence ranges 0.1–1.0 (initial 1.0)
- Ratings 1–5; >=3 counts as success
- Auto-reallocation on feedback

## License
MIT
