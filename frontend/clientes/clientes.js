const btnClientes = document.getElementById('page-clientes');
const menuLinks = document.querySelectorAll('.menu-link')
const container = document.getElementById('content-container');


const token = sessionStorage.getItem('access-token')

// Cria lista para Renderizar a tabela de clientes
let todosClientes = []


// Variável para armazenar o timer
let debounceTimer

// Variável para verificar estado do dropbox de pesquisar cliente
let searchClient

// Adiciona a função carregar clientes ao botão "Clientes" no menu lateral
btnClientes.addEventListener('click', carregarClientes)

async function carregarClientes() {
    try {
        // Remove o estilo de opção ativa de todos os outros elementos
        menuLinks.forEach(l => l.classList.remove('active'))
        // Adicona o estilo de opção ativa ao item Clientes
        btnClientes.classList.add('active')

        // Coleta o token armazenado pela requisição de login
        const token = sessionStorage.getItem('access-token')

        // Requisição para o endpoint que retorna a lista de clientes
        const resposta = await fetch(`${api_url}/api/clients`, {
            method: 'GET',
            headers: {
                'Authorization': token
            }
        })

        const clientes = await resposta.json()

        if (!resposta.ok) {
            ErrorModal(clientes.message, 'Erro ao carregar clientes')
            throw new Error(clientes.message)
        }

        // Adicona a lista recebida a lista vazia criada antes
        todosClientes = clientes.data
        // Renderiza a tabela com as informações recebidas
        renderClients(clientes.data)

    } catch (erro) {
        console.log(erro.message)
        return
    }
}

function renderClients(clientes) {
  if (clientes.length === 0) {
    ;
    return;
  }

  // 1️⃣ Clona o conteúdo do template
  const template = document.getElementById('cliente-template').content.cloneNode(true);

  // 2️⃣ Insere o template no container visível
  container.innerHTML = ''; // limpa conteúdo anterior
  container.appendChild(template);

  // 3️⃣ Seleciona o tbody dentro do template clonado
  const tbody = container.querySelector('#client-table tbody');
  const rowTemplate = tbody.querySelector('tr'); // linha de modelo

  // 4️⃣ Limpa o tbody e adiciona as linhas dos clientes
  tbody.innerHTML = '';

  clientes.forEach(cliente => {
    const clone = rowTemplate.cloneNode(true);
    const info = clone.querySelector('.cliente-nome')
    // Insere o id do cliente diretamente no HTML
    info.textContent = cliente.name;
    info.setAttribute('data-client-id', cliente.id)
    clone.querySelector('.cliente-email').textContent = cliente.email;
    clone.querySelector('.cliente-numero').textContent = cliente.phone
    clone.querySelector('.cliente-responsavel').textContent = cliente.resp;
    clone.querySelector('.cliente-contato').textContent = cliente.last_contact

    // Valida os estilos de status de acordo com a resposta recebida pela api
    const status = clone.querySelector('.status')
    if (cliente.status === 'ativo') {
        status.classList.add('active')
        status.textContent = 'Ativo'
    } else if (cliente.status == 'potencial') {
        status.classList.add('pending')
        status.textContent = 'Potencial'
    } else if (cliente.status == 'inativo') {
        status.classList.add('inactive')
        status.textContent = 'Inativo'
    }

    // Cria o template com as informações recebidas
    tbody.appendChild(clone);

  });
}

async function RequestUniqueContact(id) {
    try {
        const token = sessionStorage.getItem('access-token')

        const response = await fetch(`${api_url}/api/client/${id}/info`, {
            method: 'GET',
            headers: {
                'Content-Type':'application/json',
                'Authorization': token
            }
        })

        const content = await response.json()

        if (!response.ok){
            ErrorModal(content.message, 'Erro ao coletar informações do usuário')
            throw new Error(content.message)
        }


        RenderModalContact(content.data)
        return

    } catch (error) {
        console.error(error)
        return
    }
}

async function DeleteContact(id) {
    try {
        const response = await fetch(`${api_url}/api/clients/delete/${id}`,{
            method: 'DELETE',
            headers: {
                'Content-Type':'application/json',
                'Authorization':token
            }
        })
        const content = await response.json()

        if (!response.ok){
            ErrorModal(content.message, 'Erro ao deletar usuário')
            throw new Error(content.message)
        }

        alert('Contato excluído com sucesso')
    } catch (error) {
        console.error(error)
        return
    }
}

function RenderModalContact(data, message) {
    const modal = document.getElementById('modal-cliente');

    // Preenche os campos do modal
    document.getElementById('nome').value = data.nome;
    document.getElementById('email').value = data.email;
    document.getElementById('telefone').value = data.telefone;
    document.getElementById('cpf').value = data.cpf;
    document.getElementById('rua').value = data.rua;
    document.getElementById('numero').value = data.numero;
    document.getElementById('bairro').value = data.bairro;
    document.getElementById('cidade').value = data.cidade;
    document.getElementById('gasto').value = data.gasto;
    document.getElementById('visitas').value = data.visitas;
    document.getElementById('obs').value = data.obs;

    const title = document.querySelector('.modal-title');
    title.textContent = message;

    modal.showModal();

}

// Abrir modal de adicionar clientes (Método utilizado para evitar problemas com elemento não criado)
document.addEventListener('click', function (e) {
    switch (true) {
        case e.target.matches('.btn-new-contact'):
            const modal = document.getElementById('modal-cliente')
            inputs = [
                'nome', 'email', 'telefone', 'cpf', 'rua', 'numero', 'bairro', 'cidade',
                'gasto', 'visitas', 'obs'
            ]
            inputs.forEach(id => {
                document.getElementById(id).value = ''
            })

            document.querySelector('.modal-title').textContent = 'Cadastro de Clientes';

            register = document.querySelector('.btn-register')
            register.onclick = async (e) => {
                e.preventDefault()
                const token = sessionStorage.getItem('access-token')

                body = {}
                inputs.forEach(id => {
                    body[id] = document.getElementById(id).value
                })

                const response = await fetch(`${api_url}/api/clients/create`,{
                    method : 'POST',
                    headers: {
                        'Content-Type':'application/json',
                        'Authorization': token
                    },
                    body: JSON.stringify(body)
                })

                const content = await response.json()

                document.addEventListener('error-closed', () => {
                        console.log('sucesso')
                        // RenderModalContact(data, 'Cadastro de Clientes')
                    })

                if (!response.ok){
                    modal.close()
                    ErrorModal(content.message, 'Erro ao registrar usuário')
                    return
                } else {
                    modal.close()
                    alert('Contato criado com sucesso')
                    return
                }
            }

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
document.addEventListener('click', async function (event) {
    // Verifica se o alvo é um botão de edição
    if (event.target && event.target.matches('.edit-contact')) {
        event.stopPropagation()

        const row = event.target.closest('tr')

        const info = row.querySelector('.cliente-nome')
        const id = info.getAttribute('data-client-id')

        const response = await RequestUniqueContact(id)

        RenderModalContact(response)

    // Função para deletar contatos
    } else if (event.target.matches('.exclude-contact')) {
        const row = event.target.closest('tr')
        const info = row.querySelector('.cliente-nome')
        const id = info.getAttribute('data-client-id')

        await DeleteContact(id)
        carregarClientes()
    }
});

// Requisição para pesquisar clientes
async function SearchClient(input) {
    try {
        const response = await fetch(`${api_url}/api/clients?search=${input}`, {
            method: 'GET',
            headers: {
                'Content-Type':'application/json',
                'Authorization': token
            }
        })

        if (!response.ok) {
            alert('Erro ao buscar contato')
        }

        return response
    } catch (error) {
        console.log(error)
    }
}

container.addEventListener('input', function(e){
    // Evento para pesquisar contatos
    if (e.target.matches('#input-client-field')) {
        clearTimeout(debounceTimer)
            debounceTimer = setTimeout(async() => {
                const texto = e.target.value
                
                const response = SearchClient(texto)

                RenderSearchClients(response)
                searchClient = true

            }, 500);
    }
})

function RenderSearchClients(data){
    const dropdown = document.getElementById('input-client-dropdown')
    dropdown.innerHTML = ''
    if (data.length === 0) {
        dropdown.style.display = 'none'
        return
    }

    const lista = document.createElement('ul')

    data.forEach(item => {
        const li = document.createElement('li')
        const span = document.createElement('span')
        span.textContent = item.nome

        const acoesContainer = document.createElement('div')
        acoesContainer.className = 'input-client-actions'

                // 1. Botão CHAT
        const btnVisualizar = document.createElement('button');
        btnVisualizar.className = 'input-client-button-chat';
        btnVisualizar.dataset.id = item.id;
        btnVisualizar.title = 'Visualizar Item'; // Tooltip para acessibilidade
        const iconVisualizar = document.createElement('i');
        iconVisualizar.className = 'fas fa-comments';
        btnVisualizar.appendChild(iconVisualizar);

        // 2. Botão EDITAR
        const btnEditar = document.createElement('button');
        btnEditar.className = 'input-client-button--edit';
        btnEditar.dataset.id = item.id;
        btnEditar.title = 'Editar Item';
        const iconEditar = document.createElement('i');
        iconEditar.className = 'fas fa-pen-to-square'; // Ícone de caneta
        btnEditar.appendChild(iconEditar);

        // 3. Botão DELETAR
        const btnDeletar = document.createElement('button');
        btnDeletar.className = 'input-client-button--delete';
        btnDeletar.dataset.id = item.id;
        btnDeletar.title = 'Deletar Item';
        const iconDeletar = document.createElement('i');
        iconDeletar.className = 'fas fa-trash-can'; // Ícone de lixeira
        btnDeletar.appendChild(iconDeletar);

        // Adiciona os três botões ao container
        acoesContainer.appendChild(btnVisualizar);
        acoesContainer.appendChild(btnEditar);
        acoesContainer.appendChild(btnDeletar);

        // --- FIM DAS MUDANÇAS ---

        li.appendChild(span);
        li.appendChild(acoesContainer);
        lista.appendChild(li);
    });

    dropdown.appendChild(lista);
    dropdown.style.display = 'block';

};

// Fecha o dropdown com a tecla Escape
document.addEventListener('keydown', function(event) {
    if (!searchClient) {
        return
    }
    if (event.key === 'Escape') {
        const clientDropdown = document.getElementById('input-client-dropdown');
        clientDropdown.style.display = 'none';
        searchClient = false
        }
    }
);

document.body.addEventListener('click', function(event){
    if (searchClient) {
        const clientDropdown = document.getElementById('input-client-dropdown');
        clientDropdown.style.display = 'none'
        searchClient = false
    }
})
