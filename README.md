# Modelagem-computacional-compania-de-energia

Sistema de modelagem computacional para companhia de energia com autenticação GitHub OAuth.

## Funcionalidades

- ⚡ Processamento de leituras de energia
- 💰 Cálculo de faturamento
- 🔍 Detecção de leituras inconsistentes
- 🔐 **Autenticação GitHub OAuth**
- 👤 Gerenciamento de usuários autenticados

## Configuração da Autenticação GitHub

### 1. Criar OAuth App no GitHub

1. Acesse [GitHub Developer Settings](https://github.com/settings/developers)
2. Clique em "OAuth Apps" > "New OAuth App"
3. Preencha as informações:
   - **Application name**: `Modelagem Energia`
   - **Homepage URL**: `http://localhost:8080`
   - **Authorization callback URL**: `http://localhost:8080/callback`
4. Clique em "Register application"
5. Anote o `Client ID` e gere um `Client Secret`

### 2. Configurar Variáveis de Ambiente

```bash
export GITHUB_CLIENT_ID='seu_client_id_aqui'
export GITHUB_CLIENT_SECRET='seu_client_secret_aqui'
```

Ou crie um arquivo `.env`:
```
GITHUB_CLIENT_ID=seu_client_id_aqui
GITHUB_CLIENT_SECRET=seu_client_secret_aqui
```

## Como Usar

### Execução com Autenticação

```bash
python3 modelagem.py
```

O sistema irá:
1. Verificar se as configurações GitHub estão presentes
2. Abrir o navegador para autenticação
3. Aguardar autorização do usuário
4. Processar os dados com o usuário autenticado

### Exemplo de Autenticação

```bash
python3 exemplo_auth.py
```

### Execução Sem Autenticação (Modo Demonstração)

Se as configurações GitHub não estiverem presentes, o sistema executa em modo demonstração.

## Estrutura do Projeto

```
├── modelagem.py          # Sistema principal com autenticação
├── auth.py              # Classes de autenticação GitHub OAuth
├── config.py            # Configurações do sistema
├── exemplo_auth.py      # Exemplo de uso da autenticação
├── dados_leituras.csv   # Dados de exemplo
└── README.md           # Este arquivo
```

## Classes Principais

### GitHubAuth
Gerencia o fluxo de autenticação OAuth com GitHub.

### UsuarioAutenticado
Representa um usuário autenticado com informações do GitHub.

### Cliente, Medidor, Leitura, Faturamento
Classes do sistema de energia (funcionalidade original).

## Segurança

- ✅ Utiliza OAuth 2.0 padrão
- ✅ Validação de estado (CSRF protection)
- ✅ Tokens seguros
- ✅ Timeout de sessão configurável

## Requisitos

- Python 3.6+
- Bibliotecas padrão do Python (não requer instalações adicionais)
- Conta GitHub para autenticação

## Troubleshooting

### Erro: "CLIENT_ID do GitHub não configurado"
- Verifique se as variáveis de ambiente estão definidas
- Execute `echo $GITHUB_CLIENT_ID` para verificar

### Erro: "Estado de segurança inválido"
- Tente novamente o processo de autenticação
- Verifique se não há múltiplas tentativas simultâneas

### Navegador não abre automaticamente
- Copie a URL exibida no terminal
- Cole no navegador manualmente