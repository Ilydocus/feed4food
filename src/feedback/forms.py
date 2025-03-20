from django import forms
from .models import Feedback
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['topic', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'topic': 'What is this about?',
            'message': 'Your feedback'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'styled-form'
        
        # Create layout with custom styling
        self.helper.layout = Layout(
            Field('topic', css_class='form-control'),
            Field('message', css_class='form-control', rows=4),
            Submit('submit', 'Submit', css_class='btn btn-custom mt-3')
        )
        
        # Add labels with white text color
        for _, field in self.fields.items():
            field.label_attrs = {'style': 'color: white;'}