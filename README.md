# 💼 👁️ Wallet Watch
Um **projeto web desenvolvido em Python com Flask**, utilizando **banco de dados MySQL**, **HTML/CSS/JavaScript** para interface, e foco na gestão financeira pessoal. O sistema permite o **gerenciamento de transações financeiras**, wish lists (lista de desejos), autenticação de usuários e geração de relatórios mensais em PDF, com análises e insights automáticos. Tudo integrado com atualização dinâmica de dados e visualizações com gráficos para análises de ganhos e gastos.
O aplicativo está disponível online no domínio [wallet-watch.up.railway.app](https://wallet-watch.up.railway.app/).
---
## 📌 Funcionalidades
- **Autenticação de Usuários**
  - Registro de novos usuários com email e senha (senhas criptografadas com MD5 para segurança básica).
  - Login seguro com verificação de credenciais e gerenciamento de sessões (expiração automática após 5 horas).
  - Logout para encerrar a sessão e redirecionar para a página de login.
- **Gerenciamento de Transações**
  - Adição de novas transações (ganhos ou despesas), incluindo categoria (ex.: salário, estudos, compras), custo fixo (sim/não), valor, data, descrição e upload opcional de comprovante (arquivos como PDF, PNG, JPG).
  - Visualização de transações do mês atual em uma lista dinâmica, com totais de saldo, ganhos e despesas.
  - Download de comprovantes de pagamento para transações com recibos anexados.
  - Análises visuais com gráficos de pizza (usando Chart.js) para porcentagens de gastos por categoria e fontes de ganhos.
- **Lista de Desejos (Wish List)**
  - Adição de novos desejos ou metas financeiras.
  - Atualização do status de desejos (marcar como "concluído" ou "não concluído").
  - Exclusão de desejos selecionados.
  - Visualização de todos os desejos do usuário, com sincronização em tempo real.
- **Geração de Relatórios Mensais**
  - Criação automática de relatórios em PDF com título personalizado (ex.: "Monthly report of [email do usuário]").
  - Resumo de ganhos, despesas e saldo restante do mês.
  - Lista completa de transações com todos os detalhes (data, categoria, valor, tipo, custo fixo, descrição, presença de recibo).
  - Porcentagens de gastos por categoria (apenas categorias com despesas).
  - Insights financeiros gerados dinamicamente (ex.: sugestões baseadas em categorias de maior gasto, com variação aleatória para diversidade).
  - Inclusão da wish list pendente (itens não concluídos).
  - Limite de até 3 páginas, com design atraente (cores do sistema, tabelas, headers coloridos) usando a biblioteca fpdf.
- **Limpeza Automática de Dados**
  - Evento programado no MySQL para executar no último dia do mês às 12:00 PM: apaga transações antigas e desejos concluídos de todos os usuários, mantendo apenas contas de usuário e desejos pendentes.
---
## 💻 Como utilizar
1. **Instalação Local**:
   - Clone o repositório ou baixe os arquivos do projeto.
   - Instale as dependências Python: `pip install flask mysql-connector-python fpdf werkzeug`.
   - Configure o banco de dados MySQL: Crie um database chamado `wallet_watch` e importe o schema das tabelas `user`, `transactions` e `wishlist` (disponível no dump fornecido).
   - Atualize as credenciais de conexão no arquivo `connection.py` (host, user, password, database).
2. **Execução Local**:
   - Rode o servidor Flask: `python app.py` (executa em `localhost:5000` com modo debug ativado).
   - Acesse no navegador: `http://localhost:5000/`.
3. **Uso Online**:
   - Acesse diretamente [wallet-watch.up.railway.app](https://wallet-watch.up.railway.app/).
   - Registre uma conta ou faça login.
   - Navegue pelas seções: Home (visão geral), Transactions (gerencie transações e análises), Wish List (gerencie desejos), Reports (gere PDF mensal via botão ou rota `/generate_report`).
4. **Interações Principais**:
   - Adicione transações via modal no menu Transactions, com upload de comprovantes.
   - Visualize análises em gráficos interativos.
   - Gerencie wish list com botões de update/delete.
   - Baixe relatórios PDF da página Reports – alterações são salvas no banco e refletidas em tempo real.
5. **Observações de Segurança**:
   - Use senhas fortes; o sistema usa hashing MD5 (considere atualizar para bcrypt em produção).
   - Uploads de arquivos são limitados a tipos específicos (PDF, imagens) e armazenados em `static/images/payment_receipts`.
---
## 📖 Conceitos Aplicados
- **Desenvolvimento Web com Flask**
  - Rotas dinâmicas para CRUD (Create, Read, Update, Delete) em transações, wish lists e autenticação.
  - Gerenciamento de sessões e flashes para feedback ao usuário.
  - Integração com banco de dados via MySQL connector, com funções getters/setters para queries seguras.
- **Banco de Dados Relacional**
  - Tabelas com chaves estrangeiras (ex.: `user_id` em transactions e wishlist).
  - Eventos agendados no MySQL para manutenção automática (limpeza mensal).
  - Queries para autenticação, recuperação de dados e status de tabelas.
- **Frontend Interativo**
  - HTML templates com Jinja2 para renderização dinâmica (ex.: loops para transações).
  - CSS personalizado (baseado em root variables para temas) e JavaScript para modais, gráficos (Chart.js) e eventos (ex.: onchange para formulários).
- **Geração de Documentos**
  - Uso de fpdf para criar PDFs personalizados com tabelas, cores e layouts otimizados (máximo 3 páginas).
  - Cálculos dinâmicos para totais, porcentagens e insights randomizados.
- **CRUD Avançado**
  - Create (inserir transações/wishes), Read (visualizar listas e relatórios), Update (editar status de wishes), Delete (remover itens).
- **Segurança e Manutenção**
  - Hashing de senhas, validação de arquivos uploadados, e eventos de banco para retenção de dados relevantes.
---
## 🚀 Tecnologias
- **Python 3+ (com Flask para backend)**
- **MySQL (para banco de dados relacional)**
- **HTML5, CSS3 e JavaScript (com Chart.js para gráficos)**
- **fpdf (para geração de PDFs)**
- **Werkzeug (para uploads seguros)**
- **Hashlib (para criptografia de senhas)**
- **Railway.app (para deploy online)**
---
## 📝 Observação
Este projeto foi desenvolvido com o objetivo de **praticar desenvolvimento web full-stack** (porém é possível utilizá-lo para uso pessoal), integração com banco de dados, geração de relatórios e automações financeiras, simulando um app real de controle de finanças pessoais.

## Contribuições são bem-vindas para expandir funcionalidades.
