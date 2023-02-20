

import yaml

class DocumentCache :
  def __init__(self) :
    self.documents = {}

class Document :
  def __init__(self) :
    self.docLines = []

  def refreshFromStr(self, aDocStr) :
    self.docLines = aDocStr.splitlines()

  def update(self, startLine, endLine, updateStr) :
    pass

  def parse(self, grammar) :
    pass