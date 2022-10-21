import trace
import sys


class PyTracer:

    def __init__(self, collector):
        self.collector = collector

    def start_tracer(self):
        sys.settrace(self._global_trace)

    def stop_tracer(self):
        sys.settrace(None)

    def _global_trace(self, frame, event, arg):

        if event in ('call', 'line', 'return', 'exception'):

            self.collector.monitor_event(frame, event, arg)

            return self._global_trace

            # filename = frame.f_globals.get('__file__', None)
            # if filename:
            #     modulename = trace._modname(filename)
            #     if modulename is not None:
            #         ignore_it = trace._Ignore().names(filename, modulename)
            #         if not ignore_it:
            #             return self._global_trace
            # else:
            #     return None

