from escola.models import Estudante, Curso, Matricula
from escola.serializers import (
    EstudanteSerializer,CursoSerializer, MatriculaSerializer,
    ListaMatriculasEstudanteSerializer,ListaMatriculasCursoSerializer, EstudanteSerializerV2
)
from rest_framework import viewsets, generics, filters, versioning
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.throttling import UserRateThrottle

class EstudanteViewSet(viewsets.ModelViewSet):
    queryset = Estudante.objects.all().order_by('-id')
    # serializer_class = EstudanteSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['nome']
    search_fields = ['nome', 'cpf']
    versioning_class = versioning.QueryParameterVersioning

    def get_serializer_class(self):
        if self.request.version == 'v2':
            return EstudanteSerializerV2
        return EstudanteSerializer

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['codigo', 'nivel']
    search_fields = ['codigo', 'nivel']

class MatriculaViewSet(viewsets.ModelViewSet):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['periodo']
    search_fields = ['periodo']
    throttle_classes = [UserRateThrottle]

class ListaMatriculaEstudante(generics.ListAPIView):
    def get_queryset(self):
        queryset = Matricula.objects.filter(estudante_id=self.kwargs['pk'])
        return queryset
    serializer_class = ListaMatriculasEstudanteSerializer

class ListaMatriculaCurso(generics.ListAPIView):
    def get_queryset(self):
        queryset = Matricula.objects.filter(curso_id=self.kwargs['pk'])
        return queryset
    serializer_class = ListaMatriculasCursoSerializer