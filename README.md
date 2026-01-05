# CRM Completo (Em Desenvolvimento)

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)


---

## 🔹 Como visualizar o projeto
Todo o projeto está estruturado com docker, basta utilizar da ferramenta para facilitar o processo.

1. #### Clone o repositório:
```bash
git clone https://github.com/Ivan-Martins-DevProjects/Agenda-Pro.git
```

2. #### Navegue até a pasta do projeto:
```bash
cd Agenda-Pro
```

3. #### Execute o build do docker-compose:
```bash
docker-compose up -d --build
```

4. ### Acesse a página de login:
[http://localhost:7000/login.html](http://localhost:7000/login.html)

5. ### Insira as seguintes credenciais:
### Login:
```bash
admin@admin.com
```
### Senha:
```bash
admin
```

---

## 🔹 Descrição
Este projeto é um **CRM completo** em desenvolvimento, voltado para gestão de clientes, serviços, agendamentos e comunicação em tempo real via WhatsApp.
A ideia é criar uma plataforma unificada para que o usuário possa gerenciar contatos, serviços, agendamentos e receitas de forma prática e integrada.

A plataforma contará com:
- Cadastro de clientes sincronizado com o WhatsApp
- Gestão de serviços associados a agendamentos e registro automático de receitas
- Agendamentos integrados à agenda do Google
- Canal de chat em tempo real via WebSockets conectado ao WhatsApp
- Dashboard com informações resumidas sobre clientes, serviços e receitas

---

## 🔹 Progresso Atual
O desenvolvimento avança com foco na modularidade do frontend, segurança e arquitetura robusta no backend. Os marcos recentes incluem:

🔹 **Frontend (Módulo de Clientes)**
- Página de clientes concluída e funcional.
- Implementadas as operações de CRUD: Adicionar, Remover, Editar e Pesquisar contatos.
- Utilização combinada de Templates, Dialogs (Modais) e renderização dinâmica de elementos via JavaScript para uma interface reativa.

🔹 **Frontend (Módulo de Serviços)**
- Iniciada a implementação da página de serviços, aplicando as mesmas arquiteturas e técnicas validadas no módulo de clientes.

🔹 **Backend & Arquitetura**
- Autenticação robusta implementada via JWT (JSON Web Token).
- O token é utilizado para validar as permissões em cada requisição, garantindo a identidade do usuário e verificando se ele está autorizado a efetuar a operação solicitada.
- Foco total na aplicação dos princípios SOLID (Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation e Dependency Inversion) para garantir um código limpo, escalável e de fácil manutenção.

🔹 **Backend & Arquitetura**
- banco de dados já está populado com dados fictícios (Mock Data) para facilitar a manipulação e testes imediatos das funcionalidades durante o desenvolvimento.

---
## 🔹 Diagramas
### Fluxo da processo de login:
![Fluxo de Login](images/Fluxo%20de%20Login.png)

### Fluxo do processo de listagem de todos os clientes:
![Fluxo de Listagem de Clientes](images/Fluxo%20ListClients.png)

---

## 🔹 Funcionalidades Planejadas
- **Cadastro de Clientes:**
  Adição de contatos que serão sincronizados automaticamente com o WhatsApp.

- **Gestão de Serviços:**
  Criação e edição de serviços que podem ser vinculados a agendamentos. Serviços concluídos registram automaticamente a receita gerada.

- **Agendamentos:**
  Criação de compromissos vinculados à agenda do Google, permitindo integração com calendários existentes.

- **Chat em Tempo Real com WhatsApp:**
  Canal de comunicação instantânea com clientes via WebSockets.

- **Dashboard:**
  Exibição de informações resumidas sobre clientes, serviços, agendamentos e receitas.

---

## 🔹 Tecnologias
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Golang
- **Banco de Dados:** PostgreSQL
- **Integrações:** WhatsApp API, Google Calendar API
- **Comunicação em Tempo Real:** WebSockets

---
## 🔹 Contato
Para informações ou dúvidas:
📧 Email: Ivan_G.Martins@outlook.com
