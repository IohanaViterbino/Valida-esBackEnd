import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from escola.models import Estudante

# testes de views
@pytest.mark.django_db
def test_get_estudantes_sucess_200():
    '''Teste para verificar se a requisição GET para a lista de estudantes retorna o status 200'''
    # Cria um usuário de teste
    user = User.objects.create_user(username='testuser', password='12345')

    client = APIClient()
    # Força a autenticação do cliente com o usuário criado
    client.force_authenticate(user=user)

    # Faz a requisição
    url = reverse('Estudantes-list')
    response = client.get(url)

    # Verifica se a requisição foi bem-sucedida
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_estudantes_sucess_201():
    '''Teste para verificar se a requisição POST para a lista de estudantes retorna o status 201'''
    user = User.objects.create_user(username='testuser', password='12345')

    client = APIClient()
    client.force_authenticate(user=user)

    # Dados do estudante a ser criado
    data = {
        "nome": "Teste",
        "email": "test@tes.com",
        "cpf": "13865498353",
        "data_nascimento": "2000-01-01",
        "celular": "1386549835788"
    }

    # Faz a requisição
    url = reverse('Estudantes-list')
    response = client.post(url, data)

    assert response.status_code == 201


@pytest.mark.django_db
def test_delete_estudantes_sucess_204():
    '''Teste para verificar se a requisição DELETE para um estudante retorna o status 204'''
    user = User.objects.create_user(username='testuser', password='12345')

    client = APIClient()
    client.force_authenticate(user=user)

    # Dados do estudante a ser criado
    data = {
        "nome": "Teste",
        "email": "test@tes.com",
        "cpf": "13865498353",
        "data_nascimento": "2000-01-01",
        "celular": "1386549835378"
    }

    estudante = Estudante.objects.create(**data)

    # url = reverse('Estudantes-detail', None, None, {'pk':estudante.id})
    url = reverse('Estudantes-detail', args=[estudante.id])
    response = client.delete(url)

    assert response.status_code == 204
