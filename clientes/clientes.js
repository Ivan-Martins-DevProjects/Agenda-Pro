const btnClientes = document.getElementById('page-clientes');
const menuLinks = document.querySelectorAll('.menu-link')

let todosClientes = []

btnClientes.addEventListener('click', carregarClientes)

async function carregarClientes() {
    try {
        menuLinks.forEach(l => l.classList.remove('active'))
        btnClientes.classList.add('active')

        const response = await fetch(`{api_url}/api/clients`, {
            method: 'GET'
        })

        if (!resposta.ok) {
            console.log(resposta)
            throw new Error('Erro ao buscar clientes')
        }
        const clientes = await resposta.json()

        todosClientes = clientes
        renderClients(clientes)
    } catch (erro) {
        console.log('Erro carregarClientes:' + erro)
    }
}

function renderClients(clientes) {
  if (clientes.length === 0) {
    console.log('Documento clientes.json vazio');
    return;
  }

  // 1️⃣ Clona o conteúdo do template
  const template = document.getElementById('cliente-template').content.cloneNode(true);

  // 2️⃣ Insere o template no container visível
  const container = document.getElementById('content-container');
  container.innerHTML = ''; // limpa conteúdo anterior
  container.appendChild(template);

  // 3️⃣ Seleciona o tbody dentro do template clonado
  const tbody = container.querySelector('#client-table tbody');
  const rowTemplate = tbody.querySelector('tr'); // linha de modelo

  // 4️⃣ Limpa o tbody e adiciona as linhas dos clientes
  tbody.innerHTML = '';

  clientes.forEach(cliente => {
    const clone = rowTemplate.cloneNode(true);
    clone.querySelector('.cliente-nome').textContent = cliente.name;
    clone.querySelector('.cliente-email').textContent = cliente.email;
    clone.querySelector('.cliente-numero').textContent = cliente.phone;
    clone.querySelector('.cliente-contato').textContent = cliente.last_contact

    const status = clone.querySelector('.status')
    if (cliente.status === 'active') {
        status.classList.add('active')
        status.textContent = 'Ativo'
    } else if (cliente.status == 'potencial') {
        status.classList.add('pending')
        status.textContent = 'Potencial'
    } else if (cliente.status == 'inactive') {
        status.classList.add('inactive')
        status.textContent = 'Inativo'
    }

    tbody.appendChild(clone);

  });
}

// Abrir modal de adicionar clientes
document.addEventListener('click', function (e) {
    switch (true) {
        case e.target.matches('.btn-new-contact'):
            const modal = document.getElementById('modal-cliente')
            document.querySelector('.modal-title').textContent = 'Cadastro de Clientes';

            modal.showModal()
            break;

        case e.target.matches('.btn-exit'):
            e.preventDefault()
            const modalClose = document.getElementById('modal-cliente')

            modalClose.close()
            break

        default:
            break;
    }
});

// Função para abrir o modal de edição de contato
document.addEventListener('click', function (editModal) {
    switch (true) {
        case editModal.target.matches('.edit-contact'):
            const modal = document.getElementById('modal-cliente')

           // Encontra a linha <tr> mais próxima do botão clicado
            const row = editModal.target.closest('tr');

            // Extrai os dados da linha
            const nome = row.querySelector('.cliente-nome').textContent;
            const email = row.querySelector('.cliente-email').textContent;
            const telefone = row.querySelector('.cliente-numero').textContent;

            // Preenche os campos do modal (supondo que você já os tenha)
            document.getElementById('nome').value = nome;
            document.getElementById('email').value = email;
            document.getElementById('telefone').value = telefone;

            document.querySelector('.modal-title').textContent = 'Editar Cliente';

            modal.showModal()
            break;

        default:
            break;
    }
})

