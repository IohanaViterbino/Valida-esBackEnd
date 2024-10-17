from validate_docbr import CPF
import re, datetime
from escola.models import Matricula

def validate_cpf(value):
    cpf = CPF()
    return not cpf.validate(value)

def validate_email(value):
    regex_email = re.compile(r'[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?', re.IGNORECASE)
    return re.match(regex_email, value) == None

def validate_nome(value):
    regex_nome = re.compile(r'^[a-zA-Z ]+$', re.IGNORECASE)
    return re.match(regex_nome, value) == None

def validate_celular(value):
    return len(value) != 13

def validate_data_nascimento(value):
    return value > datetime.date.today()

def validate_codigo(value):
    return len(value) < 3

def validate_descricao(value):
    return len(value) < 10 or len(value) > 100

def validate_periodo(value):
    estudante = value.get('estudante')
    periodo = value.get('periodo')

    return Matricula.objects.filter(estudante=estudante, periodo=periodo).exists()