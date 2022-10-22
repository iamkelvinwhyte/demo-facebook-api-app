from rest_framework import permissions
from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
import coreapi
from rest_framework.schemas import AutoSchema

schema_view = get_schema_view(
   openapi.Info(
      title="FACEBOOK API",
      default_version='1.0.0',
      description="Django Restful API",
      terms_of_service="h",
      contact=openapi.Contact(email="odafeky42@gmail.com"),
      license=openapi.License(name="Kelvin License"),
   ),
   public=True,
   # permission_classes=(permissions.AllowAny,),
)

