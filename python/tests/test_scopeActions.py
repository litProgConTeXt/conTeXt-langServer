

import asyncio
import pytest
import sys
import yaml

from contextLangServer.processor.scopeActions import ScopeActions

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

  
def test_simpleStrParam() :
  actions = ScopeActions.actions
  #print("----------------------------------------------------------------")
  #print(yaml.dump(actions))
  #print("----------------------------------------------------------------")
  assert isinstance(actions, dict)
  assert 'simple' in actions
  assert 'Str' in actions['simple']
  assert 'Param' in actions['simple']['Str']
  assert '__action__' in actions['simple']['Str']['Param']
  action = actions['simple']['Str']['Param']['__action__']
  #print("----------------------------------------------------------------")
  #print(yaml.dump(action))
  #print("----------------------------------------------------------------")
  assert isinstance(action['kwargs'], dict)
  assert not action['kwargs']
  assert action['packed']
  assert action['scope'] == 'simple.Str.Param'
  #print(type(simpleStrParam))
  assert isinstance(action['method'], type(simpleStrParam))
  assert action['method'] == simpleStrParam
  #assert False