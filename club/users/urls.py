from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Sócios (exemplo, pode ser removido se não usar aqui)
    path('socios/', views.SocioListView.as_view(), name='socio_list'),
    path('socios/novo/', views.SocioCreateView.as_view(), name='socio_create'),
    path('socios/<int:pk>/editar/', views.SocioUpdateView.as_view(), name='socio_update'),
    path('socios/<int:pk>/excluir/', views.SocioDeleteView.as_view(), name='socio_delete'),

    # Leads
    path('leads/', views.ClienteLeadListView.as_view(), name='clientelead_list'),
    path('leads/novo/', views.ClienteLeadCreateView.as_view(), name='clientelead_create'),
    path('leads/<int:pk>/editar/', views.ClienteLeadUpdateView.as_view(), name='clientelead_update'),
    path('leads/<int:pk>/excluir/', views.ClienteLeadDeleteView.as_view(), name='clientelead_delete'),

    # Day-Use
    path('dayuse/', views.ClienteDayUseListView.as_view(), name='clientedayuse_list'),
    path('dayuse/novo/', views.ClienteDayUseCreateView.as_view(), name='clientedayuse_create'),
    path('dayuse/<int:pk>/editar/', views.ClienteDayUseUpdateView.as_view(), name='clientedayuse_update'),
    path('dayuse/<int:pk>/excluir/', views.ClienteDayUseDeleteView.as_view(), name='clientedayuse_delete'),

    # Locadores
    path('locadores/', views.ClienteLocadorListView.as_view(), name='clientelocador_list'),
    path('locadores/novo/', views.ClienteLocadorCreateView.as_view(), name='clientelocador_create'),
    path('locadores/<int:pk>/editar/', views.ClienteLocadorUpdateView.as_view(), name='clientelocador_update'),
    path('locadores/<int:pk>/excluir/', views.ClienteLocadorDeleteView.as_view(), name='clientelocador_delete'),
]
