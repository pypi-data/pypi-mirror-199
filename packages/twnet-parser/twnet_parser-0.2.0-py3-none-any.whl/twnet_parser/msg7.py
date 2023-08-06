NULL = 0
INFO = 1
MAP_CHANGE = 2 # sent when client should switch map
MAP_DATA = 3   # map transfer, contains a chunk of the map file
SERVERINFO = 4
CON_READY = 5  # connection is ready, client should send start info
SNAP = 6       # normal snapshot, multiple parts
SNAPEMPTY = 7  # empty snapshot
SNAPSINGLE = 8 # ?
SNAPSMALL = 9
INPUTTIMING = 10   # reports how off the input was
RCON_AUTH_ON = 11  # rcon authentication enabled
RCON_AUTH_OFF = 12 # rcon authentication disabled
RCON_LINE = 13     # line that should be printed to the remote console
RCON_CMD_ADD = 14
RCON_CMD_REM = 15

