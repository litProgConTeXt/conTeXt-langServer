

import yaml

class DocumentCache :
  def __init__(self) :
    self.documents = {}

class Document :
  def __init__(self) :
    self.docLines = []

  def loadFromFile(self, aPath) :
    with open(aPath) as docFile :
      self.refreshFromStr(docFile.read())

  def refreshFromStr(self, aDocStr) :
    self.docLines = aDocStr.splitlines()

  def update(self, startLine, endLine, updateStr) :
    pass

  def parse(self, grammar) :
    pass