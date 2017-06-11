import sys

try:
    for line in sys.stdin:
        pass
except KeyboardInterrupt: # ctrl+c won't return an error
    pass
