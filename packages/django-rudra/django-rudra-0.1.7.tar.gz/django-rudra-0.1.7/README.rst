=====
Rudra
=====

What problem does it solve?
---------------------------

#. It's a simple django package which can help developers to create APIs faster without writing views.

#. It works quite similar to GraphQL, but it's not GraphQL. It's just a simple package which can help you to create APIs with url configurations only.

#. So next time when you want to create an API, you don't need to write views, you just need to write url configurations.

#. Even frontend folks can create or tweak APIs without writing views.


Setup
-----

1. In ``urls.py``::

    from django.urls import path, include

    urlpatterns = [
        path('rudra/', include('rudra.urls')),
    ]

2. In ``somepath/response.py``::

    '''
        Sample success and error response functions
        Configure how you want to return success and error responses
    '''

    from typing import Union
    from django.http import JsonResponse

    def success_response(data: Union[dict, list], has_next: bool = None, pages: int = None, count: int = None, page_size: int = None) -> JsonResponse:
        '''
            :param data: either dict or list, depending on the response
            :param has_next: if the response is paginated, then this will be True or False
        '''
        return JsonResponse({'data': data, 'status': 'success', 'has_next': has_next. 'pages': pages, 'count': count, 'page_size': page_size})

    def error_response(error: Exception) -> JsonResponse:
        return JsonResponse({'error': str(error), 'status': 'error'})

3. In ``settings.py``::

    '''
        Configure Rudra settings
        Register your models with serializer in settings
    '''

    from rudra.settings import RudraBaseSettings, RudraMetaSettings, SerializerSettings

    # other settings
    ...
    
    INSTALLED_APPS = [
        ...
        'rudra',
    ]

    # other settings
    ...

    class RudraSettings(RudraBaseSettings):
        success_path = 'somepath/response.success_response'
        error_path = 'somepath/response.error_response'
        user_serializer_path = 'user.serializer.UserSerializer' # Serializer to be used for user model
        fixed_page_number = 9999999 # If you want to set a fixed page number for pagination

        # Register your models here
        # You can pass multiple models and their configurations in this list
        meta_settings = [
            RudraMetaSettings(
                model_path='django.contrib.auth.models.User',
                methods_allowed=['get', 'post', 'put', 'patch', 'delete'],
                
                # Either pass serializer_path or map_serializer
                # with map_serializer, you can pass different serializers for different request methods
                # with serializer_context you can pass context to serializer
                serializer_settings=SerializerSettings(
                    serializer_path='user.serializer.UserSerializer',
                    serializer_context=lambda request: {'request': request},
                    map_serializer={
                        'get': 'user.serializer.UserSerializerGet',
                        'post': 'user.serializer.UserSerializerPost',
                    }
                )
            )
        ]

    RUDRASETTINGS = RudraSettings()

How to use
----------

1. Get all registered models and their configurations::

    GET: https://{{base_url}}/rudra/models

    Sample Response:
    # Note: Response will contain json with key as model and value will be the list of fiedls(and their configurations) 
    {
        "User": [
            {
                "name": "logentry",
                "type": "ForeignKey",
                "related_model": "LogEntry",
                "description": null
            },
            {
                "name": "id",
                "type": "AutoField",
                "related_model": null,
                "description": "Integer"
            },
            {
                "name": "password",
                "type": "CharField",
                "related_model": null,
                "description": "String (up to %(max_length)s)"
            },
            {
                "name": "last_login",
                "type": "DateTimeField",
                "related_model": null,
                "description": "Date (with time)"
            },
            {
                "name": "is_superuser",
                "type": "BooleanField",
                "related_model": null,
                "description": "Boolean (Either True or False)"
            },
            {
                "name": "username",
                "type": "CharField",
                "related_model": null,
                "description": "String (up to %(max_length)s)"
            },
            {
                "name": "first_name",
                "type": "CharField",
                "related_model": null,
                "description": "String (up to %(max_length)s)"
            },
            {
                "name": "last_name",
                "type": "CharField",
                "related_model": null,
                "description": "String (up to %(max_length)s)"
            },
            {
                "name": "email",
                "type": "CharField",
                "related_model": null,
                "description": "Email address"
            },
            {
                "name": "is_staff",
                "type": "BooleanField",
                "related_model": null,
                "description": "Boolean (Either True or False)"
            },
            {
                "name": "is_active",
                "type": "BooleanField",
                "related_model": null,
                "description": "Boolean (Either True or False)"
            },
            {
                "name": "date_joined",
                "type": "DateTimeField",
                "related_model": null,
                "description": "Date (with time)"
            },
            {
                "name": "groups",
                "type": "ManyToManyField",
                "related_model": "Group",
                "description": "Many-to-many relationship"
            },
            {
                "name": "user_permissions",
                "type": "ManyToManyField",
                "related_model": "Permission",
                "description": "Many-to-many relationship"
            }
        ]
    }

2. Querying models::

    GET: https://{{base_url}}/rudra/{{model_name}}
    Query Params:
    # add your filters in query params 
    {
        'pk': 1,
        'username': 'admin',
        'email': 'someemail@email.com',
        ...
        # you can add any field name and its value
        # you can also add filters similar to django queryset
        # for example:
        'username__icontains': 'ad',
        
        # you can also add pagination
        'page': 1,
        'page_size': 10,

        # you can also add ordering
        'order_by': 'username',

        # if you want to receive all results, then
        'all': True
        # else you will receive only single result
    }

3. Use other request methods::

    {{METHOD}}: https://{{base_url}}/rudra/{{model_name}}

    # Note: You can use any request method, eg: POST, PUT, PATCH, DELETE

    # Note: You can also pass data in request body

    # Note: For DELETE request, make sure you pass filters in request body

4. Deep query models::

    # This api is used to query models with more configurations
    # More configurations will be added soon

    POST: https://{{base_url}}/rudra/query/{{model_name}}/
    Query Params:
    {
        'page': 1,
        'page_size': 10,
        'all': True # if you want to receive all results
        # don't pass anything if you want to receive single result
    }

    BODY:
    {
        'or_filters': {
            # Add your or filters here
            'pk': 1,
            'username': 'admin',
            'email': 'someemail@email.com',
            'last_name': null
        },
        'filters': {
            # Add your filters here
            'pk': 1,
            'username': 'admin',
            'email': 'someemail@email.com',
            'last_name': null
        },
        'order_by_list': [
            'id',
            '-username',
        ],
        'select_related': [
            'logentry',
            'groups',
            'user_permissions',
        ],
        'prefetch_related': [
            'logentry',
            'groups',
            'user_permissions',
        ],
    }

5. Get User::

    GET: https://{{base_url}}/rudra/get-user/
