from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.validators import ValidationError

class BaseViewSet(ModelViewSet):
    
    def get_queryset(self):
        return self.model_class.objects.all()

    # def get_serializer_class(self):
    #     return self.serializer_class
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(data={
                'status':True,
                'message':f"{self.instance_name} created successfully",
                'data':serializer.data 
            })

        return Response(data={
            'status':False,
            'message':f"{self.instance_name} failed",
            'data':serializer.errors
        })
    
    def list(self, request, *args, **kwargs):
        queryset = get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        return Response(data={
            'status':True,
            'message':f"{self.instance_name}'s list retrieved successfully",
            'data':serializer.data
        })
    
    def get_object(self, request, pk=None, *args, **kwargs):
        try:
            return self.model_class.objects.get(pk=pk)

        except self.model_class.DoesNotExist:
            raise ValidationError({
                'status': False,
                'message': f"{self.instance_name} was not found",
                "data": {}
            })
