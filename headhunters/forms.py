from django import forms
from profile_cv.models import Profile_CV
from .models import HeadHunterUser, JobOffer, ManagementCandidates, Schedule, JobOfferNotification
class HeadHunterForm(forms.ModelForm):
    class Meta:
        model = HeadHunterUser
        fields = '__all__'

class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile_CV
        fields = '__all__'

from django import forms

class JobOfferForm(forms.ModelForm):
    class Meta:
        model = JobOffer
        fields = [
            'title', 'description', 'sector', 'category', 
            'salary', 'location', 'close_date', 
            'required_hard_skills', 'required_soft_skills', 
            'required_experience', 'JobOfferTests'
        ]
        widgets = {
            'required_hard_skills': forms.CheckboxSelectMultiple(),
            'required_soft_skills': forms.CheckboxSelectMultiple(),
            'JobOfferTests': forms.CheckboxSelectMultiple(),
        }


class ManagementCandidatesForm(forms.ModelForm):
    class Meta:
        model = ManagementCandidates
        fields = '__all__'

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = '__all__'


class JobOfferNotificationForm(forms.ModelForm):
    class Meta:
        model = JobOfferNotification
        fields = '__all__'
