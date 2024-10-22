from rest_framework import serializers
from escola.models import Estudante, Curso, Matricula
from .validators import *

class EstudanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudante
        fields = ['id','nome','email','cpf','data_nascimento','celular']    
    
    def validate(self, dados):
        if validate_nome(dados['nome']):
            raise serializers.ValidationError({'nome':'O nome deve conter apenas letras!'})
        if validate_email(dados['email']):
            raise serializers.ValidationError({'email':'O email não está no formato correto!'})
        if validate_cpf(dados['cpf']):
            raise serializers.ValidationError({'cpf':'O cpf deve ter 11 digitos numéricos válidos!'})
        if validate_data_nascimento(dados['data_nascimento']):
            raise serializers.ValidationError({'data_nascimento':'A data de nascimento não pode ser maior que a data atual!'})
        if validate_celular(dados['celular']):
            raise serializers.ValidationError({'celular':'O celular precisa ter 13 digitos!'})
        return dados

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'

    def validate(self, dados):
        if validate_codigo(dados['codigo']):
            raise serializers.ValidationError({'codigo':'O código deve ter no mínimo 3 caracteres!'})
        if validate_descricao(dados['descricao']):
            raise serializers.ValidationError({'descricao':'A descrição deve ter entre 10 e 100 caracteres!'})
        return dados

class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        exclude = []

    def validate(self, dados):
        if validate_periodo(dados):
            raise serializers.ValidationError({'periodo':'Já existe uma matrícula desse estudante nesse período!'})
        return dados

class ListaMatriculasEstudanteSerializer(serializers.ModelSerializer):
    curso = serializers.ReadOnlyField(source='curso.descricao')
    periodo = serializers.SerializerMethodField()
    class Meta:
        model = Matricula
        fields = ['curso','periodo']

    def get_periodo(self,obj):
        return obj.get_periodo_display()

class ListaMatriculasCursoSerializer(serializers.ModelSerializer):
    estudante_nome = serializers.ReadOnlyField(source = 'estudante.nome')
    class Meta:
        model = Matricula
        fields = ['estudante_nome']
        
class EstudanteSerializerV2(serializers.ModelSerializer):
    class Meta:
        model = Estudante
        fields = ['id','nome','email','celular']