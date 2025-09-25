#!/usr/bin/env python3
"""
Exemplo de uso da autenticação GitHub OAuth
"""

import os
from auth import iniciar_fluxo_autenticacao, GitHubAuth, UsuarioAutenticado
from config import validar_configuracao

def exemplo_basico():
    """
    Exemplo básico de autenticação GitHub
    """
    print("=== Exemplo de Autenticação GitHub ===")
    print()
    
    # Verifica se as configurações estão presentes
    erros = validar_configuracao()
    if erros:
        print("❌ Configuração incompleta:")
        for erro in erros:
            print(f"   - {erro}")
        print()
        print("📋 Instruções de configuração:")
        print("1. Vá para GitHub.com > Settings > Developer settings > OAuth Apps")
        print("2. Clique em 'New OAuth App'")
        print("3. Preencha:")
        print("   - Application name: Modelagem Energia")
        print("   - Homepage URL: http://localhost:8080")
        print("   - Authorization callback URL: http://localhost:8080/callback")
        print("4. Configure as variáveis de ambiente:")
        print("   export GITHUB_CLIENT_ID='seu_client_id_aqui'")
        print("   export GITHUB_CLIENT_SECRET='seu_client_secret_aqui'")
        return
    
    print("✅ Configuração encontrada!")
    print("🔐 Iniciando fluxo de autenticação...")
    
    # Inicia autenticação
    auth = iniciar_fluxo_autenticacao()
    
    if auth and auth.is_authenticated():
        print("🎉 Autenticação bem-sucedida!")
        
        # Cria objeto de usuário
        usuario = UsuarioAutenticado(auth.user_info)
        print(f"👤 Usuário: {usuario}")
        print(f"📧 Email: {usuario.email}")
        print(f"🆔 GitHub ID: {usuario.github_id}")
        
        return usuario
    else:
        print("❌ Falha na autenticação")
        return None

def exemplo_sem_navegador():
    """
    Exemplo de autenticação manual (sem abrir navegador)
    """
    print("=== Exemplo de Autenticação Manual ===")
    print()
    
    auth = GitHubAuth()
    
    try:
        auth_url = auth.generate_auth_url()
        print("🔗 URL de autorização gerada:")
        print(auth_url)
        print()
        print("📋 Instruções:")
        print("1. Copie e cole a URL acima no seu navegador")
        print("2. Faça login no GitHub e autorize a aplicação")
        print("3. Você será redirecionado para localhost:8080/callback")
        print("4. A autenticação será processada automaticamente")
        
    except ValueError as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    # Tenta autenticação automática primeiro
    usuario = exemplo_basico()
    
    if not usuario:
        print("\n" + "="*50)
        # Se falhar, mostra exemplo manual
        exemplo_sem_navegador()