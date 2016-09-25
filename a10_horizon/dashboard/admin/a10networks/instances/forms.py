<<<<<<< HEAD

=======
>>>>>>> Migration with testings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms

import helper

<<<<<<< HEAD
def array_to_choices(choices):
    return map(lambda x: (x, x), choices)

class MigrateDevice(forms.SelfHandlingForm):

    def __init__(self, *args, **kwargs):
        super(MigrateDevice, self).__init__(*args, **kwargs)

        instance_id = forms.CharField(label=_("Instance ID"),
            widget=forms.HiddenInput(),
            required=True)
        host_list = helper.get_hosts(self.request)
        host = forms.ChoiceField(label=_("Host IP"),
            choices=array_to_choices(host_list),
            required=True)

    def handle(self, request, data):
        try:
            migrate = helper.migrate(request,
                    data['instance_id'],
                    data['host'])
=======
def array_to_choices(choices=[]):
    return map(lambda x: (x, x), choices)


class MigrateDevice(forms.SelfHandlingForm):
    nova_instance_id = forms.CharField(label=_("Nova Instance ID"),
                                       widget=forms.HiddenInput(),
                                       required=False)
    host = forms.ChoiceField(label=_("Host IP"),
                              required=True)

    def __init__(self, *args, **kwargs):
        super(MigrateDevice, self).__init__(*args, **kwargs)
        host_list = helper.get_hosts(self.request)

        nova_instance_id = forms.CharField(label=_("Nova Instance ID"),
                                              widget=forms.HiddenInput(),
                                              required=False)
        host = forms.ChoiceField(label=_("Host IP"),
                                  choices=array_to_choices(host_list),
                                  required=True)
        instance_id = str(kwargs.get("initial").get("nova_instance_id"))
        self.fields["host"].choices = array_to_choices(helper.get_hosts(self.request))
        self.fields["nova_instance_id"].initial = instance_id

    def handle(self, request, context):
        try:
            migrate = helper.migrate(request,
                    context['nova_instance_id'],
                    context['host'])
>>>>>>> Migration with testings
            return migrate
        except Exception:
            exceptions.handle(request,
                    _('Unable to make the migration.'))
<<<<<<< HEAD


            def get_hosts(request):
                nova_api.host_list(request)
=======
>>>>>>> Migration with testings
