#! .venv/bin/python

import asyncio
import json

from contextLangServer.langserver.simpleJsonRpc import AsyncJsonRpc

crlf = "\r\n"
inputArray = []
def addMsg(aDict) :
  jsonStr = json.dumps(aDict)
  inputArray.append(f"Content-Length: {len(jsonStr)}{crlf}{crlf}{jsonStr}")

addMsg({ "test" : "this is a test"})
addMsg({
  'jsonrpc' : '2.0',
  "method": "echo",
  'params': { 'aKey': 'aValue'},
  'id' : 10
})
addMsg({
  'jsonrpc' : '2.0',
  'method': 'stop',
  'params': {}
})

async def asyncMain() :
  proc = await asyncio.create_subprocess_shell(
    "./tests/server.py",
    stdin=asyncio.subprocess.PIPE,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE
  )
  stdinData = "".join(inputArray)
  print("---------------------------------------")
  print(stdinData)
  print("---------------------------------------")
  stdinData = stdinData.encode()
  stdoutData, stderrData = await proc.communicate(stdinData)
  print(stdoutData)
  print(stderrData)

def main() :
  asyncio.run(asyncMain())

if __name__ == '__main__' :
  main()