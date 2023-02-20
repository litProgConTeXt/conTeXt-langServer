
import yaml

#############################################################################
# Language Server Protocol Specification

# see: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/
# see: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#implementationConsiderations

#############################################################################
# Lifecycle Messages
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#lifeCycleMessages

# Initialize
# initialize
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#initialize

# Initialized
# initialized
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#initialized

# Register Capability (unused)
# Unregister Capability (unused)
# Set Trace (unused)
# Log Trace (unused)

# Shutdown
# shutdown
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#shutdown

# Exit
# exit
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#exit


#############################################################################
# Document Synchronization
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_synchronization

#    Did Open Text Document
# textDocument/didOpen

#    Did Change Text Document
# textDocument/didChange

#    Will Save Text Document
# textDocument/willSave

#    Will Save Document Wait Until (unused)

#    Did Save Text Document
# textDocument/didSave

#    Did Close Text Document
# textDocument/didClose

#    Rename a Text Document (unused?!)

#    Overview - Notebook Document (unused)
#    Did Open Notebook Document (unused)
#    Did Change Notebook Document (unused)
#    Did Save Notebook Document (unused)
#    Did Close Notebook Document (unused)

#############################################################################
# Language Features
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#languageFeatures

# Go to Declaration
# Go to Definition
# Go to Type Definition
# Go to Implementation
# Find References
# Prepare Call Hierarchy
# Call Hierarchy Incoming Calls
# Call Hierarchy Outgoing Calls
# Prepare Type Hierarchy
# Type Hierarchy Super Types
# Type Hierarchy Sub Types
# Document Highlight
# Document Link
# Document Link Resolve

# Hover
# textDocument/hover

# Code Lens
# Code Lens Refresh
# Folding Range
# Selection Range
# Document Symbols
# Semantic Tokens
# Inline Value
# Inline Value Refresh
# Inlay Hint
# Inlay Hint Resolve
# Inlay Hint Refresh
# Moniker
# Completion Proposals
# Completion Item Resolve
# Publish Diagnostics
# Pull Diagnostics

# Signature Help
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


# textDocument/completion
# textDocument/definition
# textDocument/references
# textDocument/documentSymbol


#############################################################################
# Workspace Features

#    Workspace Symbols
#    Workspace Symbol Resolve
#    Get Configuration

#    Did Change Configuration
# workspace/didChangeConfiguration

#    Workspace Folders
#    Did Change Workspace Folders
#    Will Create Files
#    Did Create Files
#    Will Rename Files
#    Did Rename Files
#    Will Delete Files
#    Did Delete Files
#    Did Change Watched Files
#    Execute Command
#    Apply Edit


# workspace/symbol


#############################################################################
# Window Features

#    Show Message Notification
#    Show Message Request
#    Log Message
#    Show Document
#    Create Work Done Progress
#    Cancel a Work Done Progress
#    Sent Telemetry


