# Keep Windows from idle-sleeping while a long PixelLab queue runs (the PC slept once and stopped a queue). Uses the same
# call video players use (SetThreadExecutionState); no settings are changed and it ends by itself.
#   python tools/keep_awake.py <queue.log> [max hours=8]
# Lets go when the log says "queue finished", when the log has not changed for 40 minutes, or after max hours.
import ctypes, os, sys, time
log, hours = sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 8
ES_CONTINUOUS, ES_SYSTEM_REQUIRED = 0x80000000, 0x00000001
t0 = time.time()
ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)
try:
    while time.time() - t0 < hours * 3600:
        time.sleep(60)
        if not os.path.exists(log): continue
        if time.time() - os.path.getmtime(log) > 40 * 60: break
        with open(log, encoding='utf-8', errors='ignore') as f:
            if 'queue finished' in f.read()[-2000:]: break
finally:
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
