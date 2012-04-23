from django import forms
from django.contrib import admin
#from ajax_select.fields import AutoCompleteSelectMultipleField, AutoCompleteSelectField
#from codemirror.widgets import CodeMirrorTextarea


class FileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FileForm, self).__init__(*args, **kwargs)
        # key should be your sortable-field - in your exaple it's *index*
        self.fields['index'].widget = forms.HiddenInput()


class ContentForm(forms.ModelForm):
    
    '''
    images = AutoCompleteSelectMultipleField('image', required=False)
    files = AutoCompleteSelectMultipleField('image', required=False)
    preview = AutoCompleteSelectField('image', required=False)
    '''
    
    def __init__(self, *args, **kwargs):
        super(ContentForm, self).__init__(*args, **kwargs)
        #self.fields['javascript'].widget = CodeMirrorTextarea(parserfile=['parsejavascript.js', 'tokenizejavascript.js'], stylesheet=[r'js/codemirror/css/jscolors.css'], path="js/codemirror")
        #self.fields['header'].widget = CodeMirrorTextarea(parserfile=['parsexml.js'], stylesheet=[r'js/codemirror/css/xmlcolors.css'], path="js/codemirror")
        #self.fields['css'].widget = CodeMirrorTextarea(parserfile=['parsecss.js'], stylesheet=[r'js/codemirror/css/csscolors.css'], path="js/codemirror")
        #self.fields['content'].widget = CodeMirrorTextarea(parserfile=['parsecss.js', 'parsejavascript.js', 'tokenizejavascript.js', 'parsexml.js', 'parsehtmlmixed.js'], stylesheet=[r'codemirror/css/csscolors.css', r'codemirror/css/xmlcolors.css', r'codemirror/css/jscolors.css'])
        #self.fields['description'].widget = CodeMirrorTextarea(parserfile=['parsecss.js', 'parsejavascript.js', 'tokenizejavascript.js', 'parsexml.js', 'parsehtmlmixed.js], stylesheet=[r'codemirror/css/csscolors.css', r'codemirror/css/xmlcolors.css', r'codemirror/css/jscolors.css'])
        
