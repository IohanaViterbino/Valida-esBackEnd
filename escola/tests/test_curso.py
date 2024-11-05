from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from escola.models import Curso
from django.contrib.auth.models import User

class CursoAPITestCase(APITestCase):    
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
        self.url_list = reverse('Cursos-list')  # URL para a lista de estudantes
        self.url_detail = reverse('Cursos-detail', args=[self.curso.id])  # URL para um estudante específico

    def test_get_curso(self):
        """Teste para verificar se a requisição GET para a lista de cursos retorna o status 200"""
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_post_curso(self):
        """Teste para verificar se a requisição POST para a lista de cursos retorna o status 201"""
        data = {
            'codigo': 'PB009',
            'descricao': 'Python backend curso de servidor em Django Rest Framework',
            'nivel': 'I',
        }
        response = self.client.post(self.url_list, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Curso.objects.count(), 2)

    def test_put_curso(self):
        '''Teste para verificar se a requisição PUT para um curso específico retorna o status 200'''
        data = {
            'codigo': 'PT009',
            'descricao': 'Python backend curso de servidor em Django Rest Framework',
            'nivel': 'I',
        }
        response = self.client.put(self.url_detail, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.curso.refresh_from_db()
        self.assertEqual(Curso.objects.get().codigo, 'PT009')

    def test_delete_curso(self):
        '''Teste para verificar se a requisição DELETE para um curso específico retorna o status 204'''
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Curso.objects.count(), 0)