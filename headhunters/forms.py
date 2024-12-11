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

class JobOfferForm(forms.ModelForm):
    class Meta:
        model = JobOffer
        fields = '__all__'

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
