from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms

import helper
from horizon_ops import HorizonOps


def array_to_choices(choices=[]):
    return map(lambda x: (x, x), choices)


class MigrateDevice(forms.SelfHandlingForm):
    nova_instance_id = forms.CharField(label=_("Nova Instance ID"),
                                       widget=forms.HiddenInput(),
                                       required=False)

    def __init__(self, *args, **kwargs):
        super(MigrateDevice, self).__init__(*args, **kwargs)
        horiz = HorizonOps()
        self.nova_api = horiz.get_nova()

        nova_instance_id = forms.CharField(label=_("Nova Instance ID"),
                                              widget=forms.HiddenInput(),
                                              required=False)
        instance_id = str(kwargs.get("initial").get("nova_instance_id"))
        self.fields["nova_instance_id"].initial = instance_id

    def handle(self, request, context):
        try:
            migrate = helper.migrate(request,
                    self.nova_api,
                    context['nova_instance_id'])
            return migrate
        except Exception:
            exceptions.handle(request,
                    _('Unable to make the migration.'))
