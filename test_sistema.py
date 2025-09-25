#!/usr/bin/env python3
"""
Teste completo do sistema com e sem autenticação
"""

import os
import sys
from modelagem import executar_sem_autenticacao, executar_com_autenticacao
from auth import GitHubAuth, UsuarioAutenticado

def teste_sistema_completo():
    """
    Testa o sistema completo
    """
    print("=== Teste do Sistema Completo ===")
    print()
    
    # Teste 1: Sistema sem autenticação
    print("1️⃣ Testando sistema sem autenticação...")
    resultado = executar_sem_autenticacao()
    assert resultado == "Fatura gerada: 57.5 R$", f"Esperado 'Fatura gerada: 57.5 R$', obtido: {resultado}"
    print("✅ Teste 1 passou!")
    print()
    
    # Teste 2: Classes de autenticação
    print("2️⃣ Testando classes de autenticação...")
    auth = GitHubAuth('test_client', 'test_secret')
    assert auth.client_id == 'test_client'
    assert not auth.is_authenticated()
    
    # Simula dados de usuário
    user_data = {
        'id': 12345,
        'login': 'testuser',
        'name': 'Test User',
        'email': 'test@example.com',
        'avatar_url': 'https://github.com/avatar.png'
    }
    
    usuario = UsuarioAutenticado(user_data)
    assert usuario.login == 'testuser'
    assert usuario.nome == 'Test User'
    print("✅ Teste 2 passou!")
    print()
    
    # Teste 3: URL de autorização
    print("3️⃣ Testando geração de URL de autorização...")
    url = auth.generate_auth_url()
    assert 'github.com/login/oauth/authorize' in url
    assert 'client_id=test_client' in url
    assert 'state=' in url
    print("✅ Teste 3 passou!")
    print()
    
    print("🎉 Todos os testes passaram!")
    return True

def teste_configuracao():
    """
    Testa validação de configuração
    """
    from config import validar_configuracao
    
    print("=== Teste de Configuração ===")
    
    # Salva configuração atual
    client_id_original = os.getenv('GITHUB_CLIENT_ID')
    client_secret_original = os.getenv('GITHUB_CLIENT_SECRET')
    
    try:
        # Remove configurações para teste
        if 'GITHUB_CLIENT_ID' in os.environ:
            del os.environ['GITHUB_CLIENT_ID']
        if 'GITHUB_CLIENT_SECRET' in os.environ:
            del os.environ['GITHUB_CLIENT_SECRET']
        
        erros = validar_configuracao()
        assert len(erros) == 2, f"Esperado 2 erros, obtido: {len(erros)}"
        print("✅ Validação de configuração funciona corretamente!")
        
    finally:
        # Restaura configuração original
        if client_id_original:
            os.environ['GITHUB_CLIENT_ID'] = client_id_original
        if client_secret_original:
            os.environ['GITHUB_CLIENT_SECRET'] = client_secret_original

if __name__ == "__main__":
    try:
        teste_configuracao()
        teste_sistema_completo()
        print("\n🏆 Todos os testes foram executados com sucesso!")
        print("✅ Sistema de autenticação GitHub implementado corretamente!")
        
    except Exception as e:
        print(f"\n❌ Erro nos testes: {e}")
        sys.exit(1)