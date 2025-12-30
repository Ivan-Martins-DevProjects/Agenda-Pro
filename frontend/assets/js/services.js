// ==============================================================================
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
const OpenModal = new Event('new-service-modal-open')

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
            throw new Error(clientes.message)
        }

        return services.data

    } catch (error) {
        ErrorModal(error, 'Erro ao listar Serviços')
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
        if (!response.status === 401) {
            alert('Acesso não autorizado')
            window.location.replace(`${FrontendURL}/login.html`)
            return
        } else if (!response.ok) {
            if (NewServiceModal) {
                NewServiceModal.close()
            }
            throw new Error(resposta.message)
        }

        NewServiceModal.close()
        alert('Serviço criado com sucesso')
        LoadServices()
        return

    } catch (error) {
        ErrorModal(undefined, 'Erro ao cadastrar novo serviço')
        console.log(error);
        return
    }
}

// ==============================================================================
// FUNÇÕES DE COLETA E PROCESSAMENTO DE DADOS
// ==============================================================================

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


/**
 * Gerencia o fluxo de criação: coleta dados e chama a API.
 */
async function CreateNewService(event) {
    event.preventDefault()
    const data = await InfoNewService()
    console.log(data);
    if (!data) { return }

    NewServiceAPI(data)
    return
}

// ==============================================================================
// FUNÇÕES DE RENDERIZAÇÃO (UI)
// ==============================================================================

/**
 * Renderiza a lista de serviços na tela.
 */
function RenderServices(services) {
    const content = document.querySelector('.content')

    content.innerHTML = ''

    if (services.length === 0) {
        const h1 = document.createElement('h1')
        h1.textContent = 'Nenhum serviço encontrado'
        h1.style.marginTop = '15%'
        h1.style.marginLeft = '35%'
        content.appendChild(h1) // Corrigido para adicionar ao DOM (lógica sugerida, embora o original não fizesse append)
        return
    }

    const header = document.createElement('div')
    header.style.display = 'flex'
    header.style.justifyContent = 'space-between'
    header.style.width = '100%'
    header.style.maxWidth = '900px'
    header.style.margin = '1rem auto 2rem 0'

    // Header Section
    const TitleDiv = document.createElement('div')
    const headerTitle = document.createElement('h2')
    headerTitle.style.margin = '0'
    headerTitle.textContent = 'Serviços Cadastrados'
    TitleDiv.appendChild(headerTitle)

    const DivSearch = document.createElement('div')
    const searchbar = document.createElement('input')
    searchbar.style.width = '300px'
    searchbar.className = 'search-input'
    searchbar.placeholder = 'Pesquise aqui'
    DivSearch.appendChild(searchbar)

    const btnDiv = document.createElement('div')
    const headerBtn = document.createElement('button')
    headerBtn.style.marginLeft = '350px'
    headerBtn.style.width = '200px'
    headerBtn.className = 'new-service'
    headerBtn.textContent = '+ Novo cadastro'
    btnDiv.appendChild(headerBtn)

    header.appendChild(TitleDiv)
    header.appendChild(DivSearch)
    header.appendChild(btnDiv)
    content.appendChild(header)

    const containers = document.createElement('div')
    containers.className = 'services-containers'

    services.forEach(item => {
        // Card Main Container
        const main = document.createElement('div')
        main.dataset.id = item.id
        main.className = 'container'

        // Card Header
        const cardHeader = document.createElement('div')
        cardHeader.className = 'services-card-header'

        const h3 = document.createElement('h3')
        h3.textContent = item.title

        cardHeader.appendChild(h3)
        main.appendChild(cardHeader)

        // Card Description
        const body = document.createElement('div')
        body.className = 'services-card-body'

        const p = document.createElement('p')
        p.textContent = item.description

        body.appendChild(p)
        main.appendChild(body)

        // Card Price and Duration
        const info = document.createElement('div')
        info.className = 'services-card-price-duration'

        const price = document.createElement('span')
        price.className = 'services-price'
        price.textContent = 'R$ ' + item.price / 100 + ',00'

        const duration = document.createElement('span')
        duration.className = 'services-duration'
        duration.textContent = item.duration + ' min'

        info.appendChild(price)
        info.appendChild(duration)
        main.appendChild(info)

        // Card Footer Buttons
        const footer = document.createElement('div')
        footer.className = 'services-card-footer'

        const editBtn = document.createElement('button')
        editBtn.className = 'btn-services-edit'
        editBtn.textContent = 'Editar'

        const excludeBtn = document.createElement('button')
        excludeBtn.className = 'btn-services-exclude'
        excludeBtn.textContent = 'Excluir'

        footer.appendChild(editBtn)
        footer.appendChild(excludeBtn)
        main.appendChild(footer)

        containers.appendChild(main)
    });

    content.appendChild(containers)
}

// ==============================================================================
// GERENCIAMENTO DE EVENTOS (LISTENERS)
// ==============================================================================

/**
 * Abre o modal de novo serviço.
 */
function NewServiceListener() {
    NewServiceModal.showModal()
    document.dispatchEvent(OpenModal)
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
