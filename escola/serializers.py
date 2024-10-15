from rest_framework import serializers
from validate_docbr import CPF
import re, datetime
from escola.models import Estudante, Curso, Matricula

class EstudanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudante
        fields = ['id','nome','email','cpf','data_nascimento','celular']    
    
    def validate(self, dados):
        cpf = CPF()
        regex_email = re.compile(r'[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?', re.IGNORECASE)
        regex_nome = re.compile(r'^[a-zA-Z\s]*$', re.IGNORECASE)

        if re.match(regex_email, dados['email']) == None:
            raise serializers.ValidationError({'email':'O email não está no formato correto!'})
        if dados['data_nascimento'] > datetime.date.today():
            raise serializers.ValidationError({'data_nascimento':'A data de nascimento não pode ser maior que a data atual!'})
        if len(dados['celular']) != 13:
            raise serializers.ValidationError({'celular':'O celular precisa ter 13 digitos!'})
        if re.match(regex_nome, dados['nome']) == None:
            raise serializers.ValidationError({'nome':'O nome deve conter apenas letras!'})
        if not cpf.validate(dados['cpf']):
            raise serializers.ValidationError({'cpf':'O cpf deve ter 11 digitos numéricos válidos!'})
        return dados


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'

class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        exclude = []

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
        
        
        