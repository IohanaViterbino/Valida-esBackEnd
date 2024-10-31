from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from escola.models import Estudante
from django.contrib.auth.models import User

class EstudanteAPITestCase(APITestCase):
    def setUp(self):
        # Criando um usuário para autenticação, caso necessário
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        
        # Criando um estudante para os testes de leitura e atualização
        self.estudante = Estudante.objects.create(
            nome='João Silva',
            email='joao.silva@example.com',
            cpf='12345678901',
            data_nascimento='2000-01-01',
            celular = "1386549835788"
        )
        self.url_list = reverse('Estudantes-list')  # URL para a lista de estudantes
        self.url_detail = reverse('Estudantes-detail', args=[self.estudante.id])  # URL para um estudante específico

    def test_get_estudantes(self):
        """Teste para verificar se a requisição GET para a lista de estudantes retorna o status 200"""
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_post_estudantes(self):
        """Teste para verificar se a requisição POST para a lista de estudantes retorna o status 201"""
        data = {
            "nome": "Teste",
            "email": "test@tes.com",
            "cpf": "13865498353",
            "data_nascimento": "2000-01-01",
            "celular": "1386549835788"
        }

        response = self.client.post(self.url_list, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nome'], data['nome'])
        self.assertEqual(Estudante.objects.count(), 2)

    def test_get_estudante_detalhe(self):
        """Teste para verificar se a requisição GET para um estudante específico retorna o status 200"""
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], self.estudante.nome)
    
    def test_put_estudante(self):
        """Teste para verificar se a requisição PUT para um estudante específico retorna o status 200"""
        data = {
            "nome": "teste",
            "email": "test@tes.com",
            "cpf": "13865498353",
            "data_nascimento": "2000-01-01",
            "celular": "1386549835788"
        }
        response = self.client.put(self.url_detail, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.estudante.refresh_from_db()
        self.assertEqual(self.estudante.nome, data['nome'])
    
    def test_delete_estudante(self):
        """Teste para verificar se a requisição DELETE para um estudante específico retorna o status 204"""
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Estudante.objects.count(), 0)