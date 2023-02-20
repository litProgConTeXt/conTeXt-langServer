
import json
import yaml

class Grammar :
  def __init__(self) :
    self.patterns = {}
    self.scopes2patterns = {}
    self.scopeName = None

  def loadFromDict(self, aGrammarDict) :
    patterns = {}
    scopes2patterns = {}
    scopeName = 'source.unknown'
    if 'scopeName' in aGrammarDict :
      scopeName = aGrammarDict['scopeName']
    if 'repository' in aGrammarDict :
      for aPatternName, aPattern in aGrammarDict['repository'].items() :
        patterns[aPatternName] = aPattern
        if 'name' in aPattern :
          scopes2patterns[aPattern['name']] = aPatternName
    patterns[scopeName] = {}
    if 'patterns' in aGrammarDict :
      patterns[scopeName] = aGrammarDict['patterns']
    scopes2patterns[scopeName] = scopeName

    self.patterns = patterns
    self.scopes2patterns = scopes2patterns
    self.scopeName = scopeName

  def loadFromFile(self, aGrammarPath) :
    with open(aGrammarPath) as grammarFile :
      grammarDict = json.loads(grammarFile.read())
      #print("----grammar-dict-----------------------------")
      #print(yaml.dump(grammarDict))
      self.loadFromDict(grammarDict)


 