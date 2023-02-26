
import copy
import importlib.resources
import json
#import pprint
import yaml

class Grammar :

  # Class variables and definitions

  repository = {}
  scopes2patterns = {}

  def addPatternsToRepository(aName, aScope, patterns) :
    if aName in Grammar.repository :
      print("WARNING: Duplicate pattern name {aPatternName} in repository.")
      print("  last pattern wins! (This may not be what you want)")
      print("")
    Grammar.repository[aName] = patterns
    if aScope :
      Grammar.scopes2patterns[aScope] = aName

  def loadFromDict(aGrammarDict) :
    if 'repository' in aGrammarDict :
      for aPatternName, aPattern in aGrammarDict['repository'].items() :
        aPatternScope = None
        if 'name' in aPattern: aPatterScope = aPattern['name']
        Grammar.addPatternsToRepository(aPatternName, aPatternScope, aPattern)
    scopeName = None
    if 'scopeName' in aGrammarDict :
      scopeName = aGrammarDict['scopeName']
    if 'patterns' in aGrammarDict :
      if not scopeName :
        print("WARNING: loading a grammer with no scope! ")
        print("  this means that this grammar can not be directly used!")
        print("")
      Grammar.addPatternsToRepository(
        scopeName, scopeName, aGrammarDict['patterns']
      )

  def loadFromFile(aGrammarPath) :
    with open(aGrammarPath) as grammarFile :
      grammarDict = json.loads(grammarFile.read())
      Grammar.loadFromDict(grammarDict)

  def loadFromResourceDir(aGrammarPackage) :
    syntaxDir = importlib.resources.files(aGrammarPackage)
    for aSyntaxFile in syntaxDir.iterdir() :
      if not aSyntaxFile.name.endswith('tmLanguage.json') : continue
      with importlib.resources.as_file(aSyntaxFile) as syntaxFile :
        syntaxStr = syntaxFile.read_text()
        syntaxDict = json.loads(syntaxStr)
        Grammar.loadFromDict(syntaxDict)
 
  def pruneRepository() :
    pass

  def checkRepository() :
    pass

  def saveToFile(aGrammarPath) :
    raise Exception("FIX ME")
    with open(aGrammarPath, 'w') as grammarFile :
      grammarDict = copy.deepcopy(Grammar.repository)
      grammarStr = json.dumps(grammarDict, indent=2) 
      grammarFile.write(grammarStr)
      grammarFile.write("\n")
  