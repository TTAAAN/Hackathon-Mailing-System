"""Rate limiting utilities."""

from __future__ import annotations

import time


class RateLimiter:
    """Token-bucket rate limiter to comply with provider sending quotas."""

    def __init__(self, max_rate_per_sec: float = 2.0, burst_capacity: int = 3):
        self.rate = max_rate_per_sec
        self.capacity = burst_capacity
        self.tokens = float(burst_capacity)
        self.last_update = time.monotonic()

    def acquire(self) -> None:
        """Wait until a token is available to proceed."""
        while True:
            now = time.monotonic()
            elapsed = now - self.last_update
            self.last_update = now
            self.tokens = min(float(self.capacity), self.tokens + elapsed * self.rate)

            if self.tokens >= 1.0:
                self.tokens -= 1.0
                return

            sleep_needed = (1.0 - self.tokens) / self.rate
            time.sleep(sleep_needed)
