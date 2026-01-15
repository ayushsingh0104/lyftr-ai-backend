from collections import defaultdict


class Metrics:
    def __init__(self):
        # (path, status) -> count
        self.http_requests_total = defaultdict(int)

        # result -> count
        self.webhook_requests_total = defaultdict(int)

    def inc_http(self, path: str, status: int):
        self.http_requests_total[(path, status)] += 1

    def inc_webhook(self, result: str):
        self.webhook_requests_total[result] += 1

    def render(self) -> str:
        lines = []

        # HTTP requests metric
        lines.append("# HELP http_requests_total Total HTTP requests")
        lines.append("# TYPE http_requests_total counter")
        for (path, status), count in self.http_requests_total.items():
            lines.append(
                f'http_requests_total{{path="{path}",status="{status}"}} {count}'
            )

        # Webhook results metric
        lines.append("# HELP webhook_requests_total Webhook processing outcomes")
        lines.append("# TYPE webhook_requests_total counter")
        for result, count in self.webhook_requests_total.items():
            lines.append(
                f'webhook_requests_total{{result="{result}"}} {count}'
            )

        return "\n".join(lines)


metrics = Metrics()
