from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import Usuario
from .serializers import UsuarioSerializer

@api_view(['POST'])
def cadastro(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        usuario = serializer.save()
        usuario.set_password(request.data['password'])  # Salvar senha corretamente
        usuario.save()
        token, created = Token.objects.get_or_create(user=usuario)
        return Response({'token': token.key, 'usuario': serializer.data})
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def login(request):
    login_input = request.data.get('email', '').strip()  # Garante que nunca seja None
    senha = request.data.get('password')

    if not login_input or not senha:
        return Response({'error': 'Todos os campos devem ser preenchidos!'}, status=400)

    try:
        usuario = Usuario.objects.filter(email=login_input).first() if "@" in login_input else Usuario.objects.filter(username=login_input).first()

        if not usuario:
            return Response({'error': 'Usuário não encontrado!'}, status=400)

        usuario_autenticado = authenticate(request, email=usuario.email, password=senha)


        if usuario_autenticado:
            token, created = Token.objects.get_or_create(user=usuario_autenticado)
            return Response({'token': token.key, 'usuario': UsuarioSerializer(usuario_autenticado).data})
        else:
            return Response({'error': 'Credenciais inválidas!'}, status=400)

    except Exception as e:
        return Response({'error': f'Erro interno: {str(e)}'}, status=500)
