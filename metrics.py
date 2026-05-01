from collections import defaultdict

class Metrics:
    def __init__(self):
        self.total_requests = 0
        self.cache_hits = 0
        self.latencies = []
        self.route_counts = defaultdict(int)
        self.route_latency = defaultdict(list)

        # 🔥 NEW
        self.total_tokens = 0
        self.total_cost = 0

    def log_request(self, cache_hit=False):
        self.total_requests += 1
        if cache_hit:
            self.cache_hits += 1

    def log_latency(self, route, latency):
        self.latencies.append(latency)
        self.route_counts[route] += 1
        self.route_latency[route].append(latency)

    # 🔥 NEW
    def log_cost(self, tokens, cost):
        self.total_tokens += tokens
        self.total_cost += cost

    def get_stats(self):
        avg_latency = (
            sum(self.latencies) / len(self.latencies)
            if self.latencies else 0
        )

        max_latency = max(self.latencies) if self.latencies else 0

        avg_latency_per_route = {
            r: sum(vals) / len(vals)
            for r, vals in self.route_latency.items()
        }

        return {
            "total_requests": self.total_requests,
            "cache_hit_rate": (
                self.cache_hits / self.total_requests
                if self.total_requests else 0
            ),
            "avg_latency": avg_latency,
            "max_latency": max_latency,
            "route_distribution": dict(self.route_counts),
            "avg_latency_per_route": avg_latency_per_route,

            # 🔥 NEW
            "total_tokens": self.total_tokens,
            "total_cost": self.total_cost
        }