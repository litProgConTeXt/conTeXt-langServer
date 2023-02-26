
import pytest
import yaml

from contextLangServer.processor.documents import Document, DocumentIter, DocumentCache

#@pytest.mark.skip
def test_loadDocument() :
  docPath = 'tests/docs/test.tex'
  if not DocumentCache.hasDocument(docPath) :
    DocumentCache.loadFromFile(docPath)
  print("-----------------------------------------------------------------")
  print(yaml.dump(DocumentCache.documents))
  print("-----------------------------------------------------------------")
  assert docPath in DocumentCache.documents
  theDoc = DocumentCache.documents[docPath]
  assert len(theDoc.docLines) == 8
  assert '  \\component partA' in theDoc.docLines
  assert theDoc.docName == docPath
  assert theDoc.filePath == docPath
  assert DocumentCache.hasDocument(docPath)
  assert DocumentCache.getDocument(docPath) == theDoc
  assert not DocumentCache.hasDocument('no document')
  assert DocumentCache.getDocument('no document') == None
  #assert False

def test_removeComment() :
  aStr = "this is a test"
  result = DocumentIter.removeComment(aStr)
  assert result == aStr
  aStr = "This is a test with % a comment"
  result = DocumentIter.removeComment(aStr)
  assert result == 'This is a test with '
  aStr = "This is a test with \\% no comment"
  result = DocumentIter.removeComment(aStr)
  assert result == aStr
  aStr = "This is a test with \\% no comment % and a comment"
  result = DocumentIter.removeComment(aStr)
  assert result == 'This is a test with \\% no comment '
  aStr = "This is another test with % a comment \\% and no comment"
  result = DocumentIter.removeComment(aStr)
  assert result == 'This is another test with '

def test_docIter() :
  docPath = 'tests/docs/test.tex'
  if not DocumentCache.hasDocument(docPath) :
    DocumentCache.loadFromFile(docPath)
  theDoc = DocumentCache.getDocument(docPath)
  print("------------------------------------------------------------------")
  print(yaml.dump(theDoc))
  print("------------------------------------------------------------------")
  iterA = theDoc.getDocIter()
  lines = theDoc.docLines
  curIndex = 0
  for aLine in iterA.nextLine() :
    assert aLine == lines[curIndex]
    curIndex += 1
  assert False