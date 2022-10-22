from django.urls import path

from webapp import api_views
from webapp import api_document as webapp_api_document

urlpatterns = [

    # Defined URL
    path('api/auth/', api_views.CustomAuthToken.as_view(), name='auth'), 
    path('api/messages/', api_views.FaceBookApp.as_view(), name='messages'),
    path('api/messages/<int:message_id>/', api_views.FaceBookApp.as_view(), name='messages'),
    path('api/data/', api_views.GetFaceBookApp.as_view(), name='GetFaceBookApp'),
    

    path('', webapp_api_document.schema_view.with_ui(
        'swagger', cache_timeout=0), name='schema-swagger-ui'),
    
    
]
