from django.urls import path
from .views import DashboardsView, MultilineIncidentTop3Country, multipleBarbySeverity, DataByYear, StationCount, FireTruckCount, FireFighterCount, IncidentCount, LocationCount, WeatherCount

urlpatterns = [
    path("", DashboardsView.as_view(template_name="dashboard_analytics.html"), name="index",),
    path('DataByYear/', DataByYear, name='incidents_by_year'),
    path('multilineChart/', MultilineIncidentTop3Country, name='chart'),
    path('multiBarChart/', multipleBarbySeverity, name='chart'),
    path('stationCount/', StationCount, name='station_count'),
    path('fireTruckCount/', FireTruckCount, name='fire_truck_count'),
    path('fireFighterCount/', FireFighterCount, name='firefighter_count'),
    path('incidentCount/', IncidentCount, name='incident_count'),
    path('locationCount/', LocationCount, name='location_count'),
    path('weatherCount/', WeatherCount, name='weather_count'),
]
