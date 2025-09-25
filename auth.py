import os
import hashlib
import secrets
import time
from urllib.parse import urlencode
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading

class GitHubAuth:
    """
    Classe para autenticação via GitHub OAuth
    """
    
    def __init__(self, client_id=None, client_secret=None):
        self.client_id = client_id or os.getenv('GITHUB_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('GITHUB_CLIENT_SECRET')
        self.redirect_uri = "http://localhost:8080/callback"
        self.scope = "user:email"
        self.state = None
        self.access_token = None
        self.user_info = None
        
    def generate_auth_url(self):
        """
        Gera URL de autorização do GitHub
        """
        if not self.client_id:
            raise ValueError("CLIENT_ID do GitHub não configurado")
            
        self.state = secrets.token_urlsafe(32)
        
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': self.scope,
            'state': self.state,
            'response_type': 'code'
        }
        
        base_url = "https://github.com/login/oauth/authorize"
        return f"{base_url}?{urlencode(params)}"
    
    def exchange_code_for_token(self, code, state):
        """
        Troca o código de autorização por um token de acesso
        """
        if state != self.state:
            raise ValueError("Estado de segurança inválido")
            
        # Em uma implementação real, faria uma requisição HTTP para:
        # POST https://github.com/login/oauth/access_token
        # Por simplicidade, simulamos o token
        self.access_token = f"gho_simulated_token_{hashlib.md5(code.encode()).hexdigest()[:16]}"
        return self.access_token
    
    def get_user_info(self):
        """
        Obtém informações do usuário autenticado
        """
        if not self.access_token:
            raise ValueError("Token de acesso não disponível")
            
        # Em uma implementação real, faria uma requisição para:
        # GET https://api.github.com/user
        # Por simplicidade, retornamos dados simulados
        self.user_info = {
            'id': 12345,
            'login': 'usuario_github',
            'name': 'Usuário GitHub',
            'email': 'usuario@github.com',
            'avatar_url': 'https://github.com/images/error/octocat_happy.gif'
        }
        return self.user_info
    
    def is_authenticated(self):
        """
        Verifica se o usuário está autenticado
        """
        return self.access_token is not None and self.user_info is not None

class AuthCallbackHandler(BaseHTTPRequestHandler):
    """
    Handler para callback do OAuth
    """
    auth_instance = None
    
    def do_GET(self):
        if self.path.startswith('/callback'):
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            code = query_params.get('code', [None])[0]
            state = query_params.get('state', [None])[0]
            error = query_params.get('error', [None])[0]
            
            if error:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f"<h1>Erro na autenticação: {error}</h1>".encode())
                return
            
            if code and self.auth_instance:
                try:
                    self.auth_instance.exchange_code_for_token(code, state)
                    self.auth_instance.get_user_info()
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    
                    user = self.auth_instance.user_info
                    response = f"""
                    <h1>Autenticação realizada com sucesso!</h1>
                    <p>Bem-vindo, {user['name']} (@{user['login']})</p>
                    <p>Você pode fechar esta janela.</p>
                    """
                    self.wfile.write(response.encode())
                    
                except Exception as e:
                    self.send_response(500)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(f"<h1>Erro: {str(e)}</h1>".encode())
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("<h1>Código de autorização não recebido</h1>".encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suprime logs do servidor HTTP
        pass

def iniciar_fluxo_autenticacao():
    """
    Inicia o fluxo de autenticação GitHub OAuth
    """
    auth = GitHubAuth()
    
    # Configura o handler do callback
    AuthCallbackHandler.auth_instance = auth
    
    # Inicia servidor local para callback
    server = HTTPServer(('localhost', 8080), AuthCallbackHandler)
    server_thread = threading.Thread(target=server.serve_request)
    server_thread.daemon = True
    server_thread.start()
    
    # Gera URL de autorização e abre no navegador
    auth_url = auth.generate_auth_url()
    print(f"Abrindo navegador para autenticação...")
    print(f"Se não abrir automaticamente, acesse: {auth_url}")
    
    try:
        webbrowser.open(auth_url)
    except Exception as e:
        print(f"Não foi possível abrir o navegador automaticamente: {e}")
    
    # Aguarda autenticação (timeout de 60 segundos)
    timeout = 60
    start_time = time.time()
    
    while not auth.is_authenticated() and (time.time() - start_time) < timeout:
        time.sleep(1)
    
    server.shutdown()
    
    if auth.is_authenticated():
        print(f"\nAutenticação realizada com sucesso!")
        print(f"Usuário: {auth.user_info['name']} (@{auth.user_info['login']})")
        return auth
    else:
        print("\nTimeout na autenticação ou erro ocorrido.")
        return None

class UsuarioAutenticado:
    """
    Classe para gerenciar usuário autenticado
    """
    
    def __init__(self, auth_info):
        self.github_id = auth_info['id']
        self.login = auth_info['login']
        self.nome = auth_info['name']
        self.email = auth_info['email']
        self.avatar_url = auth_info['avatar_url']
        self.data_login = time.time()
    
    def to_dict(self):
        return {
            'github_id': self.github_id,
            'login': self.login,
            'nome': self.nome,
            'email': self.email,
            'avatar_url': self.avatar_url,
            'data_login': self.data_login
        }
    
    def __str__(self):
        return f"UsuarioAutenticado(login={self.login}, nome={self.nome})"