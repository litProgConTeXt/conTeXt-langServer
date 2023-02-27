
import copy
import io
import pytest
import yaml

from contextLangServer.processor.grammar import Grammar

def test_loadGrammar_empty() :
  Grammar.loadFromDict({})
  assert isinstance(Grammar.repository, dict)
  assert not Grammar.repository
  assert isinstance(Grammar.scopes2patterns, dict)
  assert not Grammar.scopes2patterns

#@pytest.mark.skip
def test_loadGrammar_fromFile() :
  if 'source.lpic' not in Grammar.scopes2patterns :
    Grammar.loadFromFile('tests/context.tmLanguage.json')

  assert isinstance(Grammar.repository, dict)
  assert 'comment-line' in Grammar.repository
  commentLine = Grammar.repository['comment-line']
  assert 'captures' in commentLine
  assert 'name' in commentLine
  assert commentLine['name'] == 'comment.line.percentage.tex'

  assert isinstance(Grammar.scopes2patterns, dict)
  assert 'source.lpic' in Grammar.scopes2patterns
  assert Grammar.scopes2patterns['source.lpic'] == 'source.lpic'
  assert 'source.lpic' in Grammar.repository
  sourceLPiC = Grammar.repository['source.lpic']
  assert 'include' in sourceLPiC['patterns'][0]
  assert sourceLPiC['patterns'][0]['include'] == '#lpic'
  assert 'lpic' in Grammar.repository
  lpic = Grammar.repository['lpic']
  assert 'patterns' in lpic
  assert len(lpic['patterns']) == 17
  assert 'include' in lpic['patterns'][2]
  assert lpic['patterns'][2]['include'] == '#context-definition'
  #assert False

def test_saveToIO() :
  if 'source.lpic' not in Grammar.scopes2patterns :
    Grammar.loadFromFile('tests/context.tmLanguage.json')

  gDict = Grammar.saveToDict('source.lpic')

  assert 'scopeName' in gDict
  assert gDict['scopeName'] == 'source.lpic'

  assert 'fileTypes' in gDict
  assert isinstance(gDict['fileTypes'], list)
  assert gDict['fileTypes'][0] == 'tex'

  assert 'foldingStartMarker' in gDict
  assert gDict['foldingStartMarker'] == '\\\\(start.*|b(TABLE|TD|TR))'
  assert 'foldingStopMarker'  in gDict
  assert gDict['foldingStopMarker'] == '\\\\(stop.*|e(TABLE|TD|TR))'

  assert 'patterns' in gDict
  assert isinstance(gDict['patterns'], list)
  assert gDict['patterns'][0]['include'] == 'source.lpic'

  assert 'repository' in gDict
  assert isinstance(gDict['repository'], dict)
  assert len(list(gDict['repository'].keys())) == 19

  assert 'firstLineMatch' in gDict
  assert gDict['firstLineMatch'] == '^%% lpic'

  #assert False

def test_collectPatternReferences() :
  if 'source.lpic' not in Grammar.scopes2patterns :
    Grammar.loadFromFile('tests/context.tmLanguage.json')

  patRefs = Grammar.collectPatternReferences('source.lpic')
  assert len(patRefs) == 23
  assert '#context-definition' in patRefs
  assert 'source.lua' in patRefs

  #assert False

@pytest.mark.skip
def test_checkRepository() :
  if 'source.lpic' not in Grammar.scopes2patterns :
    Grammar.loadFromFile('tests/context.tmLanguage.json')

  missingPats, extraPats, patRefs = Grammar.checkRepository('source.lpic')
  print("")
  print("--missing patterns-----------------------------------------------")
  print(yaml.dump(missingPats))
  print("--extra patterns-------------------------------------------------")
  print(yaml.dump(extraPats))
  print("--patterns-------------------------------------------------------")
  print(yaml.dump(patRefs))
  print("-----------------------------------------------------------------")
  assert len(missingPats) < 1
  assert len(extraPats) < 1

  assert False

#@pytest.mark.skip
def test_pruneRepository() :
  if 'source.lpic' not in Grammar.scopes2patterns :
    Grammar.loadFromFile('tests/context.tmLanguage.json')

  origRepo = Grammar.repository
  Grammar.repository = copy.deepcopy(origRepo)
  Grammar.pruneRepository('source.lpic')
  missingPats, extraPats, patRefs = Grammar.checkRepository('source.lpic')
  Grammar.repository = origRepo

  print("--missing patterns-----------------------------------------------")
  print(yaml.dump(missingPats))
  print("--extra patterns-------------------------------------------------")
  print(yaml.dump(extraPats))
  print("-----------------------------------------------------------------")
  assert len(extraPats) < 1

  missingPats, extraPats, patRefs = Grammar.checkRepository('source.lpic')
  print("--missing patterns-----------------------------------------------")
  print(yaml.dump(missingPats))
  print("--extra patterns-------------------------------------------------")
  print(yaml.dump(extraPats))
  print("-----------------------------------------------------------------")


  #assert False