
import pytest
import yaml

from contextLangServer.processor.grammar import Grammar

@pytest.mark.skip
def test_loadGrammar_empty() :
  grammar = Grammar()
  grammar.loadFromDict({})

  print("------------------------------------------------------")
  print(yaml.dump(grammar.patterns))
  print("------------------------------------------------------")
  print(yaml.dump(grammar.scopes2patterns))
  print("------------------------------------------------------")
  print(grammar.scopeName)
  print("------------------------------------------------------")

  assert False

@pytest.mark.skip
def test_loadGrammar_fromFile() :
  grammar = Grammar()
  grammar.loadFromFile('tests/context.tmLanguage.json')

  print("------------------------------------------------------")
  print(yaml.dump(grammar.patterns))
  print("------------------------------------------------------")
  print(yaml.dump(list(grammar.patterns.keys())))
  print("------------------------------------------------------")
  print(yaml.dump(grammar.scopes2patterns))
  print("------------------------------------------------------")
  print(grammar.scopeName)
  print("------------------------------------------------------")

  assert False
