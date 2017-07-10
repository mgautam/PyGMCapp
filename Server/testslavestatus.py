import os
import errno
import json

wrpipe='/tmp/pcpipe'
rdpipe='/tmp/cppipe'
try:
    os.mkfifo(wrpipe)
except OSError as oe:
    if oe.errno != errno.EEXIST:
        print('cannot init named pipe')
        raise
with open(wrpipe,"w") as cmdbuf:
      cmdbuf.write("send_status")
      cmdbuf.close()
#with open(rdpipe,"r") as responsebuf:
#      while True:
#          data=responsebuf.readline().strip()
#          if len(data)!=0:
#                msg=json.dumps({'cmd':'status_send','ctrlid':'ctrlid','status':data})
#                print(msg)
#          else:
#                break
#      responsebuf.close()

