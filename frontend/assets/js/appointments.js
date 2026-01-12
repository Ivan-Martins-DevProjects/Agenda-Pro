import { api_url, token } from "./index.js"
import { ActionComplete, FrontendURL, PaginationListener, CreatePagination, nextPage } from "./clientes.js"
import ErrorModal from "./index.js"

const container = document.querySelector('.content-container')

const appointmentsListeners = []

export async function LoadAppointmentsPage() {
    const response = await AppointmentsAPI(0)

    const appointments = response.appointments
    await RenderAppointments(appointments)
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

    const newServiceBtn = document.querySelector('.appointments-header-btn')
    newServiceBtn.addEventListener('click', () => {
        const modal =  document.getElementById('bookingDialog');
        modal.showModal()
    })
}

async function AppointmentsAPI(offset) {
    try {
    const request = await fetch(`${api_url}/api/appointments?offset=${offset}`, {
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
        console.log(item);
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

        body.appendChild(card)
    })

    container.appendChild(clone)

}
