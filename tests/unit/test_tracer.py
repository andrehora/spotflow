import sys
import threading
import unittest
from tests.unit import stub_sut
from spotflow.api import monitor_func, SpotFlow


class TestTracer(unittest.TestCase):

    target = 'tests.unit.stub_sut.target_one'

    def setUp(self):
        self.addCleanup(sys.settrace, sys.gettrace())
        self.addCleanup(threading.settrace, threading.gettrace())

    def test_no_tracer_after_stop(self):
        sys.settrace(None)
        monitor_func(lambda: stub_sut.target_one(1), [self.target])
        self.assertIsNone(sys.gettrace())
        self.assertIsNone(threading.gettrace())

    def test_previous_tracer_is_restored(self):
        def previous_tracer(frame, event, arg):
            return None

        sys.settrace(previous_tracer)
        result = monitor_func(lambda: stub_sut.target_one(1), [self.target])
        after = sys.gettrace()
        sys.settrace(None)

        self.assertIs(after, previous_tracer)
        self.assertEqual(len(result[self.target].calls), 1)

    def test_previous_tracer_of_threads_is_restored(self):
        def previous_tracer(frame, event, arg):
            return None

        threading.settrace(previous_tracer)
        monitor_func(lambda: stub_sut.target_one(1), [self.target])

        self.assertIs(threading.gettrace(), previous_tracer)

    def test_previous_tracer_is_not_called_while_monitoring(self):
        events = []

        def previous_tracer(frame, event, arg):
            events.append(frame.f_code.co_name)
            return None

        sys.settrace(previous_tracer)
        monitor_func(lambda: stub_sut.target_one(1), [self.target])
        sys.settrace(None)

        self.assertNotIn('target_one', events)

    def test_calls_in_threads(self):
        def func():
            thread = threading.Thread(target=stub_sut.target_one, args=(1,))
            thread.start()
            thread.join()
            stub_sut.target_one(2)

        result = monitor_func(func, [self.target])

        calls = result[self.target].calls
        self.assertEqual(len(calls), 2)
        self.assertEqual([call.call_state.return_state.value for call in calls], ['2', '3'])
        self.assertEqual([len(call.run_lines) for call in calls], [1, 1])

    def test_calls_in_several_threads(self):
        def func():
            threads = [threading.Thread(target=stub_sut.target_one, args=(i,)) for i in range(5)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

        result = monitor_func(func, [self.target])

        calls = result[self.target].calls
        self.assertEqual(sorted(call.call_state.return_state.value for call in calls), ['1', '2', '3', '4', '5'])

    def test_thread_running_after_stop_is_not_monitored(self):
        started = threading.Event()
        stopped = threading.Event()
        tracers = []

        def in_thread():
            stub_sut.target_one(1)
            started.set()
            stopped.wait()
            stub_sut.target_one(2)
            tracers.append(sys.gettrace())

        thread = threading.Thread(target=in_thread)

        def func():
            thread.start()
            started.wait()

        result = monitor_func(func, [self.target])
        stopped.set()
        thread.join()

        self.assertEqual(len(result[self.target].calls), 1)
        self.assertEqual(tracers, [None])

    def test_start_and_stop_twice(self):
        flow = SpotFlow()
        flow.target_method_full_names([self.target])
        for _ in range(2):
            flow.start()
            stub_sut.target_one(1)
            flow.stop()

        self.assertEqual(len(flow.result()[self.target].calls), 2)
        self.assertIsNone(sys.gettrace())


if __name__ == '__main__':
    unittest.main()
