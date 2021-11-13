# from rest_framework.views import APIView
# from rest_framework.parsers import MultiPartParser, FormParser
#
# from rest_framework import status
# from .serializers import FileSerializer

# class FileView(APIView):
#     parser_classes = (MultiPartParser, FormParser)
#     def post(self, request, *args, **kwargs):
#         file_serializer = FileSerializer(data=request.data)
#         if file_serializer.is_valid():
#             file_serializer.save()
#             return Response(file_serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from db_api.models import Yolo, Yolo_Files, Picture_Files
from db_api.serializers import YoloSerializer, YoloSerializer2, Yolo_Files_Serializer, Picture_Files_Serializer
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

# class IsOwnerOrReadOnly(permissions.BasePermission):
#     """
#     自定义权限，只有创建者才能编辑
#     """

#     def has_object_permission(self, request, view, obj):
#         # Read permissions are allowed to any request,
#         # so we'll always allow GET, HEAD or OPTIONS requests.
#         if request.method in permissions.SAFE_METHODS:
#             return True

#         # Write permissions are only allowed to the owner of the snippet.
#         return obj.owner == request.user

# class YoloPostView(viewsets.ModelViewSet):
#     serializer_class = YoloSerializer2
#     def get_permissions(self):  #permission = create, update, delete, destroy
#         if self.action in ('update', 'retrieve', 'destroy',):
#             self.permission_classes = [IsAuthenticated]
#         elif self.action  in ('create',):
#             self.permission_classes = [IsAuthenticated]
#         else:
#             pass
#         return [permission() for permission in self.permission_classes]

#     # [GET]
#     def list(self, request, **kwargs):
#         return Response(status=status.HTTP_400_BAD_REQUEST)

#     # [POST]
#     def create(self, request, *args, **kwargs):
#       file_serializer = YoloSerializer2(data=request.data)
#       if file_serializer.is_valid():
#           file_serializer.save()
#           return Response(file_serializer.data, status=status.HTTP_201_CREATED)


    # def retrieve(self, request, *args, **kwargs):
    #     try:
    #         instance = self.get_object()
    #     except Exception as e:
    #         return Response({'message':str(e)})
    #     else:
    #         #any additional logic
    #         serializer = YoloSerializer2(instance, many=False)
    #         return Response({'data': serializer.data})

    # def update(self, request, *args, **kwargs):
    #     return Response(status=status.HTTP_400_BAD_REQUEST)


    # def destroy(self, request, *args, **kwargs):
    #     return Response(status=status.HTTP_400_BAD_REQUEST)



from rest_framework.permissions import SAFE_METHODS,  BasePermission

class PostUserWritePermission(BasePermission):
    message = 'Editing posts is restricted to the author only.'

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        #return obj.name == request.user
        return True


# by using the "modelviewsets" it automatically  provides `list`, `create`, `retrieve`,`update` and `destroy` actions.
class YoloFilesView(viewsets.ModelViewSet):
    permission_classes = [PostUserWritePermission]
    serializer_class = Yolo_Files_Serializer
    queryset = Yolo_Files.objects.all()

    #for custom queryset
    def get_queryset(self):
        return Yolo_Files.objects.all()

    #get item based on id
    def get_object(self, queryset = None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(Yolo_Files, id = item)


#so when yolo is ready to give us the picture, we use this API
class PictureFilesView(viewsets.ModelViewSet):
    permission_classes = [PostUserWritePermission]
    serializer_class = Picture_Files_Serializer
    queryset = Picture_Files.objects.all()

    # GET
    def list(self, request, **kwargs):
        files = Picture_Files.objects.all()
        file_serializer = YoloSerializer(files, many=True)

        return Response(file_serializer.data, status=status.HTTP_200_OK)

    # [POST]
    def create(self, request, *args, **kwargs):
      file_serializer = Picture_Files_Serializer(data=request.data)
      if file_serializer.is_valid():
          file_serializer.save()
          return Response(status=status.HTTP_201_CREATED)


    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception as e:
            return Response({'message':str(e)})
        else:
            #any additional logic
            serializer = Picture_Files_Serializer(instance, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)


    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_400_BAD_REQUEST)



class YoloView(viewsets.ModelViewSet):
    queryset = Yolo.objects.all()
    serializer_class = YoloSerializer

    # permission_classes = (IsAuthenticated,) #直接全部都要有權限
    # def get_permissions(self):  #permission = create, update, delete, destroy
    #     if self.action in ('update', 'retrieve', 'destroy',):
    #         self.permission_classes = [IsAuthenticated]
    #     elif self.action  in ('create',):
    #         self.permission_classes = [IsAuthenticated]
    #     else:
    #         pass
    #     return [permission() for permission in self.permission_classes]


    def get_permissions(self):
        if self.action not in ('list',):
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    # [GET]
    def list(self, request, **kwargs):
        files = Yolo.objects.all()
        file_serializer = YoloSerializer(files, many=True)

        return Response(file_serializer.data, status=status.HTTP_200_OK)

    # [POST]
    def create(self, request, *args, **kwargs):
      file_serializer = YoloSerializer2(data=request.data)
      if file_serializer.is_valid():
          file_serializer.save()
          return Response(status=status.HTTP_201_CREATED)
      else:
          print(file_serializer)
          return Response(status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception as e:
            return Response({'message':str(e)})
        else:
            #any additional logic
            serializer = YoloSerializer2(instance, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_400_BAD_REQUEST)

###################################################################

    # [PATCH]
    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.name = request.data.get("name")
    #     instance.save()

    #     serializer = self.get_serializer(instance)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)

    #     return Response(serializer.data)


    # @action(detail=True, methods=['get'])
    # def info(self, request, pk=None):
    #     file = get_object_or_404(Yolo, pk=pk)
    #     result = YoloSerializer2(file, many=False)
    #     # self.check_object_permissions(self.request, file)
    #     # result = {
    #     #     'remark': file.remark
    #     # }

    #     return Response(result.data, status=status.HTTP_200_OK)


    # @action(detail=False, methods=['get'])
    # def all_yolo(self, request):
    #     yolo = Yolo.objects.values_list('id', flat=True).distinct()
    #     return Response(yolo, status=status.HTTP_200_OK)


# class AlertYoloView(viewsets.ModelViewSet):
#     queryset = Alert_Yolo.objects.all()
#     serializer_class = AlertYoloSerializer
#     # permission_classes = (IsAuthenticated,) #直接全部都要有權限
#     def get_permissions(self):  #permission = create, update, delete, destroy
#         if self.action not in ('list',):
#             self.permission_classes = [IsAuthenticated]
#         return [permission() for permission in self.permission_classes]

#     # [GET]
#     def list(self, request, **kwargs):
#         files = Alert_Yolo.objects.all()
#         file_serializer = AlertYoloSerializer(files, many=True)

#         return Response(file_serializer.data, status=status.HTTP_200_OK)

#     # [POST]
#     def create(self, request, *args, **kwargs):
#     #   file_serializer = AlertYoloSerializer2(data=request.data)
#     #   if file_serializer.is_valid():
#     #       file_serializer.save()
#     #       return Response(file_serializer.data, status=status.HTTP_201_CREATED)
#         return Response(status=status.HTTP_400_BAD_REQUEST)


#     def retrieve(self, request, *args, **kwargs):
#         try:
#             instance = self.get_object()
#         except Exception as e:
#             return Response({'message':str(e)})
#         else:
#             #any additional logic
#             serializer = AlertYoloSerializer2(instance, many=False)
#             return Response({'data': serializer.data})


#     def update(self, request, *args, **kwargs):
#         return Response(status=status.HTTP_400_BAD_REQUEST)


#     def destroy(self, request, *args, **kwargs):
#         return Response(status=status.HTTP_400_BAD_REQUEST)

#   def destroy(self, request, *args, **kwargs):
#       pass

#   def update(self, request, *args, **kwargs):
#       pass


    # @action(detail=True, methods=['get'])
    # def info(self, request, pk=None):
    #     file = get_object_or_404(Alert_Yolo, pk=pk)
    #     result = AlertYoloSerializer2(file, many=False)
    #     # self.check_object_permissions(self.request, file)

    #     return Response(result.data, status=status.HTTP_200_OK)


    # @action(detail=False, methods=['get'])
    # def all_alert(self, request):
    #     alert = Alert_Yolo.objects.values_list('id', flat=True).distinct()
    #     return Response(alert, status=status.HTTP_200_OK)




''' #############################################################'''
# class FileView(viewsets.ModelViewSet):
#     queryset = File.objects.all()
#     serializer_class = FileSerializer
#     # permission_classes = (IsAuthenticated,) #直接全部都要有權限
#     def get_permissions(self):
#         if self.action in ('create',):
#             self.permission_classes = [IsAuthenticated]
#         return [permission() for permission in self.permission_classes]

#     # [GET] api/shares/
#     def list(self, request, **kwargs):
#         files = File.objects.all()
#         serializer = FileSerializer(files, many=True)

#         return Response(serializer.data, status=status.HTTP_200_OK)

#     # [POST] api/shares/
#     def create(self, request, *args, **kwargs):
#       file_serializer = FileSerializer(data=request.data)
#       if file_serializer.is_valid():
#           file_serializer.save()
#           return Response(file_serializer.data, status=status.HTTP_201_CREATED)

#     @action(detail=True, methods=['get'])
#     def detail2(self, request, pk=None):
#         # result = FileSerializer(result, many=False)
#         file = get_object_or_404(File, pk=pk)
#         # result = FileSerializer(file.remark, many=False)
#         result = {
#             'remark': file.remark
#         }

#         return Response(result, status=status.HTTP_200_OK)

#     @action(detail=False, methods=['get'])
#     def all_remark(self, request):
#         remark = File.objects.values_list('remark', flat=True).distinct()
#         return Response(remark, status=status.HTTP_200_OK)
''' #############################################################'''
    # @action(detail=False)
    # def recent_users(self, request):
    #     recent_users = User.objects.all().order_by('-last_login')

    #     page = self.paginate_queryset(recent_users)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)

    #     serializer = self.get_serializer(recent_users, many=True)
    #     return Response(serializer.data)
