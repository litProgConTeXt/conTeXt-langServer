
from contextLangServer.langserver.dispatcher import Dispatcher

#############################################################################
# Language Features
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#languageFeatures

# Go to Declaration

#############################################################################
# Go to Definition
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_definition
@Dispatcher.lsRequest('textDocument/definition') :
async def textDocument_definition(disp, ctx, params, kwargs) :
  pass

# Go to Type Definition
# Go to Implementation

#############################################################################
# Find References
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_references
# textDocument/references

# Prepare Call Hierarchy
# Call Hierarchy Incoming Calls
# Call Hierarchy Outgoing Calls
# Prepare Type Hierarchy
# Type Hierarchy Super Types
# Type Hierarchy Sub Types
# Document Highlight
# Document Link
# Document Link Resolve

#############################################################################
# Hover
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_hover
# textDocument/hover

# Code Lens
# Code Lens Refresh
# Folding Range
# Selection Range

#############################################################################
# Document Symbols
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_documentSymbol
# textDocument/documentSymbol

# Semantic Tokens
# Inline Value
# Inline Value Refresh
# Inlay Hint
# Inlay Hint Resolve
# Inlay Hint Refresh
# Moniker

#############################################################################
# Completion Proposals
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_completion
# textDocument/completion

# Completion Item Resolve
# Publish Diagnostics
# Pull Diagnostics

#############################################################################
# Signature Help
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_signatureHelp
# textDocument/signatureHelp

# Code Action
# Code Action Resolve
# Document Color
# Color Presentation
# Formatting
# Range Formatting
# On type Formatting
# Rename
# Prepare Rename
# Linked Editing Range