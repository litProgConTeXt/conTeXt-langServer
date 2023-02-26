
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

  Grammar.loadFromFile('tests/context.tmLanguage.json')

  assert isinstance(Grammar.repository, dict)
  #print("------------------------------------------------------")
  #print(yaml.dump(Grammar.repository))
  #print("------------------------------------------------------")
  assert 'comment-line' in Grammar.repository
  commentLine = Grammar.repository['comment-line']
  assert 'captures' in commentLine
  assert 'name' in commentLine
  assert commentLine['name'] == 'comment.line.percentage.tex'

  assert isinstance(Grammar.scopes2patterns, dict)
  #print("------------------------------------------------------")
  #print(yaml.dump(Grammar.scopes2patterns))
  #print("------------------------------------------------------")
  assert 'source.lpic' in Grammar.scopes2patterns
  assert Grammar.scopes2patterns['source.lpic'] == 'source.lpic'
  assert 'source.lpic' in Grammar.repository
  sourceLPiC = Grammar.repository['source.lpic']
  assert 'include' in sourceLPiC[0]
  assert sourceLPiC[0]['include'] == '#lpic'
  assert 'lpic' in Grammar.repository
  lpic = Grammar.repository['lpic']
  print("------------------------------------------------------")
  print(yaml.dump(lpic))
  print("------------------------------------------------------")
  assert 'patterns' in lpic
  assert len(lpic['patterns']) == 17
  assert 'include' in lpic['patterns'][2]
  assert lpic['patterns'][2]['include'] == '#context-definition'
  #assert False