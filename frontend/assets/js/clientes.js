// Seleciona todos os elementos com a classe 'menu-link' para manipulação do menu de navegação
const menuLinks = document.querySelectorAll('.menu-link')
// Seleciona o container principal onde o conteúdo dinâmico será inserido
const container = document.getElementById('content-container');
// URL base para o frontend, usada para redirecionamentos
const FrontendURL = 'http://localhost:7000'
// Seleciona o modal de edição e adicção de contatos
const modal = document.getElementById('modal-cliente');

// ----------------------------------------------------------------------------------// CustomEvents
// ----------------------------------------------------------------------------------//
const CustomEventCloseEditModal = new CustomEvent ('edit-modal-closed')
const ActionComplete = new CustomEvent('action-complete')

document.addEventListener('action-complete', () => {
    RemoveClientsListeners(ClientsListeners)
    RemoveClientsListeners(SearchListeners)
})

// Arrays para controle e gerenciamento dos EventListeners, permitindo remoção posterior
var ClientsListeners = []  // Armazena listeners relacionados à página de clientes
var SearchListeners = []   // Armazena listeners relacionados à funcionalidade de busca

// Variável para controle do timer da função de debounce
let debounceTimer

// Variável para controlar o estado do dropdown de pesquisa de clientes
let searchClient

// Variável para armazenar o número total de páginas disponíveis na paginação
let MaxPage

// Array que armazena todos os clientes carregados da API
let todosClientes = []

// Array com os IDs dos campos do formulário de cliente, usado para validação e processamento
const ModalInputs = [
        'nome', 'email', 'telefone', 'cpf', 'rua', 'numero', 'bairro', 'cidade',
        'gasto', 'visitas', 'obs'
]

// --------------------------------------------------------------------------------//
// Funções relacionadas aos eventos da página de clientes
// --------------------------------------------------------------------------------//
/**
 * Fecha o modal especificado e remove os event listeners associados
 * @param {HTMLElement} modal - Elemento do modal a ser fechado
 * @param {Array} data - Array de objetos contendo informações sobre os listeners a serem removidos
 */
function CloseModalRemoveListeners(modal, data) {
    console.log('Listeners Recebidos: ' + data.length);
    // Fecha o modal se ele existir
    if (modal) {
        modal.close()
    }

    // Remove cada event listener especificado no array data
    let element
    if (data) {
        data.forEach((item) => {
            element = document.querySelector(item.var)
            element.removeEventListener(item.type, item.func)
        })
    }
    console.log('Listeners Removidos: ' + data.length);
}

/**
 * Função principal para carregar e exibir a lista de clientes
 * Realiza a requisição à API, renderiza a tabela e configura a paginação
 */
function RemoveClientsListeners(data) {
    let element
    try {
        data.forEach(item => {
            const element = document.querySelector(item.var)
            if (!element){
                throw new Error(`Elemento não encontrado: ${item.var}`)
            }
            element.removeEventListener(item.type, item.func)
        })
    } catch (error) {
        console.log(error);
    }
}
async function carregarClientes() {
    // Remove o estilo de opção ativa de todos os itens do menu
    menuLinks.forEach(l => l.classList.remove('active'))
    // Adiciona o estilo de opção ativa ao item Clientes do menu
    const btnClientes = document.getElementById('page-clientes')
    btnClientes.classList.add('active')

    // Requisição à API para obter a primeira página de clientes (limite de 10 por página)
    const resposta = await GetAllClients(1)

    // Armazena os clientes recebidos na variável global
    todosClientes = resposta.data.clientes

    // Renderiza a tabela de clientes com os dados obtidos
    renderClients(todosClientes)
    //
    // Remove Listeners Anteriores para evitar conflito
    document.dispatchEvent(ActionComplete)

    // Calcula o número total de páginas arredondando para cima
    const MaxPage = Math.ceil(resposta.data.total / 10)
    // Cria os controles de paginação
    CreatePagination(1, MaxPage)
    // Recarrega os event listeners para incluir os botões de paginação
    LoadClientsEventListeners()
    return
}

/**
 * Configura e exibe o modal para cadastro de um novo cliente
 * @param {Event} event - Evento de clique que acionou a função
 */
function NewContactListener(event) {
    // Seleciona elementos do modal
    const modal = document.getElementById('modal-cliente');
    const registerBtn = modal.querySelector('.btn-register');
    const exitBtn = modal.querySelector('.btn-exit');
    const title = modal.querySelector('.modal-title');

    // Função para fechar o modal
    function close(event) {
        event.preventDefault()
        CloseModalRemoveListeners(modal)
    }

    // Limpa todos os campos do formulário
    ModalInputs.forEach(id => {
        document.getElementById(id).value = '';
    });

    // Define o título do modal
    title.textContent = 'Cadastro de Clientes';

    // Configura o botão de registro para chamar a função de API
    registerBtn.addEventListener('click', NewContactAPI);

    // Configura o botão de sair para fechar o modal
    exitBtn.addEventListener('click', close, { once: true });

    // Impede o fechamento nativo com a tecla Escape e usa a função personalizada
    modal.addEventListener('cancel', close, { once: true });

    // Exibe o modal
    modal.showModal();
}

/**
 * Envia os dados do formulário para a API para criar um novo cliente
 * @param {Event} event - Evento de clique no botão de registro
 */
async function NewContactAPI(event) {
    const modal = document.getElementById('modal-cliente')
    event.preventDefault()

    // Cria um objeto com os dados do formulário
    body = {}
    ModalInputs.forEach(id => {
        body[id] = document.getElementById(id).value
    })

    try {
        // Envia os dados para a API
        const response = await fetch(`${api_url}/api/clients/create`, {
            method: 'POST',
            headers: {
                'Content-Type':'application/json',
                'Authorization': token
            },
            body: JSON.stringify(body)
        })

        const content = await response.json()

        // Tratamento de erros de autenticação
        if (!response.ok && response.status === 401) {
            alert('Acesso não autorizado')
            window.location.replace(`${FrontendURL}/login.html`)
            return
        } else if (!response.ok) {
            modal.close()
            throw new Error(content.message)
        }

        // Sucesso na criação do cliente
        modal.close()
        alert('Contato criado com sucesso')
        // Recarrega a lista de clientes
        carregarClientes()
        return

    } catch (error) {
        // Exibe modal de erro em caso de falha
        ErrorModal(error, 'Erro ao criar usuário')
        return
    }
}

async function EditContactAPI(id, data) {
    try {
        const response = await fetch(`${api_url}/api/clients/update/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type':'application/json',
                'Authorization': token
            },
            body: JSON.stringify(data)
        })

        if (!response.ok && response.status === 401){
            alert('Acesso no autorizado')
            window.location.replace(`${FrontendURL}/login.html`)
        } else if (!response.ok) {
            throw new Error(content.message)
        }

        alert('Contato atualizado com sucesso')
        carregarClientes()
    } catch (error) {
        ErrorModal(error, 'Erro ao atualizar informações do contato')
        carregarClientes()
    }
}
/**
 * Prepara e exibe o modal de edição de contato
 * @param {Event} event - Evento de clique no botão de edição
 * @param {string} closest - Seletor CSS para encontrar o elemento pai mais próximo
 */
async function EditClientsListener(event, closest) {
    event.preventDefault()

    // Obtém o ID do cliente a ser editado
    let id
    let editBtn = event.target
    id = editBtn.dataset.id
    if (!id){
        editBtn = event.target.closest(closest)
        id = editBtn.dataset.id
    }
    if (!id) return

    // Requisita os dados detalhados do cliente
    const response = await RequestUniqueContact(id)
    // Renderiza o modal com os dados do cliente
    RenderModalContact(response.data, id)
    // Dispara evento para indicar que a ação de busca foi concluída
    // document.dispatchEvent(ActionComplete)
}

/**
 * Exclui um cliente após confirmação
 * @param {Event} event - Evento de clique no botão de exclusão
 * @param {string} closest - Seletor CSS para encontrar o elemento pai mais próximo
 */
async function DeleteClientsListener(event, closest) {
    event.preventDefault()

    // Obtém o ID do cliente a ser excluído
    let deleteBtn = event.target
    let id = deleteBtn.dataset.id
    if (!id) {
        deleteBtn = event.target.closest(closest)
        id = deleteBtn.dataset.id
    }
    if (!id) return

    // Executa a exclusão e recarrega a lista
    const confirm = window.confirm('Deseja continuar?')
    if (!confirm) {
        return
    } else {
        await DeleteContact(id)
        carregarClientes()
        return
    }

    // Dispara evento para indicar que a ação de busca foi concluída
    document.dispatchEvent(ActionComplete)
}

/**
 * Implementa a funcionalidade de busca com debounce
 * Aguarda 500ms após a última digitação antes de enviar a requisição
 * @param {Event} event - Evento de teclado no campo de busca
 */
async function SearchClientsListener(event) {
    // Se a tecla Escape for pressionada, oculta o dropdown de resultados
    if (event.key === 'Escape') {
        const searchBar = document.querySelector('.input-client-dropdown')
        if (!searchBar) {
            return
        }
        searchBar.style.display = 'none'
        searchClient = false
        return
    }

    // Limpa o timer anterior e configura um novo
    clearTimeout(debounceTimer)
    debounceTimer = setTimeout(async () => {
        const texto = event.target.value
        if (!texto) {
            return
        }

        // Realiza a busca na API
        const response = await SearchClientAPI(texto)

        // Renderiza os resultados da busca
        RenderSearchClients(response)
        searchClient = true

        // Função auxiliar para direcionar eventos para as funções apropriadas
        function setClosest(event, closest, func) {
            switch (func) {
                case 'delete':
                    DeleteClientsListener(event, closest)
                    break
                case 'edit':
                    EditClientsListener(event, closest)
            }
        }

        // Configura os botões de exclusão nos resultados da busca
        const resultsBar = document.getElementById('input-client-dropdown')
        const exclude = resultsBar.querySelectorAll('.input-client-button--delete')
        exclude.forEach(item => {
            SearchListeners.push({
                var: '.input-client-button--delete',
                type: 'click',
                func: DeleteClientsListener
            })
            item.addEventListener('click', (event) => {
                setClosest(event, '.input-client-button--delete', 'delete')
            })
        })

        // Configura os botões de edição nos resultados da busca
        const edit = resultsBar.querySelectorAll('.input-client-button--edit')
        edit.forEach(item => {
            SearchListeners.push({
                var: '.input-client-button--edit',
                type: 'click',
                func: EditClientsListener,
            })
            item.addEventListener('click', (event) => {
                setClosest(event, '.input-client-button--edit', 'edit')
            })
        })
    }, 500); // Aguarda 500ms após a última digitação
}

/**
 * Gerencia os eventos de paginação da lista de clientes
 * @param {Event} event - Evento de clique nos botões de paginação
 */
async function PaginationListener(event) {
    let active
    let last
    const botoes = document.querySelectorAll('.pagination-button')
    const start = Number(botoes[0].textContent)
    const lastElement = document.querySelector('.pagination-last-button')

    // Determina o número da última página
    if (!lastElement){
        last = start
    } else{
        last = Number(lastElement.textContent)
    }

    // Determina a página atualmente ativa
    const ElementActive = document.querySelector('.pagination-button.active')
    if (!ElementActive) {
        active = last
    } else {
        active = Number(ElementActive.textContent)
    }

    // Identifica qual botão foi clicado
    const botao = event.target.closest('button')

    // Executa a ação correspondente ao botão clicado
    switch (botao.className) {
        case 'pagination-button':
            // Botão de página específica
            const offset = Number(botao.textContent)
            ListNextPageClients(start, offset)
            return

        case 'pagination-preview-button':
            // Botão de página anterior
            const min = active - 1

            if (min < 1) {
                alert('Você chegou a primeira página')
                return
            }
            if (active === start){
                let initial = active - 4
                if (initial <= 0){
                    ListNextPageClients(1, min, false)
                    return
                } else {
                    ListNextPageClients(active - 4, min, false)
                    return
                }
            }

            ListNextPageClients(start, min, false)
            return

        case 'pagination-more-button':
            // Botão para exibir mais páginas
            ListNextPageClients(start + 4, last + 1, false)
            return

        case 'pagination-next-button':
            // Botão de próxima página
            const max = active + 1
            if (max > last) {
                alert('Você chegou a última página')
                return
            }

            if (max === last) {
                ListNextPageClients(last, last, false)
                return
            }

            ListNextPageClients(start, max, false)
            return

        case 'pagination-last-button':
            // Botão para ir diretamente à última página
            const number = Number(botao.textContent)
            ListNextPageClients(start, number, true)
            return
    }
}

// --------------------------------------------------------------------------------//
// Gerador dos Event Listeners da página clientes
// --------------------------------------------------------------------------------//

/**
 * Configura todos os event listeners necessários para a página de clientes
 * Inclui botões de ação, campo de busca e paginação
 */
function LoadClientsEventListeners() {
    // Verifica e oculta o dropdown de busca se estiver visível
    window.clientDropdown = document.querySelector('.input-client-dropdown')
    if (searchClient) {
        clientDropdown.style.display = 'none'
        searchClient = false
    }

    // Configura o botão para adicionar novo contato
    const newContact = document.querySelector('.btn-new-contact')
    if (newContact){
        newContact.addEventListener('click', NewContactListener)
        ClientsListeners.push({
            var: '.btn-new-contact',
            type: 'click',
            func: NewContactListener
        })
    }

    // Configura o botão de edição (se existir)
    const editBtns = document.querySelectorAll('.edit-contact')
    if (editBtns){
        editBtns.forEach(btn => {
            btn.addEventListener('click', EditClientsListener)
            ClientsListeners.push({
                var: '.edit-contact',
                type: 'click',
                func: EditClientsListener
                })
            })
    }

    // Configura todos os botões de exclusão na tabela
    const deleteBtns = document.querySelectorAll('.exclude-contact')
    deleteBtns.forEach(btn => {
        btn.addEventListener('click', DeleteClientsListener);
        ClientsListeners.push({
            var: '.exclude-contact',
            type: 'click',
            func: DeleteClientsListener
        });
    });

    // Configura o campo de busca com a função de debounce
    const SearchClient = document.querySelector('.search-input')
    SearchClient.addEventListener('keydown', SearchClientsListener)
    ClientsListeners.push({
        var: '.search-input',
        type: 'keydown',
        func: SearchClientsListener
    })

    // Configura os eventos de paginação no container principal
    container.addEventListener('click', PaginationListener)
    ClientsListeners.push({
        var: '.content',
        type: 'click',
        func: PaginationListener
    })

    // Configura um evento personalizado para limpar os listeners de busca
    document.addEventListener('search-action-complete', () => {
        CloseModalRemoveListeners(undefined, SearchListeners)
    })
}

// --------------------------------------------------------------------------------//
// Lógica da aplicação
// --------------------------------------------------------------------------------//

/**
 * Carrega uma página específica de clientes da API e atualiza a interface
 * @param {number} start - Número da página inicial exibida na paginação
 * @param {number} offset - Número da página a ser carregada
 * @param {boolean} last - Indica se a página a ser carregada é a última
 */
async function ListNextPageClients(start, offset, last){
    // Requisita a página específica de clientes
    const response = await GetAllClients(offset)

    // Atualiza a lista de clientes com os novos dados
    todosClientes = response.data.clientes
    renderClients(response.data.clientes)


    // Recalcula o número total de páginas
    const MaxPage = Math.ceil(response.data.total / 10)

    // Recria os controles de paginação
    CreatePagination(Number(start), MaxPage)
    // Atualiza o estado da paginação
    nextPage(Number(offset), last)
    RemoveClientsListeners(ClientsListeners)
    RemoveClientsListeners(SearchListeners)
    LoadClientsEventListeners()
    return
}

/**
 * Requisita uma lista de clientes da API com paginação
 * @param {number} offset - Número da página a ser retornada (começando em 1)
 * @returns {Promise<Object>} - Promise que resolve para os dados da resposta da API
 */
async function GetAllClients(offset) {
    try{
        // Requisição para o endpoint que retorna a lista de clientes paginada
        const resposta = await fetch(`${api_url}/api/clients?offset=${offset}`, {
                method: 'GET',
                headers: {
                    'Authorization': token
                }
            })
        const clientes = await resposta.json()

        // Tratamento de erros de autenticação
        if (!resposta.ok && resposta.status == 401) {
            alert('Acesso não autorizado')
            window.location.replace(`${FrontendURL}/login.html`)
        } else if (!resposta.ok) {
            ErrorModal(clientes.message, 'Erro ao carregar clientes')
            throw new Error(clientes.message)
        }

        return clientes

    } catch (error) {
        ErrorModal(clients.message, 'Erro ao Listar todos os clientes')
        return
    }
}

/**
 * Cria dinamicamente os elementos de controle de paginação
 * @param {number} start - Número da primeira página a ser exibida
 * @param {number} MaxPage - Número total de páginas disponíveis
 */
function CreatePagination(start, MaxPage){
    // Cria o elemento nav que conterá os botões de paginação
    const nav = document.createElement('nav')
    nav.className = 'pagination-clients'

    // Botão para página anterior
    const reverse = document.createElement('button')
    reverse.textContent = '<'
    reverse.className = 'pagination-preview-button'
    reverse.id = 'reverse-page'
    nav.appendChild(reverse)

    const end = MaxPage - 2
    // Cria botões para as páginas (até 4 por vez)
    for (let i = start; i <= start + end; i++) {
        if (i > Number(MaxPage)) break;
        const button = document.createElement('button')
        button.textContent = i

        // Marca a primeira página como ativa
        if (i === 1) {
            button.className = 'pagination-button active'
        } else {
            button.className = 'pagination-button'
        }

        nav.appendChild(button)
    }

    // Botão de reticências (...) para exibir mais páginas
    if (MaxPage > 10) {
        const reticences = document.createElement('button')
        reticences.textContent = '...'
        reticences.className = 'pagination-more-button'
        reticences.id = 'reticences-page'
        nav.appendChild(reticences)
    }

    // Botão para ir diretamente à última página (se houver mais páginas)
    if (MaxPage > start){
        const last = document.createElement('button')
        last.textContent = MaxPage
        last.className = 'pagination-last-button'
        nav.appendChild(last)
    }

    // Botão para próxima página
    const next = document.createElement('button')
    next.textContent = '>'
    next.className = 'pagination-next-button'
    next.id = 'next-page'
    nav.appendChild(next)

    // Adiciona os controles de paginação ao container principal
    container.appendChild(nav)
}

/**
 * Atualiza o estado visual dos botões de paginação
 * @param {number} page - Número da página atual
 * @param {boolean} last - Indica se a página atual é a última
 */
function nextPage(page, last) {
    const pages = document.querySelector('.pagination-clients')
    const buttons = pages.querySelectorAll('.pagination-button')
    const lastButton = pages.querySelector('.pagination-last-button')

    // Remove a classe 'active' de todos os botões
    buttons.forEach(btn => btn.classList.remove('active'))

    // Se não for a última página, marca o botão da página atual como ativo
    if (!last){
    buttons.forEach(btn => {
        if (btn.textContent === String(page)) {
            btn.classList.add('active')
            }
        })
        return
    }

    // Se for a última página, marca o botão da última página como ativo
    lastButton.classList.add('active')
    return
}

/**
 * Renderiza a tabela de clientes com base nos dados fornecidos
 * @param {Array} clientes - Array de objetos contendo os dados dos clientes
 */
function renderClients(clientes) {
    // Clona o conteúdo do template para manipulação
    const template = document.getElementById('cliente-template').content.cloneNode(true);

    // Se não houver clientes, exibe mensagem informativa
    if (clientes.length === 0) {
        container.innerHTML = ''
        // Remove a tabela do template
        const table = template.querySelector('.client-table')
        if (table) table.remove()

        // Cria a mensagem de lista vazia
        const h1 = document.createElement('h1')
        h1.textContent = 'Nenhum cliente encontrado'
        h1.style.marginTop = '15%'
        h1.style.marginLeft = '35%'

        // Adiciona o título ao template
        template.append(h1)

        // Adiciona o template ao container
        container.appendChild(template)
        return;
    }

    // Insere o template no container visível
    container.innerHTML = '';
    container.appendChild(template);

    // Seleciona o tbody dentro do template clonado
    const tbody = container.querySelector('#client-table tbody');
    const rowTemplate = tbody.querySelector('tr'); // linha de modelo

    // Limpa o tbody e adiciona as linhas dos clientes
    tbody.innerHTML = '';

    // Itera sobre cada cliente e cria uma linha na tabela
    clientes.forEach(cliente => {
        const clone = rowTemplate.cloneNode(true);
        const info = clone.querySelector('.cliente-nome')
        // Preenche os dados do cliente na linha
        info.textContent = cliente.name;
        clone.querySelector('.cliente-email').textContent = cliente.email;
        clone.querySelector('.cliente-numero').textContent = cliente.phone
        clone.querySelector('.cliente-responsavel').textContent = cliente.resp;
        clone.querySelector('.cliente-contato').textContent = cliente.last_contact

        // Aplica estilos de status com base no valor retornado pela API
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

        // Adiciona o ID do cliente aos botões de ação
        const deleteBtn = clone.querySelector('#exclude-contact')
        const editBtn = clone.querySelector('#edit-contact')
        deleteBtn.dataset.id = cliente.id
        editBtn.dataset.id = cliente.id

        // Adiciona a linha preenchida ao tbody
        tbody.appendChild(clone);
    });
}

/**
 * Requisita os dados detalhados de um cliente específico
 * @param {string} id - ID do cliente a ser consultado
 * @returns {Promise<Object>} - Promise que resolve para os dados do cliente
 */
async function RequestUniqueContact(id) {
    try {
        // Requisição à API para obter dados detalhados do cliente
        const response = await fetch(`${api_url}/api/client/${id}/info`, {
            method: 'GET',
            headers: {
                'Content-Type':'application/json',
                'Authorization': token
            }
        })

        // Tratamento de erros de autenticação
        if (!response.ok && response.status === 401){
            alert('Acesso não autorizado')
            window.location.replace(`${FrontendURL}/login.html`)
        } else if (!response.ok){
            ErrorModal(content.message, 'Erro ao coletar informações do usuário')
            throw new Error(content.message)
        }

        const content = await response.json()
        return content

    } catch (error) {
        console.error(error)
        return
    }
}

/**
 * Envia uma requisição para excluir um cliente
 * @param {string} id - ID do cliente a ser excluído
 */
async function DeleteContact(id) {
    try {
        // Requisição à API para excluir o cliente
        const response = await fetch(`${api_url}/api/clients/delete/${id}`,{
            method: 'DELETE',
            headers: {
                'Content-Type':'application/json',
                'Authorization':token
            }
        })

        // Tratamento de erros de autenticação
        if (!response.ok && response.status === 401){
            alert('Acesso não autorizado')
            window.location.replace(`${FrontendURL}/login.html`)
        } else if (!response.ok){
            throw new Error(content.message)
        }

        // Mensagem de sucesso
        alert('Contato excluído com sucesso')
    } catch (error) {
        ErrorModal(error, 'Erro ao deletar usurio')
    }
}

/**
 * Preenche o modal de edição com os dados do cliente
 * @param {Object} data - Objeto contendo os dados do cliente
 */
function RenderModalContact(data, id) {

    // Preenche todos os campos do formulário com os dados do cliente
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

    // Define o título do modal
    const title = modal.querySelector('.modal-title');
    title.textContent = 'Editar Contato';

    const exitBtn = modal.querySelector('.btn-exit')
    const confirmBtn = modal.querySelector('.btn-register')

    function ConfirmSend(event) {
        event.preventDefault()
        body = {}
        ModalInputs.forEach(item => {
                body[item] = modal.querySelector('#' + item).value
        })

        EditContactAPI(id, body)
    }

    function closeEdit(event) {
        event.preventDefault()
        modal.close()
        modal.dispatchEvent(CustomEventCloseEditModal)
    }

    modal.addEventListener('edit-modal-closed', (event) => {
        event.preventDefault()
        if (modal.open) {
            modal.close()
        }

        exitBtn.removeEventListener('click', closeEdit)
        confirmBtn.removeEventListener('click', ConfirmSend)
    }, {once: true})

    modal.addEventListener('cancel', () => {
        modal.dispatchEvent(CustomEventCloseEditModal)
    })

    // Configura o botão de sair para fechar o modal
    exitBtn.addEventListener('click', closeEdit)

    // Configura o botão de confirmação (atualmente exibe mensagem de desenvolvimento)
    confirmBtn.textContent = 'Confirmar'
    confirmBtn.addEventListener('click', ConfirmSend)

    // Exibe o modal
    modal.showModal();
}

/**
 * Realiza uma busca de clientes por nome ou termo
 * @param {string} input - Termo de busca
 * @returns {Promise<Array>} - Promise que resolve para um array de clientes correspondentes
 */
async function SearchClientAPI(input) {
    try {
        // Requisição à API para buscar clientes pelo termo fornecido
        const response = await fetch(`${api_url}/api/clients/search/${input}`, {
            method: 'GET',
            headers: {
                'Content-Type':'application/json',
                'Authorization': token
            }
        })

        // Tratamento de erros de autenticação
        if (!response.ok && response.status === 401){
            alert('Acesso não autorizado')
            window.location.replace(`${FrontendURL}/login.html`)
        } else if (!response.ok){
            alert('Erro ao buscar usuário')
            throw new Error(content.message)
        }

        const resposta = await response.json()

        return resposta.data

    } catch (error) {
        console.log(error)
    }
}

/**
 * Renderiza os resultados da busca no dropdown
 * @param {Array} data - Array de clientes encontrados na busca
 */
function RenderSearchClients(data){
    const dropdown = document.getElementById('input-client-dropdown')
    dropdown.innerHTML = ''

    // Se não houver resultados, oculta o dropdown
    if (data.length === 0) {
        dropdown.style.display = 'none'
        return
    }

    // Cria a lista de resultados
    const lista = document.createElement('ul')

    // Itera sobre cada cliente encontrado e cria um item na lista
    data.forEach(item => {
        const li = document.createElement('li')
        const span = document.createElement('span')
        span.textContent = item.nome

        // Container para os botões de ação
        const acoesContainer = document.createElement('div')
        acoesContainer.className = 'input-client-actions'

        // Botão para visualizar/chat com o cliente
        const btnVisualizar = document.createElement('button');
        btnVisualizar.className = 'input-client-button-chat';
        btnVisualizar.dataset.id = item.clientid;
        btnVisualizar.title = 'Visualizar Item';
        const iconVisualizar = document.createElement('i');
        iconVisualizar.className = 'fas fa-comments';
        btnVisualizar.appendChild(iconVisualizar);

        // Botão para editar o cliente
        const btnEditar = document.createElement('button');
        btnEditar.className = 'input-client-button--edit';
        btnEditar.id = 'search-edit-contact'
        btnEditar.dataset.id = item.clientid;
        btnEditar.title = 'Editar Item';
        const iconEditar = document.createElement('i');
        iconEditar.className = 'fas fa-pen-to-square';
        btnEditar.appendChild(iconEditar);

        // Botão para excluir o cliente
        const btnDeletar = document.createElement('button');
        btnDeletar.className = 'input-client-button--delete';
        btnDeletar.id = 'search-exclude-contact';
        btnDeletar.dataset.id = item.clientid;
        btnDeletar.title = 'Deletar Item';
        const iconDeletar = document.createElement('i');
        iconDeletar.className = 'fas fa-trash-can';
        btnDeletar.appendChild(iconDeletar);

        // Adiciona os botões ao container de ações
        acoesContainer.appendChild(btnVisualizar);
        acoesContainer.appendChild(btnEditar);
        acoesContainer.appendChild(btnDeletar);

        // Adiciona o nome e os botões ao item da lista
        li.appendChild(span);
        li.appendChild(acoesContainer);
        lista.appendChild(li);
    });

    // Adiciona a lista ao dropdown e o exibe
    dropdown.appendChild(lista);
    dropdown.style.display = 'block';
}
