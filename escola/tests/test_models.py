from django.test import TestCase
from escola.models import Estudante, Curso, Matricula

class ModelEstudanteTestCase(TestCase):
    def setUp(self):
        self.estudante = Estudante.objects.create(
            nome = 'Teste de Modelo',
            email = 'testedemodelo@gmail.com',
            cpf = '68195899056',
            data_nascimento = '2023-02-02',
            celular = '86 99999-9999'
        )
        
    def test_verifica_atributos_de_estudante(self):
        """Teste que verifica os atributos do modelo de Estudante"""
        self.assertEqual(self.estudante.nome,'Teste de Modelo')
        self.assertEqual(self.estudante.email,'testedemodelo@gmail.com')
        self.assertEqual(self.estudante.cpf,'68195899056')
        self.assertEqual(self.estudante.data_nascimento,'2023-02-02')
        self.assertEqual(self.estudante.celular,'86 99999-9999')

class ModelCursoTestCase(TestCase):
    def setUp(self):
        self.curso = Curso.objects.create(
            codigo = '001',
            descricao = 'Curso de Teste de Modelo',
            nivel = 'B'
        )
    def test_verifica_atributos_de_curso(self):
        """Teste que verifica os atributos do modelo de Curso"""
        self.assertEqual(self.curso.codigo,'001')
        self.assertEqual(self.curso.descricao,'Curso de Teste de Modelo')
        self.assertEqual(self.curso.nivel,'B')

class ModelMatriculaTestCase(TestCase):
    def setUp(self):
        self.curso = Curso.objects.create(
            codigo = '001',
            descricao = 'Curso de Teste de Modelo',
            nivel = 'B'
        )
        self.estudante = Estudante.objects.create(
            nome = 'Teste de Modelo',
            email = 'testedemodelo@gmail.com',
            cpf = '68195899056',
            data_nascimento = '2023-02-02',
            celular = '86 99999-9999'
        )
        self.matricula = Matricula.objects.create(
            estudante = self.estudante,
            curso = self.curso,
            periodo = 'M'
        )
    def test_verifica_atributos_de_matricula(self):
        """Teste que verifica os atributos do modelo de Matricula"""
        self.assertEqual(self.matricula.estudante.id,self.estudante.id)
        self.assertEqual(self.matricula.curso.id,self.curso.id)
        self.assertEqual(self.matricula.periodo,'M')