// =============================================================================r
// IMPORTAÇÕES
// ==============================================================================
import { api_url, token } from "./index.js"
import { ActionComplete, FrontendURL, PaginationListener, CreatePagination, nextPage } from "./clientes.js"
import ErrorModal from "./index.js"

// ==============================================================================
// CONSTANTES E VARIÁVEIS GLOBAIS
// ==============================================================================
const ServicesListeners = []
const NewServiceModal = document.querySelector('.new-service-modal')
const OpenNewServiceModal = new Event('new-service-modal-open')
const OpenEditServiceModal = new Event('edit-service-modal-open')

// ==============================================================================
// FUNÇÕES DE API (REQUISIÇÕES AO SERVIDOR)
// ==============================================================================

/**
 * Busca a lista de serviços na API com base no offset (paginação).
 */
async function ListServicesAPI(offset) {
    try {
        const response = await fetch(`${api_url}/api/services?offset=${offset}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token
            }
        })
        const services = await response.json()

        // Tratamento de erros de autenticação
        if (!response.ok && response.status == 401) {
            alert('Acesso não autorizado')
            window.location.replace(`${FrontendURL}/login.html`)
        } else if (!response.ok) {
            ErrorModal(services.message, services.code)
            throw new Error(services.code)
        }

        return services

    } catch (error) {
        console.warn(error);
        return
    }
}

/**
 * Envia os dados para criar um novo serviço na API.
 */
async function NewServiceAPI(data) {
    try {
        const response = await fetch(`${api_url}/api/services/create`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token
            },
            body: JSON.stringify(data)
        })

        const resposta = await response.json()

        // Nota: Mantido a lógica original de '!response.status === 401'
        if (response.status === 401) {
            alert('Acesso não autorizado')
            window.location.replace(`${FrontendURL}/login.html`)
            return
        } else if (!response.ok) {
            if (NewServiceModal) {
                NewServiceModal.close()
            }
            ErrorModal(resposta.message, resposta.code)
            throw new Error(resposta.code)
        }

        NewServiceModal.close()
        alert('Serviço criado com sucesso')
        LoadServices()
        return

    } catch (error) {
        console.log('Erro ao cadastrar novo usuário');
        return
    }
}

async function DeleteServiceAPI(id) {
    try {
        const response = await fetch(`${api_url}/api/services/delete?id=${id}`, {
            method: 'DELETE',
            headers: {'Authorization': token}
        })

        resposta = await response.json()

        if (response.status === 401) {
            alert('Acesso não autorizado')
            window.location.replace(`${FrontendURL}/login.html`)
            return
        } else if (!response.ok) {
            ErrorModal(resposta.message, resposta.code)
            throw new Error(resposta.code)
        }

        alert('Usuário excluído com sucesso')
        return

    } catch (error) {
        console.warn(error);
        return
    }
}

async function GetUniqueServiceAPI(id){
    try {
        const response = await fetch(`${api_url}/api/services/unique?id=${id}`, {
            method: 'GET',
            headers: {'Authorization': token}
        })

        const resposta = await response.json()

        if (response.status === 401) {
            alert('Acesso não autorizado')
            window.location.replace(`${FrontendURL}/login.html`)
            return
        } else if (!response.ok) {
            ErrorModal(resposta.message, resposta.code)
            throw new Error(response.code)
        }

        return resposta.data

    } catch (error) {
        console.warn(error);
        return
    }
}

async function EditServiceAPI(data, id) {
    try {
        const response = await fetch(`${api_url}/api/services/edit?id=${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token
            },
            body: JSON.stringify(data)
        })

        const resposta = await response.json()

        if (response.status === 401) {
            alert('Acesso não autorizado')
            window.location.replace(`${FrontendURL}/login.html`)
            return
        } else if (!response.ok) {
            ErrorModal(resposta.message, resposta.code)
            throw new Error(resposta.code)
        }

        alert('Contato editado com sucesso')
        NewServiceModal.close()

    } catch (error) {
        console.warn(error);
        return
    }

}

// ==============================================================================
// FUNÇÕES DE COLETA E PROCESSAMENTO DE DADOS
// ==============================================================================

function ClearNewServiceModal() {
    const title = NewServiceModal.querySelector('.new-service-title h2')
    title.textContent = 'Cadastrar Novo Serviço'

    const fields = [
    '.new-service-input-title', '.new-service-input-description',
    '.new-service-input-price', '.new-service-input-duration'
    ]

    fields.forEach(item => {
        const element = NewServiceModal.querySelector(item)
        if (element) {
            element.value = ''
        }
    })
}

/**
 * Coleta os dados inseridos no modal de novo serviço.
 */
function InfoNewService() {
    const parameters = {
        título: '.new-service-input-title',
        descrição: '.new-service-input-description',
        preço: '.new-service-input-price',
        duração: '.new-service-input-duration'
    }

    const data = {}

    try {
        for (const [key, selector] of Object.entries(parameters)) {
            const element = NewServiceModal.querySelector(selector)

            if (!element) {
                throw new Error(`Elemento não encontrado: ${selector}`)
                return
            }

            const content = element.value.trim()

            if (!content) {
                throw new Error(key)
                return
            }

            switch (key) {
                case 'título':
                    data['title'] = content
                    break
                case 'descrição':
                    data['description'] = content
                    break
                case 'preço':
                    data['price'] = content
                    break
                case 'duração':
                    data['duration'] = content
                    break
                default:
                    break
            }
        }

        return data

    } catch (error) {
        ErrorModal(`Valor de ${error.message} vazio`, 'Formato Inválido')
        return
    }
}

function RenderEditServiceModal(data){
    const modal = document.querySelector('.new-service-modal')
    const title = document.querySelector('.new-service-title h2')
    title.textContent = 'Editar Serviço'

    const name = document.querySelector('.new-service-input-title')
    name.value = data.title

    const description = document.querySelector('.new-service-input-description')
    description.value = data.description

    const price = document.querySelector('.new-service-input-price')
    price.value = data.price / 100

    const duration = document.querySelector('.new-service-input-duration')
    duration.value = data.duration

    modal.showModal()
    document.dispatchEvent(OpenEditServiceModal)
}
/**
 * Gerencia o fluxo de criação: coleta dados e chama a API.
 */
async function CreateNewService(event) {
    event.preventDefault()

    const data = await InfoNewService()
    if (!data) { return }

    NewServiceAPI(data)
    return
}

async function GetUniqueServiceListener(event){
    event.preventDefault()

    const editBtn = event.target
    const id = editBtn.dataset.id
    const confirmBtn = NewServiceModal.querySelector('.new-service-confirm')
    confirmBtn.dataset.id = id
    const data = await GetUniqueServiceAPI(id)

    RenderEditServiceModal(data)
    EditServiceModalListeners()
}

async function EditServiceListener(event) {
    event.preventDefault()
    const confirmBtn = event.target
    const id = confirmBtn.dataset.id

    const title = NewServiceModal.querySelector('.new-service-input-title')
    const description = NewServiceModal.querySelector('.new-service-input-description')
    const price = NewServiceModal.querySelector('.new-service-input-price')
    const duration = NewServiceModal.querySelector('.new-service-input-duration')

    const data = {
        title: title.value,
        description: description.value,
        price: price.value,
        duration: duration.value
    }

    EditServiceAPI(data, id)
}

// ==============================================================================
// FUNÇÕES DE RENDERIZAÇÃO (UI)
// ==============================================================================

/**
 * Renderiza a lista de serviços na tela.
 */

function RenderServices(services) {
    const content = document.querySelector('.content');
    content.innerHTML = '';

    // --- Caso não haja serviços ---
    if (!services.length) {
        const h1 = document.createElement('h1');
        h1.textContent = 'Nenhum serviço encontrado';
        h1.className = 'no-services'; // você pode definir CSS para centralizar
        content.appendChild(h1);
        return;
    }

    // --- HEADER ---
    const header = document.createElement('div');
    header.className = 'services-header'; // usa CSS responsivo

    // Título
    const titleDiv = document.createElement('div');
    const logoTitle = document.createElement('i')
    logoTitle.className = 'fas fa-briefcase fa-2x'
    logoTitle.style.color = '#1582BD'


    const headerTitle = document.createElement('h2');
    headerTitle.textContent = 'Meus Serviços';
    titleDiv.className = 'services-header-title'
    titleDiv.appendChild(logoTitle);
    titleDiv.appendChild(headerTitle);

    // Search
    const searchDiv = document.createElement('div');
    const searchInput = document.createElement('input');
    searchInput.className = 'search-input';
    searchInput.placeholder = 'Pesquise aqui';
    searchDiv.appendChild(searchInput);

    // Botão Novo Serviço
    const btnDiv = document.createElement('div');
    const newServiceBtn = document.createElement('button');
    newServiceBtn.className = 'new-service';
    newServiceBtn.textContent = '+ Novo cadastro';
    btnDiv.appendChild(newServiceBtn);

    // Append ao header
    header.appendChild(titleDiv);
    header.appendChild(searchDiv);
    header.appendChild(btnDiv);

    content.appendChild(header);

    // --- GRID DE CARDS ---
    const containers = document.createElement('div');
    containers.className = 'services-containers';

    services.forEach(item => {
        // Card principal
        const card = document.createElement('div');
        card.className = 'services-container';

        // Header do Card
        const cardHeader = document.createElement('div');
        cardHeader.className = 'services-card-header';
        const h3 = document.createElement('h3');
        h3.textContent = item.title;
        cardHeader.appendChild(h3);
        card.appendChild(cardHeader);

        // Corpo do Card
        const cardBody = document.createElement('div');
        cardBody.className = 'services-card-body';
        const desc = document.createElement('p');
        desc.textContent = item.description;
        cardBody.appendChild(desc);
        card.appendChild(cardBody);

        // Preço e duração
        const info = document.createElement('div');
        info.className = 'services-card-price-duration';
        const price = document.createElement('span');
        price.className = 'services-price';
        price.textContent = `R$ ${(item.price / 100).toFixed(2).replace('.', ',')}`;

        const clock = document.createElement('i')
        clock.className = 'fas fa-clock'
        clock.style.marginRight = '5px'

        const durationDiv = document.createElement('div')
        durationDiv.className = 'services-duration';

        const duration = document.createElement('span');
        duration.textContent = `${item.duration} min`;
        durationDiv.appendChild(clock)
        durationDiv.appendChild(duration);
        info.appendChild(price);
        info.appendChild(durationDiv)
        card.appendChild(info);

        // Footer com botões
        const footer = document.createElement('div');
        footer.className = 'services-card-footer';

        const editBtn = document.createElement('button');
        editBtn.className = 'btn-services-edit';
        editBtn.dataset.id = item.id;
        editBtn.textContent = 'Editar';
        editBtn.addEventListener('click', GetUniqueServiceListener);

        const excludeBtn = document.createElement('button');
        excludeBtn.className = 'btn-services-exclude';
        excludeBtn.dataset.id = item.id;
        excludeBtn.textContent = 'Excluir';
        excludeBtn.addEventListener('click', DeleteServiceListener);

        footer.appendChild(editBtn);
        footer.appendChild(excludeBtn);
        card.appendChild(footer);

        // Adiciona card ao grid
        containers.appendChild(card);
    });

    content.appendChild(containers);
}


// ==============================================================================
// GERENCIAMENTO DE EVENTOS (LISTENERS)
// ==============================================================================

/**
 * Abre o modal de novo serviço.
 */
function NewServiceListener() {
    ClearNewServiceModal()
    NewServiceModal.showModal()
    document.dispatchEvent(OpenNewServiceModal)
}

function EditServiceModalListeners() {
    const modal = document.querySelector('.new-service-modal')
    modal.addEventListener('cancel', exit)

    function exit(event) {
        event.preventDefault()
        editBtn.removeEventListener('click', EditServiceListener)
        exitBtn.removeEventListener('click', exit)
        modal.removeEventListener('cancel', exit)
        modal.close()
    }

    const editBtn = modal.querySelector('.new-service-confirm')
    editBtn.addEventListener('click', EditServiceListener)

    const exitBtn = modal.querySelector('.new-service-exit')
    exitBtn.addEventListener('click', exit)
}


async function DeleteServiceListener(event){
    const deleteBtn = event.target
    const id = deleteBtn.dataset.id

    const confirm = window.confirm('Deseja continuar?')
    if (!confirm){
        return
    } else {
        await DeleteServiceAPI(id)
        LoadServices()
        return
    }
}

/**
 * Configura os listeners específicos para dentro do Modal (Confirmar/Sair).
 */
function NewServiceModalListeners() {
    const btnConfirm = document.querySelector('.new-service-confirm')
    const btnExit = document.querySelector('.new-service-exit')

    function exit(event) {
        event.preventDefault()
        NewServiceModal.close()
        btnExit.removeEventListener('click', exit)
        btnConfirm.removeEventListener('click', CreateNewService)
    }

    btnConfirm.addEventListener('click', CreateNewService)
    btnExit.addEventListener('click', exit)
    NewServiceModal.addEventListener('cancel', exit, { once: true })
}

/**
 * Configura os listeners globais da página de serviços.
 */
function LoadServicesListener() {
    const container = document.querySelector('.content')
    container.addEventListener('click', PaginationListener)

    ServicesListeners.push({
        var: '.content',
        type: '.click',
        func: PaginationListener
    })

    document.addEventListener('new-service-modal-open', NewServiceModalListeners)
    const NewServiceBtn = document.querySelector('.new-service')
    NewServiceBtn.addEventListener('click', NewServiceListener)
    ServicesListeners.push({
        var: '.new-service',
        type: 'click',
        func: NewServiceListener
    })

    document.addEventListener('edit-service-modal-open', EditServiceModalListeners)
    ServicesListeners.push({
        var: '.new-service',
        type: 'click',
        func: EditServiceModalListeners
    })

    }

// ==============================================================================
// FUNÇÕES PRINCIPAIS DE CONTROLE E EXPORTAÇÃO
// ==============================================================================

/**
 * Função principal para carregar os serviços.
 * Orquestra a busca na API, renderização e paginação inicial.
 */
export default async function LoadServices() {
    const response = await ListServicesAPI(0)
    if (!response) {
        return
    }

    const services = response.services
    RenderServices(services)

    document.dispatchEvent(ActionComplete)

    if (services.length > 1) {
        const MaxPage = Math.ceil(response.total / 10)
        CreatePagination(1, MaxPage)
    }

    LoadServicesListener()
    return
}

/**
 * Carrega a próxima página de serviços (paginação).
 */
export async function ListNextPageServices(start, offset, last) {
    const response = await ListServicesAPI(offset - 1)

    const services = response.services
    RenderServices(services)
    LoadServicesListener()

    const MaxPage = Math.ceil(response.total / 10)
    CreatePagination(start, MaxPage)
    nextPage(offset, last)
    return
}
