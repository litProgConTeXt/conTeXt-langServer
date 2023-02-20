
import copy
import yaml

class ScopeActions :

  # Class variables and definitions

  actions = {} # Class variable

  def method(scopeStr, packed=True, kwargsDict={}) :
    def decorator_scopeMethod(func) :
      scopeParts = scopeStr.split('.')
      print(yaml.dump(scopeParts))
      curScope = ScopeActions.actions
      for aScopePart in scopeParts :
        print(aScopePart)
        if aScopePart not in curScope :
          curScope[aScopePart] = {}
        curScope = curScope[aScopePart]
      curScope['__action__'] = {
        'scope'  : scopeStr,
        'method' : func,
        'packed' : packed,
        'kwargs' : copy.deepcopy(kwargsDict)
      }
      print(yaml.dump(ScopeActions.actions))
      return func
    return decorator_scopeMethod

  def pattern(scopeStr, aPattern) :
    scopeParts = scopeStr.split('.')
    print(yaml.dump(scopeParts))
    curScope = ScopeActions.actions
    for aScopePart in scopeParts :
      print(aScopePart)
      if aScopePart not in curScope :
        curScope[aScopePart] = {}
      curScope = curScope[aScopePart]
    curScope['__pattern__'] = {
      'scope'   : scopeStr,
      'pattern' : aPattern,
    }
    print(yaml.dump(ScopeActions.actions))


  # Instance varaibles and definitions

  def __init__(self, ctx=None, debugIO=None) :
    self.context = ctx
    self.debugIO = debugIO

  def getContext(self) :
    return self.context

  async def run(scopeStr) :
    scopeParts = scopeStr.split('.')
