from typing import Any
from django import forms
from django.contrib import admin

from apps.authorizations.models import AccessRule, Resource, Role
from django.contrib.auth import get_user_model
from django.contrib.admin.widgets import FilteredSelectMultiple

from apps.privilege_manager.models import Team


admin.site.register(AccessRule)
admin.site.register(Resource)

class RoleForm(forms.ModelForm):
    name = forms.CharField(max_length=200)
    user = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects, 
        required=False,
        widget=FilteredSelectMultiple(verbose_name="users", is_stacked=False)
    )
    team = forms.ModelMultipleChoiceField(
        queryset=Team.objects, 
        required=False,
        widget=FilteredSelectMultiple(verbose_name="users", is_stacked=False)
    )
    class Meta:
        model = Role
        fields = ("name", "user",)

    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        if self.instance:
            is_insert = self.instance.pk is None
            self.fields["user"].initial = [] if is_insert else self.instance.user_set.all() 
            self.fields["team"].initial = [] if is_insert else self.instance.team_set.all() 

    def save(self, commit: bool = ...) -> Any:
        self.instance.user_set.add(*[u.id for u in self.cleaned_data['user']])
        self.instance.team_set.add(*[u.id for u in self.cleaned_data['team']])
        return super().save(commit=commit)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    form = RoleForm
    
    def __str__(self) -> str:
        return self.name
