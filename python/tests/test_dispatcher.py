
import asyncio
import pytest
import sys
import yaml

from contextLangServer.langserver.dispatcher import Dispatcher
from utils import MockJsonRpc

async def simpleStrParam(disp, ctx, aMessage, **kwargs) :
  print("-----------------------------------------")
  print('simpleStrParam')
  print(aMessage)
  print("-----------------------------------------")
  ctx.append({
    'method'   : 'simpleStrParam',
    'msg'      : aMessage,
    'kwargs'   : kwargs,
    'dispType' : type(disp)
  })

async def simpleListParam(disp, ctx, msg1, msg2, **kwargs) :
  print("-----------------------------------------")
  print('simpleListParam')
  print(msg1)
  print(msg2)
  print("-----------------------------------------")
  ctx.append({
    'method'   : 'simpleListParam',
    'msg1'     : msg1,
    'msg2'     : msg2,
    'kwargs'   : kwargs,
    'dispType' : type(disp)
  })

async def simpleDictParam(disp, ctx, msg1="msg1", msg2="msg2", **kwargs) :
  print("-----------------------------------------")
  print('simpleDictParam')
  print(msg1)
  print(msg2)
  print("-----------------------------------------")
  ctx.append({
    'method'   : 'simpleDictParam',
    'msg1'     : msg1,
    'msg2'     : msg2,
    'kwargs'   : kwargs,
    'dispType' : type(disp)
  })

async def simpleRaiseExcep(disp, ctx, *params, **kwargs) :
  raise Exception("simple exception raised")

async def simpleBrokenDef() :
  pass

def simpleNotAsync(disp, ctx, *params, **kwargs) :
  pass

async def simpleStop(disp, ctx, *params, **kwargs) :
  disp.stopDispatching()

def test_listMethods() :
  disp = Dispatcher(None)
  disp.addMethod('simpleStrParam', simpleStrParam)
  disp.addMethod('simpleListParam', simpleListParam)
  disp.addMethod('simpleDictParam', simpleDictParam)
  disp.addMethod('simpleRaiseExcep', simpleRaiseExcep)
  disp.addMethod('simpleBrokenDef', simpleBrokenDef)
  disp.addMethod('simpleNotAsync', simpleNotAsync)
  disp.addMethod('simpleStop', simpleStop)
  methods = disp.listMethods()
  assert isinstance(methods, list)
  assert len(methods) == 7
  assert 'simpleStrParam' in methods
  assert 'simpleListParam' in methods
  assert 'simpleDictParam' in methods
  assert 'simpleRaiseExcep' in methods
  assert 'simpleBrokenDef' in methods
  assert 'simpleNotAsync' in methods
  assert 'simpleStop' in methods

@pytest.mark.asyncio
async def test_dispatch_strParam() :
  mockJsonRpc = MockJsonRpc(debugIO=sys.stdout)
  resultsCtx = []
  disp = Dispatcher(mockJsonRpc, resultsCtx)
  disp.addMethod('simpleStrParam', simpleStrParam)

  dispatcherTask = asyncio.create_task(disp.dispatchOnce())

  theMessage = 'this is a simple message'
  await mockJsonRpc.putNextMsg('simpleStrParam', theMessage)

  await dispatcherTask
  assert len(resultsCtx) == 1
  assert 'msg' in resultsCtx[0]
  assert resultsCtx[0]['msg'] == theMessage
  #print(yaml.dump(resultsCtx))
  #await mockJsonRpc.printMsgs()
  #assert False

@pytest.mark.asyncio
async def test_dispatch_listParam() :
  mockJsonRpc = MockJsonRpc(debugIO=sys.stdout)
  resultsCtx = []
  disp = Dispatcher(mockJsonRpc, resultsCtx)
  disp.addMethod('simpleListParam', simpleListParam)

  dispatcherTask = asyncio.create_task(disp.dispatchOnce())

  theMsg1 = 'this is the first message'
  theMsg2 = 'this is the second message'
  await mockJsonRpc.putNextMsg('simpleListParam', [ theMsg1, theMsg2 ], anId=1)

  await dispatcherTask
  assert len(resultsCtx) == 1
  assert 'msg1' in resultsCtx[0]
  assert resultsCtx[0]['msg1'] == theMsg1
  assert 'msg2' in resultsCtx[0]
  assert resultsCtx[0]['msg2'] == theMsg2
  #print(yaml.dump(resultsCtx))
  #await mockJsonRpc.printMsgs()
  #assert False

@pytest.mark.asyncio
async def test_dispatch_dictParam() :
  mockJsonRpc = MockJsonRpc(debugIO=sys.stdout)
  resultsCtx = []
  disp = Dispatcher(mockJsonRpc, resultsCtx)
  disp.addMethod('simpleDictParam', simpleDictParam)

  dispatcherTask = asyncio.create_task(disp.dispatchOnce())

  theMsg1 = 'this is the first message'
  theMsg2 = 'this is the second message'
  await mockJsonRpc.putNextMsg('simpleDictParam', {
    'msg1' : theMsg1,
    'msg2' : theMsg2
  })

  await dispatcherTask
  assert len(resultsCtx) == 1
  assert 'msg1' in resultsCtx[0]
  assert resultsCtx[0]['msg1'] == theMsg1
  assert 'msg2' in resultsCtx[0]
  assert resultsCtx[0]['msg2'] == theMsg2
  #print(yaml.dump(resultsCtx))
  #await mockJsonRpc.printMsgs()
  #assert False

@pytest.mark.asyncio
async def test_dispatch_raiseException() :
  mockJsonRpc = MockJsonRpc(debugIO=sys.stdout)
  resultsCtx = []
  disp = Dispatcher(mockJsonRpc, resultsCtx)
  disp.addMethod('simpleRaiseExcep', simpleRaiseExcep)

  dispatcherTask = asyncio.create_task(disp.dispatchOnce())

  theMsg1 = 'this is the first message'
  theMsg2 = 'this is the second message'
  await mockJsonRpc.putNextMsg('simpleRaiseExcep', {
    'msg1' : theMsg1,
    'msg2' : theMsg2
  })

  await dispatcherTask
  assert len(resultsCtx) == 0
  assert mockJsonRpc.getNumMsgs() == 1
  aMsgDict, anId = await mockJsonRpc.getLastMsg()
  assert 'error' in aMsgDict
  assert -1 < aMsgDict['error'].find('simple exception raised')
  #print(yaml.dump(aMsgDict))
  #print(yaml.dump(resultsCtx))
  #await mockJsonRpc.printMsgs()
  #assert False

@pytest.mark.asyncio
async def test_dispatch_brokenDef() :
  mockJsonRpc = MockJsonRpc(debugIO=sys.stdout)
  resultsCtx = []
  disp = Dispatcher(mockJsonRpc, resultsCtx)
  disp.addMethod('simpleBrokenDef', simpleBrokenDef)

  dispatcherTask = asyncio.create_task(disp.dispatchOnce())

  theMsg1 = 'this is the first message'
  theMsg2 = 'this is the second message'
  await mockJsonRpc.putNextMsg('simpleBrokenDef', {
    'msg1' : theMsg1,
    'msg2' : theMsg2
  })

  await dispatcherTask
  assert len(resultsCtx) == 0
  assert mockJsonRpc.getNumMsgs() == 1
  aMsgDict, anId = await mockJsonRpc.getLastMsg()
  assert 'error' in aMsgDict
  assert -1 < aMsgDict['error'].find('TypeError')
  #print(yaml.dump(aMsgDict))
  #print(yaml.dump(resultsCtx))
  #await mockJsonRpc.printMsgs()
  #assert False

@pytest.mark.asyncio
async def test_dispatch_notAsync() :
  mockJsonRpc = MockJsonRpc(debugIO=sys.stdout)
  resultsCtx = []
  disp = Dispatcher(mockJsonRpc, resultsCtx)
  disp.addMethod('simpleNotAsync', simpleNotAsync)

  dispatcherTask = asyncio.create_task(disp.dispatchOnce())

  theMsg1 = 'this is the first message'
  theMsg2 = 'this is the second message'
  await mockJsonRpc.putNextMsg('simpleNotAsync', {
    'msg1' : theMsg1,
    'msg2' : theMsg2
  })

  await dispatcherTask
  assert len(resultsCtx) == 0
  assert mockJsonRpc.getNumMsgs() == 1
  aMsgDict, anId = await mockJsonRpc.getLastMsg()
  assert 'error' in aMsgDict
  assert -1 < aMsgDict['error'].find('No coroutine')
  #print(yaml.dump(aMsgDict))
  #print(yaml.dump(resultsCtx))
  #await mockJsonRpc.printMsgs()
  #assert False

@pytest.mark.asyncio
async def test_dispatch_run() :
  mockJsonRpc = MockJsonRpc(debugIO=sys.stdout)
  resultsCtx = []
  disp = Dispatcher(mockJsonRpc, resultsCtx, debugIO=sys.stdout)
  disp.addMethod('simpleStrParam', simpleStrParam)
  disp.addMethod('simpleListParam', simpleListParam)
  disp.addMethod('simpleDictParam', simpleDictParam)
  disp.addMethod('simpleRaiseExcep', simpleRaiseExcep)
  disp.addMethod('simpleBrokenDef', simpleBrokenDef)
  disp.addMethod('simpleNotAsync', simpleNotAsync)
  disp.addMethod('simpleStop', simpleStop)

  dispatcherTask = asyncio.create_task(disp.run())

  theMsg  = "this is a message"
  theMsg1 = 'this is the first message'
  theMsg2 = 'this is the second message'
  theMsgs = { 'msg1' : theMsg1, 'msg2' : theMsg2 }

  await mockJsonRpc.putNextMsg('simpleStrParam', theMsg, anId=1)
  await mockJsonRpc.putNextMsg('simpleRaiseExcep', theMsgs, anId=2)
  await mockJsonRpc.putNextMsg('simpleListParam', [ theMsg1, theMsg2 ], anId=3)
  await mockJsonRpc.putNextMsg('simpleBrokenDef', theMsgs, anId=4)
  await mockJsonRpc.putNextMsg('simpleDictParam', theMsgs, anId=5)
  await mockJsonRpc.putNextMsg('simpleNotAsync', theMsgs, anId=6)
  await mockJsonRpc.putNextMsg('simpleStop', theMsgs, anId=7)
  
  await dispatcherTask
  assert len(resultsCtx) == 3
  aResult = resultsCtx[0]
  assert aResult['method'] == 'simpleStrParam'
  assert aResult['kwargs']['id'] == 1

  aResult = resultsCtx[1]
  assert aResult['method'] == 'simpleListParam'
  assert aResult['kwargs']['id'] == 3

  aResult = resultsCtx[2]
  assert aResult['method'] == 'simpleDictParam'
  assert aResult['kwargs']['id'] == 5

  assert mockJsonRpc.getNumMsgs() == 3
  aMsgDict, anId = await mockJsonRpc.getLastMsg()
  assert -1 < aMsgDict['error'].find('simple exception raised')
  aMsgDict, anId = await mockJsonRpc.getLastMsg()
  assert -1 < aMsgDict['error'].find('TypeError')
  aMsgDict, anId = await mockJsonRpc.getLastMsg()
  assert -1 < aMsgDict['error'].find('No coroutine')

  #print(yaml.dump(resultsCtx))
  #await mockJsonRpc.printMsgs()
  #assert False