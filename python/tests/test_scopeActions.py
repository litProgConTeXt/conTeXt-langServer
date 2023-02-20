

import asyncio
import pytest
import sys
import yaml

from contextLangServer.processor.scopeActions import ScopeActions
from utils import MockJsonRpc

@ScopeActions.method('simple.Str.Param')
def simpleStrParam(disp, ctx, aMessage, **kwargs) :
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

  