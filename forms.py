from django import forms
from django.contrib import admin
from ajax_select.fields import AutoCompleteSelectMultipleField, AutoCompleteSelectField
from codemirror.widgets import CodeMirrorTextarea


class PostForm(forms.ModelForm):
    
    '''
    images = AutoCompleteSelectMultipleField('image', required=False)
    files = AutoCompleteSelectMultipleField('image', required=False)
    preview = AutoCompleteSelectField('image', required=False)
    '''
    
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['javascript'].widget = CodeMirrorTextarea(parserfile=['parsejavascript.js', 'tokenizejavascript.js'], stylesheet=[r'codemirror/css/jscolors.css'])
        self.fields['header'].widget = CodeMirrorTextarea(parserfile=['parsexml.js'], stylesheet=[r'codemirror/css/xmlcolors.css'])
        self.fields['css'].widget = CodeMirrorTextarea(parserfile=['parsecss.js'], stylesheet=[r'codemirror/css/csscolors.css'])
        self.fields['content'].widget = CodeMirrorTextarea(parserfile=['parsecss.js', 'parsejavascript.js', 'tokenizejavascript.js', 'parsexml.js', 'parsehtmlmixed.js'],
                                                           stylesheet=[r'codemirror/css/csscolors.css', r'codemirror/css/xmlcolors.css', r'codemirror/css/jscolors.css'])
        self.fields['description'].widget = CodeMirrorTextarea(parserfile=['parsecss.js', 'parsejavascript.js', 'tokenizejavascript.js', 'parsexml.js', 'parsehtmlmixed.js'],
                                                           stylesheet=[r'codemirror/css/csscolors.css', r'codemirror/css/xmlcolors.css', r'codemirror/css/jscolors.css'])