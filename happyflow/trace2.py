from happyflow import trace_inspect
import trace


class Trace2(trace.Trace):
    def __init__(self, count=1, trace=1, countfuncs=0, countcallers=0,
                 ignoremods=(), ignoredirs=(), infile=None, outfile=None,
                 timing=False, test_name=None):

        super().__init__(count, trace, countfuncs, countcallers, ignoremods, ignoredirs, infile, outfile, timing)
        self.test_name = test_name

    def globaltrace_lt(self, frame, why, arg):
        """Handler for call events.

        If the code block being entered is to be ignored, returns `None',
        else returns self.localtrace.
        """
        if why == 'call':
            code = frame.f_code

            trace_inspect.collect_flow_and_state(frame, 'global', self.test_name, why)

            filename = frame.f_globals.get('__file__', None)
            if filename:
                # XXX _modname() doesn't work right for packages, so
                # the ignore support won't work right for packages
                modulename = trace._modname(filename)
                if modulename is not None:
                    ignore_it = self.ignore.names(filename, modulename)
                    if not ignore_it:
                        # if self.trace:
                        #     print((" --- modulename: %s, funcname: %s"
                        #            % (modulename, code.co_name)))
                        return self.localtrace
            else:
                return None

    def localtrace_trace_and_count(self, frame, why, arg):

        if why == "line" or why == 'return':

            # CHANGE
            trace_inspect.collect_flow_and_state(frame, 'local', self.test_name, why)

            # record the file name and line number of every trace
            filename = frame.f_code.co_filename
            lineno = frame.f_lineno
            key = filename, lineno
            self.counts[key] = self.counts.get(key, 0) + 1

            # if self.start_time:
            #     print('%.2f' % (_time() - self.start_time), end=' ')
            # bname = os.path.basename(filename)
            # print("%s(%d): %s" % (bname, lineno,
            #                       linecache.getline(filename, lineno)), end='')
        return self.localtrace