

from contextLangServer.langserver.dispatcher import Dispatcher

##############################################################################
# Lifecycle Messages
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#lifeCycleMessages

##############################################################################
# Initialize
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#initialize
#
@Dispatcher.lsRequest('initialize') # all parameters in kwargs
async def initialize(disp, ctx, params, kwargs) :
  if disp.debugIO : 
    disp.debugIO.write("lsRequest: initialize\n")
  return {
    'capabilities' : {
      'textDocumentSync' : {
        'openClose' : True,
        'change' : 2
      },
      'completionProvider' : {
        'triggerCharacters' : [ "\\", "{", "[", ",", "=" ],
      },
      'signatureHelpProvider' : {
        'triggerCharacters' : [ "{", "[", "=" ],
      },
      'hoverProvider'           : True,
      'definitionProvider'      : True,
      'referencesProvider'      : True,
      'documentSymbolProvider'  : True,
      'workspaceSymbolProvider' : True
    },
    'serverInfo' : {
      'name' : "ConTeXtLS",
      'version' : '0.0.1' #config.version
    }
  }

##############################################################################
# Initialized
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#initialized
#
@Dispatcher.lsNotification('initialized')
async def initialized(disp, ctx, params, kwargs) :
  if disp.debugIO : 
    disp.debugIO.write("lsNotification: initialized\n")
  return None
  
# Register Capability (unused)
# Unregister Capability (unused)
# Set Trace (unused)
# Log Trace (unused)

##############################################################################
# Shutdown
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#shutdown
@Dispatcher.lsRequest('shutdown')
async def shutdown(disp, ctx, params, kwargs) :
  if disp.debugIO : 
    disp.debugIO.write("lsRequest: shutdown\n")
  return {}

##############################################################################
# Exit
# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#exit
@Dispatcher.lsNotification('exit')
async def exit(disp, ctx, params, kwargs) :
  if disp.debugIO : 
    disp.debugIO.write("lsNotification: exit\n")
  disp.stopDispatching()
  return None
