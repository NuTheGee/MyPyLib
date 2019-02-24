import time, calendar

def GetTime(ts=None, f_out="%H:%M:%S"):
    ts = time.time() if ts == None else ts
    local_time = time.localtime(ts)
    return time.strftime(f_out, local_time)

def GetDate(ts=None, f_out="%Y-%m-%d"):
    ts = time.time() if ts == None else ts
    local_time = time.localtime(ts)
    return time.strftime(f_out, local_time)

def LocalTimeString(t_string, f_in, f_out="%Y-%m-%d(%a) %H:%M %Z"):
    t = time.strptime(t_string, f_in)
    ts = calendar.timegm(t)
    local_time = time.localtime(ts)
    return time.strftime(f_out, local_time)
