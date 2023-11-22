from .views import *
from django.urls import path

urlpatterns = [
    path('dashboard', DashboardDataView.as_view(), name='dashboard'),
    path('refund', RefundStatementData.as_view(), name='refund'),
    path('intimation', IntimationData.as_view(), name='intimation'),
    path('proceeding', ProceedingData.as_view(), name='proceeding'),
    path('acknowledgement', AcknowledgementFile.as_view(), name='acknowledgement'),
    path('intimation_file', IntimationFile.as_view(), name='intimation_file'),
    path('proceeding_notice_file', ProceedingNoticeFile.as_view(), name='proceeding_notice_file'),
    path('tis_file', TISFile.as_view(),name='tis_file'),
    path('ais_file', AISFile.as_view(), name='ais_file'),
    path('form26as',Form26AS.as_view(),name='form26as')
]
