from django.urls import path
from .views import DashboardsView, MultilineIncidentTop3Country, multipleBarbySeverity, DataByYear

urlpatterns = [
    path("", DashboardsView.as_view(template_name="dashboard_analytics.html"), name="index",), 
    path('multilineChart/', MultilineIncidentTop3Country, name='chart'),
    path('multiBarChart/', multipleBarbySeverity, name='chart'),
    path('DataByYear/', DataByYear, name='incidents_by_year'),
]
