from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram

instrumentator = Instrumentator()
metrics = {
    'request_counter': Counter('real_requests_total', 'Total requests', ['method', 'endpoint', 'status']),
    'response_time': Histogram('real_response_duration_seconds', 'Response time', ['method', 'endpoint'],
                              buckets=[0.1, 0.5, 1.0])
}
