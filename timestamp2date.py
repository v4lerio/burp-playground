'''
Author: v4lerio
Source: https://github.com/v4lerio/burp-playground/blob/main/timestamp2date.py

Based on https://github.com/PortSwigger/example-custom-editor-tab/blob/master/python/CustomEditorTab.py
'''

from burp import IBurpExtender
from burp import IMessageEditorTabFactory
from burp import IMessageEditorTab
from datetime import datetime
import re
 
class BurpExtender(IBurpExtender, IMessageEditorTabFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("Timestamp2Date")
        callbacks.registerMessageEditorTabFactory(self)
         
    def createNewInstance(self, controller, editable):
        #This bit returns the new tab we are adding that we are now doing all the work on
        tab = UrlDecoderTab(self, controller, editable)
        return tab
 
class UrlDecoderTab(IMessageEditorTab):
    def __init__(self, extender, controller, editable):
        self._extender = extender
        self._editable = editable
        self._txtInput = extender._callbacks.createTextEditor()
        self._txtInput.setEditable(editable)
        return
         
    def decodeData(self, content):
        params = self._extender._helpers.analyzeRequest(content).getParameters()
        val = 'Timestamp2Date'
 
        for param in params:
            value = param.getValue() 
            value = self._extender._helpers.bytesToString(value)
 
            pattern = re.compile(r'\d{9,13}')
            for match in re.findall(pattern, value):
                
                lenM = len(match)
                if lenM > 10:
                    match = match[0:10]
                    
                val += "\n\ninput: " + match
                val += "\noutput: " + str(datetime.fromtimestamp(int(match)))
     
        return val
 
    def getTabCaption(self):
        return "Timestamp2Date"
         
    def getUiComponent(self):
        return self._txtInput.getComponent()
         
    def isModified(self):
        return self._txtInput.isTextModified()
     
    def getSelectedData(self):
        return self._txtInput.getSelectedText()
 
    def isEnabled(self, content, isRequest):
        return not isRequest
         
    def setMessage(self, content, isRequest):
        if content is None:
            self._txtInput.setText(None)
            self._txtInput.setEditable(False)
        else:
            output=self.decodeData(content)
            self._txtInput.setText(output)
            self._txtInput.setEditable(self._editable)
        return
     
    def getMessage(self):
        return self._currentMessage
