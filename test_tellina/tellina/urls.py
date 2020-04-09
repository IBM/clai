"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse

from website import annotator, cmd2html, views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^index$', views.index),
    url(r'^translate$', views.translate),
    url(r'^load_example_requests_with_translations', views.example_requests_with_translations),
    url(r'^load_latest_requests_with_translations', views.latest_requests_with_translations),
    url(r'^developers$', views.developers),

    url(r'^remember_ip_address$', views.remember_ip_address),
    url(r'^vote$', views.vote),

    url(r'^explain_cmd$', cmd2html.explain_cmd),

    url(r'^login$', annotator.login),
    url(r'^register_user', annotator.register_user),
    url(r'^user_login$', annotator.user_login),
    url(r'^logout$', annotator.user_logout),

    url(r'^url_panel$', annotator.url_panel),
    url(r'^utility_panel$', annotator.utility_panel),

    url(r'^collect_page$', annotator.collect_page),
    url(r'^previous_url$', annotator.previous_url),
    url(r'^next_url$', annotator.next_url),
    url(r'^submit_annotation$', annotator.submit_annotation),
    url(r'^submit_edit$', annotator.submit_edit),
    url(r'^delete_annotation$', annotator.delete_annotation),
    url(r'^mark_duplicate$', annotator.mark_duplicate),
    url(r'^mark_wrong$', annotator.mark_wrong),
    url(r'^mark_i_dont_know', annotator.mark_i_dont_know),
    url(r'^update_progress$', annotator.update_progress),

    url(r'^accept_update', annotator.accept_update),
    url(r'^retract_update', annotator.retract_update),
    url(r'^submit_annotation_update', annotator.submit_annotation_update),
    url(r'^get_relevant_updates', annotator.get_relevant_updates),
    url(r'^get_update_status', annotator.get_update_status),
    url(r'^get_url_stats', annotator.get_url_stats),
    url(r'^get_utility_stats', annotator.get_utility_stats),
    url(r'^get_utility_num_notifications', annotator.get_utility_num_notifications),
    url(r'^get_url_num_notifications', annotator.get_url_num_notifications),
    url(r'^reject_update', annotator.reject_update),

    url(r'user_panel', annotator.user_panel),
    url(r'user_profile', annotator.user_profile),
    url(r'update_user_time_logged', annotator.update_user_time_logged),

    url(r'^robots.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),

    url(r'^admin', admin.site.urls)
]
