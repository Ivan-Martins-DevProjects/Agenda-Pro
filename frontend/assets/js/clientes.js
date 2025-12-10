const btnClientes = document.getElementById('page-clientes');
const menuLinks = document.querySelectorAll('.menu-link')
const container = document.getElementById('content-container');
const FrontendURL = 'http://localhost:7000'


const token = sessionStorage.getItem('access-token')

// Cria lista para Renderizar a tabela de clientes
let todosClientes = []


// Variável para armazenar o timer
let debounceTimer

// Variável para verificar estado do dropbox de pesquisar cliente
let searchClient

// Variável para controlar o número total de páginas
let MaxPage

// Adiciona a função carregar clientes ao botão "Clientes" no menu lateral
btnClientes.addEventListener('click', () => {
    carregarClientes()
})

async function carregarClientes() {
    try {
        // Remove o estilo de opção ativa de todos os outros elementos
        menuLinks.forEach(l => l.classList.remove('active'))
        // Adicona o estilo de opção ativa ao item Clientes
        btnClientes.classList.add('active')


        // Requisição para o endpoint que retorna a lista de clientes
        const resposta = await GetAllClients(1)


        // Adicona a lista recebida a lista vazia criada antes
        todosClientes = resposta.data.clientes

        // Renderiza a tabela com as informações recebidas
        renderClients(todosClientes)
        if (todosClientes.length === 0) {
            return
        }

        MaxPage = Math.ceil(resposta.data.total / 10)
        CreatePagination(1, MaxPage)
        return

    } catch (erro) {
        console.log(erro.message)
        return false
    }
}

async function ListNextPageClients(start, offset, last){
    const response = await GetAllClients(offset)

    todosClientes = response.data.clientes
    renderClients(response.data.clientes)

    const MaxPage = Math.ceil(response.data.total / 10)

    CreatePagination(Number(start), MaxPage)
    nextPage(Number(offset), last)
    return

}

async function GetAllClients(offset) {
    // Coleta o token armazenado pela requisição de login
    const token = sessionStorage.getItem('access-token')
    try{
        // Requisição para o endpoint que retorna a lista de clientes
        const resposta = await fetch(`${api_url}/api/clients?offset=${offset}`, {
                method: 'GET',
                headers: {
                    'Authorization': token
                }
            })
        const clientes = await resposta.json()

        if (!resposta.ok && resposta.status == 401) {
            alert('Acesso não autorizado')
            window.location.replace(`${FrontendURL}/login.html`)
        } else if (!resposta.ok) {
            ErrorModal(clientes.message, 'Erro ao carregar clientes')
            throw new Error(clientes.message)
        }

        return clientes

    } catch (error) {
        console.log(error)
        return
    }

}

// function CreateHeader()

function CreatePagination(start, all){
    // const template = document.getElementById('cliente-template')
    // if (template.content.querySelector('.pagination-clients')){
    //     return
    // }
    const nav = document.createElement('nav')
    nav.className = 'pagination-clients'

    const reverse = document.createElement('button')
    reverse.textContent = '<'
    reverse.className = 'pagination-preview-button'
    reverse.id = 'reverse-page'
    nav.appendChild(reverse)

    for (let i = start; i <= start + 3; i++) {
        if (i > Number(all)) break;

        const button = document.createElement('button')
        button.textContent = i

        if (i === 1) {
            button.className = 'pagination-button active'
        } else {
            button.className = 'pagination-button'
        }

        nav.appendChild(button)
    }
    const reticences = document.createElement('button')
    reticences.textContent = '...'
    reticences.className = 'pagination-more-button'
    reticences.id = 'reticences-page'
    nav.appendChild(reticences)

    if (all > start){
        const last = document.createElement('button')
        last.textContent = all
        last.className = 'pagination-last-button'
        nav.appendChild(last)
    }

    const next = document.createElement('button')
    next.textContent = '>'
    next.className = 'pagination-next-button'
    next.id = 'next-page'
    nav.appendChild(next)

    container.appendChild(nav)
}

function nextPage(page, last) {
    const pages = document.querySelector('.pagination-clients')
    const buttons = pages.querySelectorAll('.pagination-button')
    const lastButton = pages.querySelector('.pagination-last-button')

    buttons.forEach(btn => btn.classList.remove('active'))

    if (!last){
    buttons.forEach(btn => {
        if (btn.textContent === String(page)) {
            btn.classList.add('active')
            }
        })
        return
    }

    lastButton.classList.add('active')
    return

}


function renderClients(clientes) {
    // 1️⃣ Clona o conteúdo do template
  const template = document.getElementById('cliente-template').content.cloneNode(true);

  if (clientes.length === 0) {
      container.innerHTML = ''

      const table = template.querySelector('.client-table')
      if (table) table.remove()

      const h1 = document.createElement('h1')
      h1.textContent = 'Nenhum cliente encontrado'
      h1.style.marginTop = '15%'
      h1.style.marginLeft = '35%'

      template.append(h1)

      container.appendChild(template)
    return;
  }

  // 2️⃣ Insere o template no container visível
  container.innerHTML = '';
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

        if (!response.ok && response.status === 401){
            alert('Acesso não autorizado')
            window.location.replace(`${FrontendURL}/login.html`)
        } else if (!resposta.ok){
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

        if (!response.ok && response.status === 401){
            alert('Acesso não autorizado')
            window.location.replace(`${FrontendURL}/login.html`)
        } else if (!resposta.ok){
            ErrorModal(content.message, 'Erro ao deletar usuário')
            throw new Error(content.message)
        }


        alert('Contato excluído com sucesso')
    } catch (error) {
        console.error(error)
        return
    }
}

function RenderModalContact(data) {
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

    const title = modal.querySelector('.modal-title');
    title.textContent = 'Editar Contao';

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

            if (!response.ok && response.status === 401){
                alert('Acesso não autorizado')
                window.location.replace(`${FrontendURL}/login.html`)
            } else if (!resposta.ok){
                ErrorModal(content.message, 'Erro ao deletar usuário')
                throw new Error(content.message)
            }

                modal.close()
                alert('Contato criado com sucesso')
                return
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

        // Coletar informações da tabela
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
        const response = await fetch(`${api_url}/api/clients/search/${input}`, {
            method: 'GET',
            headers: {
                'Content-Type':'application/json',
                'Authorization': token
            }
        })

        if (!response.ok && response.status === 401){
            alert('Acesso não autorizado')
            window.location.replace(`${FrontendURL}/login.html`)
        } else if (!resposta.ok){
            alert('Erro ao buscar usuário')
            throw new Error(content.message)
        }

        const resposta = await response.json()

        return resposta.data

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

                const response = await SearchClient(texto)

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
        btnVisualizar.dataset.id = item.clientid;
        btnVisualizar.title = 'Visualizar Item'; // Tooltip para acessibilidade
        const iconVisualizar = document.createElement('i');
        iconVisualizar.className = 'fas fa-comments';
        btnVisualizar.appendChild(iconVisualizar);

        // 2. Botão EDITAR
        const btnEditar = document.createElement('button');
        btnEditar.className = 'input-client-button--edit';
        btnEditar.id = 'edit-contact'
        btnEditar.dataset.id = item.clientid;
        btnEditar.title = 'Editar Item';
        const iconEditar = document.createElement('i');
        iconEditar.className = 'fas fa-pen-to-square'; // Ícone de caneta
        btnEditar.appendChild(iconEditar);

        // 3. Botão DELETAR
        const btnDeletar = document.createElement('button');
        btnDeletar.className = 'input-client-button--delete';
        btnDeletar.dataset.id = item.clientid;
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

}

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

// Eventos para o dropdown de pesquisa de clientes
document.body.addEventListener('click', async function(event){
    const clientDropdown = document.getElementById('input-client-dropdown');

    if (searchClient) {
        clientDropdown.style.display = 'none'
        searchClient = false
    }

    const botao = event.target.closest('button')
    if (botao.className == 'input-client-button--edit') {
        event.stopPropagation()

        const id = botao.getAttribute('data-id')
        const response = await RequestUniqueContact(id)

        RenderModalContact(response)
    }

    if (botao.className == 'input-client-button--delete') {
        event.stopPropagation()

        const id = botao.getAttribute('data-id')
        await DeleteContact(id)
        carregarClientes()
    }

})


// EventListener para os botões de paginação
document.body.addEventListener('click', async(event) => {
    const botoes = document.querySelectorAll('.pagination-button')
    let start
    let last
    if (botoes.length === 0) {
        start = Number(document.querySelector('.pagination-button.active').textContent)
        last = start
    } else {
        start = Number(botoes[0].textContent)
        last = botoes[botoes.length - 1].textContent
    }

    const active = Number(document.querySelector('.pagination-button.active').textContent)

    const botao = event.target.closest('button')
    if (botao.className === 'pagination-button') {
        const offset = botao.textContent

        ListNextPageClients(start, offset)
        return
    } else if (botao.className === 'pagination-preview-button') {
        const min = active - 1
        if (min < 1) {
            alert('Você já chegou a primeira página')
            return
        }

        if (active === start){
            ListNextPageClients(active - 4, min, false)
            return
        }

        ListNextPageClients(start, min, false)
        return
    } else if (botao.className === 'pagination-more-button') {

        ListNextPageClients(Number(start) + 4, Number(last) + 1, false)
        return
    } else if (botao.className === 'pagination-next-button'){
        const active = document.querySelector('.pagination-button.active').textContent
        const max = Number(active) + 1
        if (max > MaxPage) {
            alert('Você já chegou a ultima página')
            return
        }

        if (active === last) {
            ListNextPageClients(max, max, false)
            return
        }

        ListNextPageClients(start, max, false)
        return

    } else if (botao.className === 'pagination-last-button'){
        const number = botao.textContent
        ListNextPageClients(start, Number(number), true)
        return
    }

})
