from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from escola.models import Matricula, Estudante, Curso
from django.contrib.auth.models import User

class MatriculaAPITestCase(APITestCase):
    def setUp(self):
        # Criando um usuário para autenticação, caso necessário
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        
        # Criando um estudante para os testes de leitura e atualização
        self.curso = Curso.objects.create(
            codigo='PB008',
            descricao='Python backend curso de servidor em Django Rest Framework',
            nivel='I',
        )
        # Criando um estudante para os testes de leitura e atualização
        self.estudante = Estudante.objects.create(
            nome='João Silva',
            email='joao.silva@example.com',
            cpf='12345678901',
            data_nascimento='2000-01-01',
            celular = "1386549835788"
        )

        self.matriculas = Matricula.objects.create(
            estudante=self.estudante,
            curso=self.curso,
            periodo='M'
        )

        self.url_list = reverse('Matriculas-list')  # URL para a lista de estudantes
        self.url_detail = reverse('Matriculas-detail', args=[self.matriculas.id])  # URL para um estudante específico

    def test_get_matriculas(self):
        """Teste para verificar se a requisição GET para a lista de estudantes retorna o status 200"""
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_post_matriculas(self):
        """Teste para verificar se a requisição POST para a lista de estudantes retorna o status 201"""
        data = {
            "estudante": self.estudante.id,
            "curso": self.curso.id,
            "periodo": "M"
        }

        response = self.client.post(self.url_list, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['estudante'], self.estudante.id)
        self.assertEqual(Matricula.objects.count(), 2)

    def test_get_matricula_detalhe(self):
        """Teste para verificar se a requisição GET para um estudante específico retorna o status 200"""
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['estudante'], self.estudante.id)

    def test_put_matricula(self):
        """Teste para verificar se a requisição PUT para um estudante específico retorna o status 200"""
        data = {
            "estudante": self.estudante.id,
            "curso": self.curso.id,
            "periodo": "M"
        }
        response = self.client.put(self.url_detail, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['estudante'], self.estudante.id)

    def test_delete_matricula(self):
        """Teste para verificar se a requisição DELETE para um estudante específico retorna o status 204"""
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Matricula.objects.count(), 0)