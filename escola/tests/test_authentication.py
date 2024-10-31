from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.contrib.auth import authenticate
from django.urls import reverse

class AuthenticationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='testpassword')
        self.url = reverse('Estudantes-list')

    def test_authentication_user_com_credencias_corretas(self):
        usuario = authenticate(username='test', password='testpassword')
        self.assertTrue((usuario is not None) and usuario.is_authenticated)
    
    def test_authentication_user_com_credencial_errada(self):
        usuario = authenticate(username='test', password='wrongtestpassword')
        self.assertFalse(usuario is not None and usuario.is_authenticated)
        
    def test_authentication_user_com_username_errado(self):
        usuario = authenticate(username='wrongtest', password='testpassword')
        self.assertFalse(usuario is not None and usuario.is_authenticated)

    def test_authentication_user_com_credencias_erradas(self):
        usuario = authenticate(username='wrongtest', password='wrongtestpassword')
        self.assertFalse(usuario is not None and usuario.is_authenticated)
        
    def test_get_estudantes_sem_autenticacao(self):
        """Verifica se a requisição GET sem autenticação retorna 401 Unauthorized"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)  # Defina para um código diferente de 401
    
    def test_get_estudantes_com_autenticacao(self):
        """Verifica se a requisição GET autenticada retorna 200 OK"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
