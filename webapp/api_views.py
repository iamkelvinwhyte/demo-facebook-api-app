
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator 
from django.views.decorators.cache import cache_page
from rest_framework import status
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .serializers import MessageSerializer,MassageValidation,likeValidation
from webapp.models import Messages,query_message_report_by_args
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from facebook_scraper import get_posts



class CustomAuthToken(ObtainAuthToken):
    """
    Custom token class for generating authentication token for  api endpoint  
    """
    @swagger_auto_schema(request_body=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        required=['username','password'],
                        properties={
                            'username': openapi.Schema(type=openapi.TYPE_STRING,description="Username"),
                            'password': openapi.Schema(type=openapi.TYPE_STRING,description="Password"),
                        },
                    ))
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({"status": "success", "message": "Login Successful", "data": {
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }}, status=status.HTTP_200_OK)


@method_decorator(cache_page(60 * 5), name='dispatch') 
class FaceBookApp(APIView):
    """
    This module provides various functions to Post  and Retrieves facebook post data.
    """
    permission_classes = [IsAuthenticated]
    parameters_start_date=openapi.Parameter('start_date',in_=openapi.IN_QUERY,description="Start Date",type=openapi.TYPE_STRING)
    parameters_end_date=openapi.Parameter('end_date',in_=openapi.IN_QUERY,description="End Date",type=openapi.TYPE_STRING)
    parameters_value=openapi.Parameter('no_likes',in_=openapi.IN_QUERY,description="Number of Likes",type=openapi.TYPE_INTEGER)
    parameters_value=openapi.Parameter('post_category',in_=openapi.IN_QUERY,description="The message category",type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[parameters_start_date,parameters_end_date,parameters_value])
    def get(self, request, message_id=None):
        """
        Retrieve single/multiple objects from the Message Table based on Message ID and Filter parameter.
         ----------
        :param date start_date:  The starting date of the message report 
        :param date end_date: The ending date of the message report 
        :param likes no_likes: The number of  likes for each messages
        :param category post_category: The message category 
        """
        if message_id:
            try:
                get_message = Messages.objects.get(id=message_id)
            except ObjectDoesNotExist:
                return Response({"status": "RecordNotFound"}, status=status.HTTP_404_NOT_FOUND)
            message_serializer = MessageSerializer(get_message)
            return Response({"data": message_serializer.data}, status=status.HTTP_200_OK)

        if 'start_date' in request.query_params or 'end_date' in request.query_params:
            serializer_data=MassageValidation(data=request.query_params)
            if not serializer_data.is_valid():
                return Response(serializer_data.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
            try:
                get_message_report=query_message_report_by_args(**request.query_params)
            except ValueError:
                return Response(status=status.HTTP_404_NOT_FOUND)   
            message_report_serializer = MessageSerializer(get_message_report, many=True)
            return Response({"data": message_report_serializer.data}, status=status.HTTP_200_OK)

        if 'no_likes' in request.query_params:
            serializer_data=likeValidation(data=request.query_params)
            if not serializer_data.is_valid():
                return Response(serializer_data.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
            try:
                get_message_report=query_message_report_by_args(**request.query_params)
            except ValueError:
                return Response(status=status.HTTP_404_NOT_FOUND)   
            message_report_serializer = MessageSerializer(get_message_report, many=True)
            return Response({"data": message_report_serializer.data}, status=status.HTTP_200_OK)

        if 'post_category' in request.query_params:
    
            try:
                get_message_report=query_message_report_by_args(**request.query_params)
            except ValueError:
                return Response(status=status.HTTP_404_NOT_FOUND)   
            message_report_serializer = MessageSerializer(get_message_report, many=True)
            return Response({"data": message_report_serializer.data}, status=status.HTTP_200_OK)
            
        get_message = Messages.objects.all().order_by('-id')
        sensor_serializer = MessageSerializer(get_message, many=True)
        return Response({"data": sensor_serializer.data}, status=status.HTTP_200_OK)




@method_decorator(cache_page(60 * 5), name='dispatch') 
class GetFaceBookApp(APIView):
    """
    This module GET data from  facebook page . 
    """
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        required=['facebook_page_name'],
                        properties={
                            'facebook_page_name': openapi.Schema(type=openapi.TYPE_STRING,description="Facebook Page Name")
                        },
                    ))
    def post(self, request):

        if 'facebook_page_name' not in request.data:
            return Response({"message": "id is required"}, status=status.HTTP_404_NOT_FOUND)  
        try:
            get_all_post= get_posts(request.data['facebook_page_name'], cookies='cookies_file.txt',extra_info=True,pages=1, options={"comments":True})
        except ValueError:
            return Response({"status": "Unable to Fetch data"}, status=status.HTTP_404_NOT_FOUND)

        for post in get_all_post:
            comments=post['comments']
            post_text=post['post_text']
            image=post['image']
            like=post['likes']
            shared_time=post['shared_time']
            post_url=post['post_url']
            post_id=post['post_id']
            for comment in comments:
                 obj= Messages(post=comment,no_likes=like,post_thumbnail=image,title=post_text,post_id=post_id,post_url=post_url,post_date=shared_time)
            obj.save()     
            return Response({"data": 'successful'}, status=status.HTTP_200_OK)
