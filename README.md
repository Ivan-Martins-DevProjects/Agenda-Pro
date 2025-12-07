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

## 🔹 Status do Projeto
O projeto está **em desenvolvimento inicial**.
Nenhuma funcionalidade está plenamente operante até o momento, mas a arquitetura já está definida e a plataforma está sendo estruturada para suportar todas as funcionalidades planejadas.

---

## 🔹 Contato
Para informações ou dúvidas:
📧 Email: Ivan_G.Martins@outlook.com
