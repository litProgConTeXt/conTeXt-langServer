

import yaml

class DocumentCache :

  # class methods and variables

  documents = {}

  def hasDocument(aPath) :
    return aPath in DocumentCache.documents

  def getDocument(aPath) :
    if aPath in DocumentCache.documents :
      return DocumentCache.documents[aPath]
    return None

  def loadFromFile(aPath) :
    doc = Document()
    doc.loadFromFile(aPath)
    DocumentCache.documents[aPath] = doc
    return doc

  def loadFromStr(docName, docStr) :
    doc = Document()
    doc.loadFromStr(docName, docStr)
    DocumentCache.documents[docName] = doc
    return doc

  def parse(docName, startingScope) :
    if docName in DocumentCache.documents :
      theDoc = DocumentCache.documents[docName]
      theDocIter = theDoc.getDocIter()
      aProbe = theDocIter.nextProbe()
      while aProbe :
        print(aProbe)
        if aProbe in Grammar.macros :
          index = theDocIter.curLine.find(aProbe)
          print(f"Found {aProbe} at {index} in [{theDocIter.curLine}]")
          Grammar.macros[aProbe](theDocIter, index)
        aProbe = theDocIter.nextProbe()

class DocumentIter :

  # Class variables and definitions

  def removeComment(aLine) :
    parts = aLine.split('%')
    newLine = []
    while True :
      if len(parts) < 1 : break
      firstPart = parts.pop(0)
      newLine.append(firstPart)
      if not firstPart.endswith('\\') : break
    return "%".join(newLine)

  # Instance variables and definitions

  def __init__(self, aDoc) :
    self.theDoc = aDoc
    self.curLine = None

  def __lineIter__(self) :
    for aLine in self.docLines :
      aLine = aLine.strip()
      yield aLine
    yield None

  def nextLine(self) :
    return(self.__lineIter__, None)

  def __probeIter__(self) :
    curLine = self.nextLine()
    while curLine is not None :
      curLine = Document.removeComment(curLine)
      curProbes = Document.macroRE.findall(curLine)
      for aProbe in curProbes :
        yield aProbe
      self.nextLine()
    yield None

  def nextProbe(self) :
    return next(self.__probeIter__, None)

class Document :
  def __init__(self) :
    self.filePath = None
    self.docName  = None
    self.docLines = []

  def loadFromFile(self, aPath) :
    self.filePath = aPath
    with open(aPath) as docFile :
      self.refreshFromStr(aPath, docFile.read())

  def refreshFromStr(self, aDocName, aDocStr) :
    self.docName  = aDocName
    self.docLines = aDocStr.splitlines()

  def update(self, startLine, endLine, updateStr) :
    pass

  def getDocIter(self) :
    return DocumentIter(self)
