from django import forms

class TipForm(forms.ModelForm):
    class Meta:
        model = Tip
        
def submit_tip(request):
    pass
        
