from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import Usuario
from .serializers import UsuarioSerializer

@api_view(['POST'])
def cadastro(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        usuario = serializer.save()
        token, created = Token.objects.get_or_create(user=usuario)
        return Response({'token': token.key, 'usuario': serializer.data})
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    senha = request.data.get('password')
    usuario = authenticate(email=email, password=senha)

    if usuario:
        token, created = Token.objects.get_or_create(user=usuario)
        return Response({'token': token.key, 'usuario': UsuarioSerializer(usuario).data})
    return Response({'error': 'Credenciais inválidas'}, status=400)
