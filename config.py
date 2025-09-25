"""
Configurações para autenticação GitHub OAuth
"""

import os

# Configurações do GitHub OAuth
GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID', '')
GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET', '')

# URL de redirecionamento para callback
REDIRECT_URI = 'http://localhost:8080/callback'

# Escopos solicitados
GITHUB_SCOPES = 'user:email'

# Configurações de segurança
SESSION_TIMEOUT = 3600  # 1 hora em segundos

def validar_configuracao():
    """
    Valida se as configurações necessárias estão presentes
    """
    erros = []
    
    if not GITHUB_CLIENT_ID:
        erros.append("GITHUB_CLIENT_ID não configurado")
    
    if not GITHUB_CLIENT_SECRET:
        erros.append("GITHUB_CLIENT_SECRET não configurado")
    
    return erros

def obter_configuracao_github():
    """
    Retorna configurações do GitHub OAuth
    """
    return {
        'client_id': GITHUB_CLIENT_ID,
        'client_secret': GITHUB_CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'scope': GITHUB_SCOPES
    }