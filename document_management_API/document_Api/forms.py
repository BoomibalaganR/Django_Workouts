from django import forms

from .models import Document 


class DocumentUploadForm(forms.ModelForm):  
    files = forms.FileField() 
    class Meta:
        model = Document    
        fields = ['description'] 

class DocumentUpdateForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['description']  

    