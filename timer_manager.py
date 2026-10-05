import threading

class TimerManager:
    def __init__(self, interval_minutes: int = 30):
        self.interval_minutes = max(1, int(interval_minutes))
        self.interval_seconds = self.interval_minutes * 60
        self._stop_event = threading.Event()

    def set_interval_minutes(self, minutes: int):
        """타이머 간격 변경 (분 단위)"""
        self.interval_minutes = max(1, int(minutes))
        self.interval_seconds = self.interval_minutes * 60
        print(f"타이머 간격 변경: {self.interval_minutes}분")

    def wait_next_cycle(self):
        """다음 배치 전까지 대기"""
        print(f"{self.interval_minutes}분({self.interval_seconds}초) 대기 중...")
        self._stop_event.wait(self.interval_seconds)

    def stop(self):
        """대기 중단"""
        self._stop_event.set()
