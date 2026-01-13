import { api_url, token } from "../../index/js/index.js"
import { ActionComplete, FrontendURL, PaginationListener, CreatePagination, nextPage } from "../../clients/js/clientes.js"
import { enterEditMode, exitEditMode, isEditing } from "./detailAppointments.js"
import * as Listeners from "./listenerFunctions.js"
import ErrorModal from "../../index/js/index.js"

const container = document.querySelector('.content-container')
const detailModal = document.querySelector('.appointment-detail-modal')

const appointmentsListeners = []
const detailListeners = []

export async function LoadAppointmentsPage(filter) {
    let response
    if (filter) {
        response = await AppointmentsAPI(0, filter)
    } else {
        response = await AppointmentsAPI(0)
    }

    const appointments = response.appointments
    RenderAppointments(appointments)
    document.dispatchEvent(ActionComplete)

    if (appointments.length > 1){
        const MaxPage = Math.ceil(response.total / 10)
        CreatePagination(1, MaxPage)
    }

    LoadAppointmentsListeners()
}

function LoadAppointmentsListeners() {
    const container = document.querySelector('.content')
    container.addEventListener('click', PaginationListener)
    appointmentsListeners.push({
        var: '.content',
        type: '.click',
        func: PaginationListener
    })

    const Google = document.querySelector('.google-btn')
    Google.addEventListener('click', () => {
        alert('Integração em desenvolvimento')
    })

    const newServiceBtn = document.querySelector('.appointments-header-btn')
    newServiceBtn.addEventListener('click', () => {
        const modal =  document.getElementById('bookingDialog');
        modal.showModal()
    })

    const filterContainer = document.querySelector('.custom-filter');
    const trigger = document.querySelector('.filter-trigger');
    const options = document.querySelectorAll('.filter-option');
    const selectedText = document.querySelector('.selected-text');

    trigger.addEventListener('click', Listeners.FilterDropboxActive)
    appointmentsListeners.push({
        var: '.filter-trigger',
        type: 'click',
        func: Listeners.FilterDropboxActive
    })

    options.forEach(option => {
        option.addEventListener('click', Listeners.ItemsDropbox)
    });
    appointmentsListeners.push({
        var: '.filter-option',
        type: 'click',
        func: Listeners.ItemsDropbox,
        many: true
    })

    document.addEventListener('click', (e) => {
        if (!filterContainer.contains(e.target)) {
            filterContainer.classList.remove('active');
        }
    });

}

async function AppointmentsAPI(offset, filter) {
    let URL
    if (filter) {
        URL = `${api_url}/api/appointments?offset=${offset}?filter=${filter}`
    } else {
        URL = `${api_url}/api/appointments?offset=${offset}`
    }

    try {
    const request = await fetch(URL, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': token
        }
    })
    const response = await request.json()

    if (!request.ok && request.status == 401) {
        alert('Acesso não autorizado')
        window.location.replace(`${FrontendURL}/login.html`)
    } else if (!request.ok) {
        ErrorModal(response.message, response.code)
        throw new Error(response.code)
    }

    return response

    } catch (error) {
        console.warn(error)
        return
    }
}

export async function ListNextPageAppointments(start, offset, last) {
    const filter = document.querySelector('.selected-text')
    let response
    if (filter.textContent !== 'Nenhum') {
        console.log(filter.textContent);
        response = await AppointmentsAPI(offset - 1, filter.textContent)
    } else {
        response = await AppointmentsAPI(offset - 1)
    }

    const appointments = response.appointments
    RenderAppointments(appointments)
    LoadAppointmentsListeners()

    const MaxPage = Math.ceil(response.total / 10)
    CreatePagination(start, MaxPage)
    nextPage(offset, last)
    return
}

export function RenderAppointments(appointments, total) {
    const template = document.querySelector('.appointments-template')
    const container = document.querySelector('.content')

    container.innerHTML = ''

    if (appointments.length === 0) {
        const h1 = document.createElement('h1')
        h1.textContent = 'Nenhum agendamento encontrado'
        h1.style.marginTop = '15%'
        h1.style.marginLeft = '35%'

        container.append(h1)
        return;
    }

    const clone = template.content.cloneNode(true)

    const body = clone.querySelector('.appointments-body')
    const cardTemplate = clone.querySelector('.appointment-container')
    body.innerHTML = ''

    const mesesAbreviados = [
        'jan', 'fev', 'mar', 'abr', 'mai', 'jun',
        'jul', 'ago', 'set', 'out', 'nov', 'dez'
    ];

    appointments.forEach(item => {
        const card = cardTemplate.cloneNode(true)
        card.querySelector('.appointment-container-title h3').textContent = item.service_name
        card.querySelector('.appointment-client').textContent = item.client_name

        const resp = card.querySelector('.appointment-resp')
        if (item.user_name) {
            resp.textContent = 'Resp: ' + item.user_name
        } else {
            resp.textContent = 'Sem Responsável'
        }

        card.querySelector('.appointment-hour').textContent = item.time_begin

        const status = card.querySelector('.appointment-container-status span')
        switch (item.status.toLowerCase()) {
            case 'confirmado':
                status.style.backgroundColor = '#DCFCE7'
                status.style.color = '#166534'
                break;
            case 'pendente':
                status.style.backgroundColor = '#e2e680'
                status.style.color = '#7b7f03'
                break
            case 'cancelado':
                status.style.backgroundColor = '#d00b0b57'
                status.style.color = '#d00b0bc7'
                break
            default:
                status.style.backgroundColor = '#ccc'
                status.style.color = '#ccc'
                break
        }
        status.textContent = item.status

        const dateOriginal = item.date
        const dateObj = new Date(dateOriginal + 'T00:00:00')

        const dia = String(dateObj.getDate())
        let diaFinal
        if (dia.length < 2) {
            diaFinal = '0' + dia
        } else {
            diaFinal = dia
        }


        const indiceMes = dateObj.getMonth()
        const dataFormatada = `${diaFinal} ${mesesAbreviados[indiceMes]}`
        card.querySelector('.appointment-date').textContent = dataFormatada

        const detailBtn = card.querySelector('.appointment-footer-detail')
        detailBtn.dataset.id = item.id
        detailBtn.addEventListener('click', OpenDetailsModal)
        const cancelBtn = card.querySelector('.appointment-footer-cancel')
        if (cancelBtn) {
            cancelBtn.dataset.id = item.id
        }

        body.appendChild(card)
    })

    container.appendChild(clone)

}

function OpenDetailsModal(event) {
    if (isEditing) {
        return
    }

    detailModal.showModal()
    const editBtn = detailModal.querySelector('.appointment-detail-edit')
    editBtn.dataset.id = event.target.dataset.id
    DetailModalListeners()
}

function CloseDetailModal() {
    if (isEditing) {
        exitEditMode()
        return
    }

    detailModal.close()
    RemoveDetailListeners()
}

function RemoveDetailListeners() {
    detailListeners.forEach(item => {
        const element = document.querySelector(item.var)
        if (element) {
            element.removeEventListener(item.type, item.func)
        }
        return
    })
    detailListeners.length = 0
}

function DetailModalListeners() {
    detailModal.addEventListener('cancel', CloseDetailModal)
    detailListeners.push({
        var: '.appointment-detail-modal',
        type: 'cancel',
        func: CloseDetailModal
    })

    const editBtn = detailModal.querySelector('.appointment-detail-edit')
    editBtn.addEventListener('click', enterEditMode)
    detailListeners.push({
        var: '.appointment-detail-edit',
        type: 'click',
        func: enterEditMode
    })

    const closeBtn = detailModal.querySelector('.appointment-detail-close')
    closeBtn.addEventListener('click', CloseDetailModal)
    detailListeners.push({
        var: '.appointment-detail-close',
        type: 'click',
        func: CloseDetailModal
    })

}


