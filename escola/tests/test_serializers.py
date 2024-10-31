from django.test import TestCase
from escola.models import Estudante, Curso, Matricula
from escola.serializers import EstudanteSerializer, CursoSerializer, MatriculaSerializer
from datetime import date

class SerializerEstudanteTestCase(TestCase):
    def setUp(self):
        self.estudante_instacia = Estudante(
            nome = 'Teste de Serializer',
            email = 'testedeserializar@gmail.com',
            cpf = '68195899056',
            data_nascimento = '2023-02-02',
            celular = '86 99999-9999'
        )

        self.estudante_data = {
            'nome': 'Teste de Serializer denovo',
            'email': 'teste2deserializar@gmail.com',
            'cpf': '04540361082',
            'data_nascimento': '2013-02-02',
            'celular': '65 98888-8888'
        }

    def test_verifica_campos_serializados_instaciado(self):
        """Teste que verifica os campos serializados da instacia de Estudante"""
        serializer = EstudanteSerializer(instance=self.estudante_instacia)
        self.assertEqual(set(serializer.data.keys()), set(['id','nome', 'email', 'cpf', 'data_nascimento', 'celular']))
    
    def test_verifica_campos_serializados_com_dados(self):
        """Teste que verifica os campos serializados com dados"""
        serializer = EstudanteSerializer(data=self.estudante_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(set(serializer.validated_data.keys()), set(['nome', 'email', 'cpf', 'data_nascimento', 'celular']))

    def test_verifica_dados_serializados_instaciado(self):
        """Teste que verifica os dados serializados da instacia de Estudante"""
        serializer = EstudanteSerializer(instance=self.estudante_instacia)

        self.assertEqual(serializer.data['nome'], 'Teste de Serializer')
        self.assertEqual(serializer.data['email'], 'testedeserializar@gmail.com')
        self.assertEqual(serializer.data['cpf'], '68195899056')
        self.assertEqual(serializer.data['data_nascimento'], '2023-02-02')
        self.assertEqual(serializer.data['celular'], '86 99999-9999')
    
    def test_verifica_dados_serializados_com_dados(self):
        """Teste que verifica os dados serializados com dados"""
        serializer = EstudanteSerializer(data=self.estudante_data)
        self.assertTrue(serializer.is_valid())
        
        self.assertEqual(serializer.validated_data['nome'], 'Teste de Serializer denovo')
        self.assertEqual(serializer.validated_data['email'], 'teste2deserializar@gmail.com')
        self.assertEqual(serializer.validated_data['cpf'], '04540361082')
        self.assertEqual(serializer.validated_data['data_nascimento'], date(2013, 2, 2))
        self.assertEqual(serializer.validated_data['celular'], '65 98888-8888')

class SerializerCursoTestCase(TestCase):
    def setUp(self):
        self.curso_instacia = Curso(
            codigo = '001',
            descricao = 'Curso de Teste de Serializer',
            nivel = 'B'
        )

        self.curso_data = {
            'codigo': '002',
            'descricao': 'Curso de Teste de Serializer denovo',
            'nivel': 'I'
        }

    def test_verifica_campos_serializados_instaciado(self):
        """Teste que verifica os campos serializados da instacia de Curso"""
        serializer = CursoSerializer(instance=self.curso_instacia)
        self.assertEqual(set(serializer.data.keys()), set(['id','codigo', 'descricao', 'nivel']))
    
    def test_verifica_campos_serializados_com_dados(self):
        """Teste que verifica os campos serializados com dados"""
        serializer = CursoSerializer(data=self.curso_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(set(serializer.validated_data.keys()), set(['codigo', 'descricao', 'nivel']))

    def test_verifica_dados_serializados_instaciado(self):
        """Teste que verifica os dados serializados da instacia de Curso"""
        serializer = CursoSerializer(instance=self.curso_instacia)

        self.assertEqual(serializer.data['codigo'], '001')
        self.assertEqual(serializer.data['descricao'], 'Curso de Teste de Serializer')
        self.assertEqual(serializer.data['nivel'], 'B')
    
    def test_verifica_dados_serializados_com_dados(self):
        """Teste que verifica os dados serializados com dados"""
        serializer = CursoSerializer(data=self.curso_data)
        self.assertTrue(serializer.is_valid())
        
        self.assertEqual(serializer.validated_data['codigo'], '002')
        self.assertEqual(serializer.validated_data['descricao'], 'Curso de Teste de Serializer denovo')
        self.assertEqual(serializer.validated_data['nivel'], 'I')
        
class SerializerMatriculaTestCase(TestCase):
    def setUp(self):
        # Salvando as instâncias para garantir que IDs sejam gerados
        self.curso_instacia = Curso.objects.create(
            codigo='001',
            descricao='Curso de Teste de Serializer',
            nivel='B'
        )
        
        self.estudante_instacia = Estudante.objects.create(
            nome='Teste de Serializer',
            email='testedeserializar@gmail.com',
            cpf='68195899056',
            data_nascimento='2023-02-02',
            celular='86 99999-9999'
        )

        # Instância da matrícula para serialização
        self.matricula_instacia = Matricula.objects.create(
            estudante=self.estudante_instacia,
            curso=self.curso_instacia,
            periodo='M'
        )

        # Dados para teste de serialização
        self.matricula_data = {
            'estudante': self.estudante_instacia.id,
            'curso': self.curso_instacia.id,
            'periodo': 'V'
        }

    def test_verifica_campos_serializados_instaciado(self):
        """Teste que verifica os campos serializados da instacia de Matricula"""
        serializer = MatriculaSerializer(instance=self.matricula_instacia)
        self.assertEqual(set(serializer.data.keys()), set(['id', 'estudante', 'curso', 'periodo']))

    def test_verifica_campos_serializados_com_dados(self):
        """Teste que verifica os campos serializados com dados"""
        serializer = MatriculaSerializer(data=self.matricula_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(set(serializer.validated_data.keys()), set(['estudante', 'curso', 'periodo']))

    def test_verifica_dados_serializados_instaciado(self):
        """Teste que verifica os dados serializados da instacia de Matricula"""
        serializer = MatriculaSerializer(instance=self.matricula_instacia)

        self.assertEqual(serializer.data['estudante'], self.estudante_instacia.id)
        self.assertEqual(serializer.data['curso'], self.curso_instacia.id)
        self.assertEqual(serializer.data['periodo'], 'M')
    
    def test_verifica_dados_serializados_com_dados(self):
        """Teste que verifica os dados serializados com dados"""
        serializer = MatriculaSerializer(data=self.matricula_data)
        self.assertTrue(serializer.is_valid())
        
        # Corrigido para comparar com IDs, pois validated_data retorna os IDs dos relacionamentos
        self.assertEqual(serializer.validated_data['estudante'], self.estudante_instacia)
        self.assertEqual(serializer.validated_data['curso'], self.curso_instacia)
        self.assertEqual(serializer.validated_data['periodo'], 'V')
