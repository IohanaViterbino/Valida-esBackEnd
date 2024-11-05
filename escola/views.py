from escola.models import Estudante, Curso, Matricula
from escola.serializers import (
    EstudanteSerializer,CursoSerializer, MatriculaSerializer,
    ListaMatriculasEstudanteSerializer,ListaMatriculasCursoSerializer, EstudanteSerializerV2
)
from rest_framework import viewsets, generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.throttling import UserRateThrottle
from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework.versioning import NamespaceVersioning

@extend_schema(
    tags=["Estudante"],
    responses={
        200: EstudanteSerializer,  # Response de sucesso ao obter dados do estudante
        400: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "nome": {"type": "string", "example": "O nome deve conter apenas letras!"},
                    "email": {"type": "string", "example": "O email não está no formato correto!"},
                    "cpf": {"type": "string", "example": "O cpf deve ter 11 digitos numéricos válidos!"},
                    "data_nascimento": {
                        "type": "string", 
                        "example": "A data de nascimento não pode ser maior que a data atual!"
                    },
                    "celular": {"type": "string", "example": "O celular precisa ter 13 digitos!"},
                },
            },
            description="Erros de validação dos campos fornecidos."
        ),
        404: OpenApiResponse(
            description="Estudante não encontrado."
        ),
    },
    description="Endpoint para o CRUD de estudantes. Retorna detalhes de validação e possíveis erros.",
)
class EstudanteViewSet(viewsets.ModelViewSet):
    queryset = Estudante.objects.all().order_by('nome')
    serializer_class = EstudanteSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['nome']
    search_fields = ['nome', 'cpf']

@extend_schema(
    tags=["Curso"],
    responses={
        200: CursoSerializer,  # Response de sucesso ao obter dados do estudante
        400: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "codigo": {"type": "string", "example": "O código deve ter no mínimo 3 caracteres!"},
                    "descricao": {"type": "string", "example": "A descrição deve ter entre 10 e 100 caracteres!"},
                },
            },
            description="Erros de validação dos campos fornecidos."
        ),
        404: OpenApiResponse(
            description="Curso não encontrado."
        ),
    },
    description="Endpoint para o CRUD de cursos. Retorna detalhes de validação e possíveis erros.",
)
class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all().order_by('codigo')
    serializer_class = CursoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['codigo', 'nivel']
    search_fields = ['codigo', 'nivel']

@extend_schema(
    tags=["Matricula"],
    responses={
        200: MatriculaSerializer,  # Response de sucesso ao obter dados do estudante
        400: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "periodo": {"type": "string", 
                                "example": "Já existe uma matrícula desse estudante nesse período!"},
                },
            },
            description="Erros de validação dos campos fornecidos."
        ),
        404: OpenApiResponse(
            description="Matricula não encontrado."
        ),
    },
    description="Endpoint para o CRUD de matrículas. Retorna detalhes de validação e possíveis erros.",
)
class MatriculaViewSet(viewsets.ModelViewSet):
    queryset = Matricula.objects.all().order_by('-id')
    serializer_class = MatriculaSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['periodo']
    search_fields = ['periodo']
    throttle_classes = [UserRateThrottle]

@extend_schema(tags=["Lista de Matriculas do estudante"])
class ListaMatriculaEstudante(generics.ListAPIView):
    def get_queryset(self):
        queryset = Matricula.objects.filter(estudante_id=self.kwargs['pk']).order_by('periodo')
        return queryset
    serializer_class = ListaMatriculasEstudanteSerializer

@extend_schema(tags=["Lista de Matriculas do curso"])
class ListaMatriculaCurso(generics.ListAPIView):
    def get_queryset(self):
        queryset = Matricula.objects.filter(curso_id=self.kwargs['pk']).order_by('estudante__nome')
        return queryset
    serializer_class = ListaMatriculasCursoSerializer