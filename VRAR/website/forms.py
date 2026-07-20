from django import forms

from .models import Annotation


class AnnotationForm(forms.ModelForm):
    class Meta:
        model = Annotation
        fields = ['title', 'instruction', 'audio_file', 'image_file']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Main Water Valve'}),
            'instruction': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Turn counter-clockwise to shut off.'}),
            'audio_file': forms.ClearableFileInput(attrs={'accept': 'audio/*'}),
            'image_file': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }