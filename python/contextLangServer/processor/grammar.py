
import copy
import importlib.resources
import json
#import pprint
import yaml

from contextLangServer.processor.scopeActions import ScopeActions

# see:
#  https://code.visualstudio.com/api/language-extensions/syntax-highlight-guide
#  https://macromates.com/manual/en/language_grammars

class Grammar :

  # Class variables and definitions

  repository = {}
  scopes2patterns = {}
  baseScopes = {}

  def addPatternsToRepository(aName, aScope, patterns) :
    if aName in Grammar.repository :
      print("WARNING: Duplicate pattern name {aPatternName} in repository.")
      print("  last pattern wins! (This may not be what you want)")
      print("")
    Grammar.repository[aName] = patterns
    if aScope :
      Grammar.scopes2patterns[aScope] = aName

  def loadFromDict(gDict) :

    # deal with the grammar's repository
    if 'repository' in gDict :
      for aPatternName, aPattern in gDict['repository'].items() :
        aPatternScope = None
        if 'name' in aPattern: aPatterScope = aPattern['name']
        Grammar.addPatternsToRepository(aPatternName, aPatternScope, aPattern)
  
    # deal with the grammar's base scope/pattern
    scopeName = None
    if 'scopeName' in gDict :
      scopeName = gDict['scopeName']
    if 'patterns' in gDict :
      if not scopeName :
        print("WARNING: loading a grammer with no scope! ")
        print("  this means that this grammar can not be directly used!")
        print("")
      Grammar.addPatternsToRepository(
        scopeName, scopeName, {
          'patterns' : gDict['patterns']
        }
      )
  
    # deal with the grammar's info
    info = {}
    if 'fileTypes' in gDict :
      info['fileTypes'] = gDict['fileTypes']
    if 'foldingStartMarker' in gDict :
      info['foldingStartMarker'] = gDict['foldingStartMarker']
    if 'foldingStopMarker' in gDict :
      info['foldingStopMarker'] = gDict['foldingStopMarker']
    if 'firstLineMatch' in gDict :
      info['firstLineMatch'] = gDict['firstLineMatch']
    info['scopeName'] = scopeName
    Grammar.baseScopes[scopeName] = info
  

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
 
  def collectPatternReferences(aScope) :
    repo = Grammar.repository
    patRefs = {}
    if aScope : patRefs[aScope] = True
    for aName, aPattern in repo.items() :
      #print(aName)
      if 'patterns' in aPattern :
        for aSubPattern in aPattern['patterns'] :
          if 'include' in aSubPattern :
            aPatRef = aSubPattern['include']
            if aPatRef == '$self' : continue
            #print(f"  {aPatRef}")
            patRefs[aPatRef] = True
    return list(patRefs.keys())
  
  def removePatternsWithNoActions(baseScope) :

    def foundPatternsWithActions(aDict) :
      if not isinstance(aDict, dict) : return False
      for aKey, aValue in aDict.items() :
        if aKey == 'name' :
          aValue = aValue.lstrip('#')
          if ScopeActions.hasAction(aValue) : 
            print(f"found action for {aValue}")
            return True
        if foundPatternsWithActions(aValue) : return True
      return False

    patternsWithActions = {}

    def removePatternsWithoutActions(aDict) :
      if not isinstance(aDict, dict) : return False
      numPatterns = 0
      hasAction   = False
      for aKey, aValue in aDict.items() :
        if aKey == 'patterns' :
          indices2delete = []
          for anIndex, aPat in enumerate(aValue) :
            if removePatternsWithoutActions(aPat) : indices2delete.append(anIndex)
          indices2delete.reverse()
          for anIndex in indices2delete :
            del aValue[anIndex]
          numPatterns = len(aValue)
        if aKey == 'name' :
          aValue = aValue.lstrip('#')
          if aValue in patternsWithActions and patternsWithActions[aValue] :
            hasAction = True
      if numPatterns < 1 :
        if 'patterns' in aDict : del aDict['patterns']
        return not hasAction
      return True

    repo    = Grammar.repository

    for aName, aPattern in repo.items() :
      patternsWithActions[aName] = foundPatternsWithActions(aPattern)

    names2delete = []
    for aName, aPattern in repo.items() :
      if removePatternsWithoutActions(aPattern) : names2delete.append(aName)
    
    for aName in names2delete :
      del repo[aName]
    return names2delete
      
  def pruneRepository(aScope) :
    patRefs     = Grammar.collectPatternReferences(aScope)
    repo        = Grammar.repository
    keys2delete = []
    for aName in repo :
      if aName not in patRefs and f"#{aName}" not in patRefs :
        keys2delete.append(aName)
    for aName in keys2delete :
      del repo[aName]
    return keys2delete

  def checkRepository(aScope) :
    patRefs = Grammar.collectPatternReferences(aScope)
    repo    = Grammar.repository
    missingPats = []
    extraPats   = []
    for aName in patRefs :
      aName = aName.lstrip('#')
      if aName not in repo :
        missingPats.append(aName)
    for aName in repo :
      if aName not in patRefs and f"#{aName}" not in patRefs :
        extraPats.append(aName)
    return missingPats, extraPats, patRefs

  def saveToDict(aScope) :
    if aScope not in Grammar.baseScopes :
      return None
    gDict = Grammar.baseScopes[aScope]
    gDict['patterns'] = [
      { 'include' : aScope }
    ]
    gDict['repository'] = copy.deepcopy(Grammar.repository)
    return gDict

  def savedToFile(aScope, aGrammarPath) :
    grammarDict = Grammar.saveToDict(aScope)
    if grammarDict :
      grammarStr = json.dumps(grammarDict, indent=2) 
      with open(aGrammarPath, 'w') as grammarFile :
        grammarFile.write(grammarStr)
        grammarFile.write("\n")
      return True
    return False