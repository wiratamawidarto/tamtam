from rest_framework import serializers
from db_api.models import Yolo, Yolo_Files, Picture_Files

class YoloSerializer(serializers.HyperlinkedModelSerializer):
    # alert = serializers.BooleanField(required=False)
    # description = serializers.CharField(required=False)
    class Meta:
        model = Yolo
        # fields = '__all__'
        fields = ('id', 'title', 'timestamp')

class Yolo_Files_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Yolo_Files
        fields = ('id','yolo_id','image','created_at')

class Picture_Files_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Picture_Files
        fields = ('identifier', 'picture')


class Picture_Files_Serializer_PUSH(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Picture_Files
        # fields = ('identifier', 'picture')
        fields = ('picture')


    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['identifier'] = Yolo_Files_Serializer(instance.identifier).data
    #     return response


# class AlertYoloSerializer(serializers.HyperlinkedModelSerializer):
#     # description = serializers.CharField(required=False)
#     file = serializers.FileField(required=False)
#     class Meta:
#         model = Alert_Yolo
#         # fields = '__all__'
#         fields = ('id', 'title', 'timestamp', 'file')


class YoloSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Yolo
        fields = '__all__'
        # fields = ('id', 'title', 'timestamp')


# class AlertYoloSerializer2(serializers.ModelSerializer):
#     class Meta:
#         model = Alert_Yolo
#         fields = '__all__'
#         # fields = ('id', 'title')