def monitored_methods_overview(monitored_system):

    print('monitored_methods_overview')


    print('all_methods', len(monitored_system.all_methods()))
    print('all_calls', len(monitored_system.all_calls()))

    top_called = sorted(monitored_system.all_methods(), key=lambda m: len(m.calls), reverse=True)
    print(top_called[0])
    print(top_called[1])
    print(top_called[2])


    # len(monitored_system.all_methods()) # 31
    # len(monitored_system.all_calls())   # 14366
    #
    # top_called = sorted(monitored_system.all_methods(), key=lambda method: len(method.calls), reverse=True)
    # top_called[0] # gzip._PaddedFile.read (calls: 5432)
    # top_called[1] # gzip.GzipFile.readline (calls: 1183)
    # top_called[2] # gzip.GzipFile.seek (calls: 1026)
