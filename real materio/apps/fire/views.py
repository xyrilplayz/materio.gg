from django.views.generic import TemplateView
from web_project import TemplateLayout
from .models import FireStation
from django.views.generic.list import ListView
from django.db import connection
from django.http import JsonResponse


"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to dashboards/urls.py file for more pages.
"""

class DashboardsView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context
    
def MultilineIncidentTop3Country(request):
    query = '''
    WITH top_countries AS (
        SELECT fl.country
        FROM fire_incident fi
        JOIN fire_locations fl ON fi.location_id = fl.id
        WHERE strftime('%Y', fi.date_time) = strftime('%Y', 'now')
        GROUP BY fl.country
        ORDER BY COUNT(fi.id) DESC
        LIMIT 3
    )
    SELECT 
        fl.country, 
        strftime('%m', fi.date_time) AS month, 
        COUNT(fi.id) AS incident_count
    FROM 
        fire_incident fi
    JOIN 
        fire_locations fl ON fi.location_id = fl.id
    WHERE 
        fl.country IN (SELECT country FROM top_countries)
        AND strftime('%Y', fi.date_time) = strftime('%Y', 'now')
    GROUP BY 
        fl.country, month
    ORDER BY 
        fl.country, month;
    '''
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    months = [str(i).zfill(2) for i in range(1, 13)]
    result = {}

    for country, month, count in rows:
        if country not in result:
            result[country] = {m: 0 for m in months}
        result[country][month] = count

    if len(result) < 3:
        placeholders_needed = 3 - len(result)
        for i in range(placeholders_needed):
            placeholder_rank = len(result) + 1
            result[f"No Top {placeholder_rank}"] = {m: 0 for m in months}

    for country in result:
        result[country] = dict(sorted(result[country].items()))

    return JsonResponse(result)

def multipleBarbySeverity(request):
    query = '''
        SELECT
            fi.severity_level,
            strftime('%m', fi.date_time) AS month,
            COUNT(fi.id) AS incident_count
        FROM
            fire_incident fi
        GROUP BY fi.severity_level, month
        '''

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    result = {}
    months = set(str(i).zfill(2) for i in range(1, 13))

    for row in rows:
        level = str(row[0])  # Ensure the severity level is a string
        month = row[1]
        total_incidents = row[2]

        if level not in result:
            result[level] = {month: 0 for month in months}

        result[level][month] = total_incidents

    # Sort months within each severity level
    for level in result:
        result[level] = dict(sorted(result[level].items()))

    return JsonResponse(result)