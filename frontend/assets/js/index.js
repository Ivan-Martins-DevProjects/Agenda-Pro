import {carregarClientes, CloseModalRemoveListeners} from './clientes.js'
import LoadServices from './services.js'

// Obtém referência ao botão do Dashboard no menu lateral
const btnDashboard = document.getElementById('page-dashboard')

// URL base da API utilizada para requisições
export const api_url = 'http://localhost:8585'

// Seleciona todos os links do menu lateral
const menuLinks = document.querySelectorAll('.menu-link')

// Seleciona o container principal onde o conteúdo das páginas será renderizado
var container = document.getElementById('content-container');

// Obtém o token de acesso armazenado na sessão
export const token = sessionStorage.getItem('access-token')

const servicesList = [
    { id: 1, name: 'Corte Degradê', description: 'Corte moderno com degrade na lateral e posterior, finalizado com loção pós-barba.', price: 40.00, duration: 30 },
    { id: 2, name: 'Barba Completa', description: 'Alinhamento, navalha, toalha quente e tônicos para uma barba impecável.', price: 30.00, duration: 25 },
    { id: 3, name: 'Pacote Executivo', description: 'Corte + Barba + Máscara facial relaxante. O tratamento completo para o cavalheiro.', price: 80.00, duration: 60 },
    { id: 4, name: 'Sombrancelha', description: 'Design e alinhamento de sobrancelha com pinça ou navalha.', price: 15.00, duration: 10 }
]


// Executa a função PageDashboard assim que o DOM estiver totalmente carregado
window.addEventListener('DOMContentLoaded', () => {
    PageDashboard('page-dashboard')
})

// Seleciona o menu lateral e adiciona um listener de clique para todos os itens
const sideMenu = document.querySelector('.side-menu')
sideMenu.addEventListener('click', MainMenuListeners)

/**
 * Remove a classe 'active' de todos os links do menu lateral e adiciona ao botão selecionado
 * @param {string} btn - ID do botão que deve receber a classe 'active'
 */
function ClearActiveSideMenu(btn) {
    const element = document.getElementById(btn)
    menuLinks.forEach(item => item.classList.remove('active'))
    element.classList.add('active')
}

/**
 * Função principal que trata os cliques nos itens do menu lateral
 * @param {Event} event - Evento de clique
 */
function MainMenuListeners(event) {
    const btn = event.target.closest('.menu-link') // Verifica o elemento clicado mais próximo com a classe 'menu-link'
    if (!btn) {
        console.error('Botão menu-link não encontrado');
    }
    // Redireciona para a função correspondente ao botão clicado
    switch (btn.id) {
        case 'page-dashboard':
            PageDashboard(btn.id)
            break

        case 'page-clientes':
            PageClients(btn.id)
            break

        case 'page-services':
            PageServices(btn.id)
            break;

        case 'page-appointments':
            PageAppointments(btn.id)
            break

        case 'page-chat':
            PageChat(btn.id)
            break

        case 'page-config':
            PageConfig(btn.id)
            break

        default:
            break
    }
}

/**
 * Função genérica para páginas ainda em construção
 */
function PageInConstruction() {
    container.innerHTML = '' // Limpa o container principal

    // Cria e estiliza o título da página em construção
    const h1 = document.createElement('h1')
    h1.textContent = 'Função em construção'
    h1.style.marginTop = '15%'
    h1.style.marginLeft = '35%'

    container.append(h1)
    return
}

/**
 * Página de clientes: ativa o botão correspondente e carrega os clientes
 * @param {string} btn - ID do botão clicado
 */
async function PageClients(btn) {
    ClearActiveSideMenu(btn)
    await carregarClientes() // Função assíncrona para buscar clientes
    return
}

/**
 * Outras páginas que ainda estão em construção
 */
function PageServices(btn) {
    ClearActiveSideMenu(btn)
    LoadServices()
    // PageInConstruction()
    return
}

function PageAppointments(btn) {
    ClearActiveSideMenu(btn)
    // PageInConstruction()
    const dialog = document.getElementById('bookingDialog');
    dialog.showModal()
    return
}

function PageChat(btn) {
    ClearActiveSideMenu(btn)
    PageInConstruction()
    return
}

function PageConfig(btn) {
    ClearActiveSideMenu(btn)
    PageInConstruction()
    return
}

/**
 * Página do dashboard
 * @param {string} btn - ID do botão clicado
 */
async function PageDashboard(btn) {
    ClearActiveSideMenu(btn)
    PageInConstruction()
}

/**
 * Função que faz requisição GET para obter dados do dashboard
 */
async function LoadDashboard() {
    try {
        const response = await fetch(`${api_url}/api/dashboard`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })

        if (!response.ok) {
            return response
        }

        const data = await response.json()
        return data

    } catch (error) {
        return null
    }
}

/**
 * Exibe modal de erro na tela
 * @param {string} message - Mensagem de erro
 * @param {string} title - Título do erro
 */
export default function ErrorModal(message, title) {
    const errorModal = document.getElementById('error-modal-template')

    // Preenche modal com título e mensagem
    errorModal.querySelector('#modal-code').textContent = title
    errorModal.querySelector('#modal-message').textContent = message

    // Função para fechar o modal
    function CloseModal(event) {
        event.preventDefault()
        CloseModalRemoveListeners(errorModal, data)
    }

    const data = []

    // Adiciona evento de clique no botão de fechar
    const exitBtn = errorModal.querySelector('.btn-cancel-exclude')
    exitBtn.addEventListener('click', CloseModal)
    data.push({
        var: '.btn-cancel-exclude',
        type: 'click',
        func: CloseModal
    })

    const close = errorModal.querySelector('.close-modal-btn')
    close.addEventListener('click', CloseModal)
    data.push({
        var: '.close-modal-btn',
        type: 'click',
        func: CloseModal
    })

    errorModal.addEventListener('cancel', CloseModal, {once:true})

    errorModal.showModal()
}

/**
 * Dropdown das informações do usuário
 * Mostra/oculta o menu ao clicar na área do usuário
 */
document.addEventListener('DOMContentLoaded', function(){
    const dropdown = document.getElementById('userDropdown')
    const dropdownButton = dropdown.querySelector('.user-info')

    dropdownButton.addEventListener('click', function(event){
        event.stopPropagation() // Evita que o clique feche imediatamente o dropdown
        dropdown.classList.toggle('active')
    })

    // Fecha o dropdown ao clicar fora dele
    document.addEventListener('click', function(event) {
        if (!event.target.closest('.user-dropdown')) {
            dropdown.classList.remove('active')
        }
    })
})

