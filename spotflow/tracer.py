import sys
import threading


class PyTracer:
    def __init__(self, collector):
        self.collector = collector
        self.active = False
        self.previous_trace = None
        self.previous_threading_trace = None

    def start_tracer(self):
        # The tracers that are replaced (e.g., of a debugger) are restored on stop
        self.previous_trace = sys.gettrace()
        self.previous_threading_trace = threading.gettrace()
        self.active = True
        # sys.settrace only traces the current thread: threading.settrace
        # also traces the threads that are started from now on
        threading.settrace(self._global_trace)
        sys.settrace(self._global_trace)

    def stop_tracer(self):
        self.active = False
        sys.settrace(self.previous_trace)
        threading.settrace(self.previous_threading_trace)
        self.previous_trace = None
        self.previous_threading_trace = None

    def _global_trace(self, frame, event, arg):
        if not self.active:
            # A thread that is still running after stop: only the thread
            # itself can remove its tracer
            if sys.gettrace() == self._global_trace:
                sys.settrace(None)
            return None

        if event in ("call", "line", "return", "exception"):
            is_monitored = self.collector.monitor_event(frame, event, arg)

            # Most frames are not of monitored methods (e.g., libraries and
            # tests). The lines, returns and exceptions of a frame are only
            # traced when its "call" event returns a trace function.
            if event == "call" and not is_monitored:
                return None

            return self._global_trace
