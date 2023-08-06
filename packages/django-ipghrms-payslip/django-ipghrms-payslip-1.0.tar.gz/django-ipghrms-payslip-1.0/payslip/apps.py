from django.apps import AppConfig
import os
from django.conf import settings

class PayslipConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payslip'
    path = os.path.join(settings.BASE_DIR, 'payslip')
