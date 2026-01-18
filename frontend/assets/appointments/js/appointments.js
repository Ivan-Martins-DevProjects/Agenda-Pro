import { api_url, token } from "../../index/js/index.js"
import { ActionComplete, FrontendURL, PaginationListener, CreatePagination, nextPage } from "../../clients/js/clientes.js"
import { enterEditMode, exitEditMode, isEditing } from "./detailAppointments.js"
import * as Listeners from "./listenerFunctions.js"
import ErrorModal from "../../index/js/index.js"

const detailModal = document.querySelector('.appointment-detail-modal')

const appointmentsListeners = []
const detailListeners = []

export async function LoadAppointmentsPage(filter, filterType) {
  let response
  if (filter) {
    response = await AppointmentsAPI(0, filter, filterType)
  } else {
    response = await AppointmentsAPI(0)
  }

  const appointments = response.appointments
  const header = document.querySelector('.appointments-header')
  if (!header) {
    RenderAppointmentsHeader()
  }
  RenderAppointmentsBody(appointments)
  document.dispatchEvent(ActionComplete)

  if (appointments.length > 1) {
    const page = document.querySelector('.pagination-clients')
    if (page) { page.remove() }
    const MaxPage = Math.ceil(response.total / 10)
    console.log(MaxPage);
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
    const modal = document.getElementById('bookingDialog');
    modal.showModal()

    NewAppointmentListeners()
  })

  const trigger = document.querySelector('.filter-trigger');
  const options = document.querySelectorAll('.filter-option');

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
    const filterContainer = document.querySelector('.custom-filter');
    if (!filterContainer.contains(e.target)) {
      filterContainer.classList.remove('active');
    }
  });

}

async function AppointmentsAPI(offset, filter, filterType) {
  let URL
  if (filter) {
    URL = `${api_url}/api/appointments?offset=${offset}&filterType=${filterType}&value=${filter}`
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

async function RequestUniqueAppointment(id) {
  try {
    const request = await fetch(`${api_url}/api/appointments/unique?id=${id}`, {
      method: 'GET',
      headers: {
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
    response = await AppointmentsAPI(offset - 1, filter.dataset.value, filter.dataset.type)
  } else {
    response = await AppointmentsAPI(offset - 1)
  }

  const appointments = response.appointments
  RenderAppointments(appointments)
  LoadAppointmentsListeners()

  const pages = document.querySelector('.pagination-clients')
  const MaxPage = Math.ceil(response.total / 10)
  // CreatePagination(start, MaxPage)
  nextPage(offset, last)
  return
}


function RenderAppointmentsHeader() {
  const template = document.querySelector('.appointments-template');
  const container = document.querySelector('.content');

  // Limpa o container
  container.innerHTML = '';

  // Clona o template
  const clone = template.content.cloneNode(true);

  // Adiciona o clone no container
  container.appendChild(clone);

}


export function RenderAppointmentsBody(appointments) {
  const body = document.querySelector('.appointments-body')
  let cardTemplate = document.querySelector('.appointment-container');
  const mesesAbreviados = [
    'jan', 'fev', 'mar', 'abr', 'mai', 'jun',
    'jul', 'ago', 'set', 'out', 'nov', 'dez'
  ];

  body.innerHTML = ''

  // Lista vazia
  if (!appointments || appointments.length === 0) {
    const pages = document.querySelector('.pagination-clients')
    if (pages) {
      pages.remove()
    }
    const emptyMessage = document.createElement('div');
    emptyMessage.classList.add('empty-message');
    emptyMessage.textContent = 'Nenhum agendamento encontrado';
    emptyMessage.style.textAlign = 'center';
    emptyMessage.style.marginTop = '20px';
    body.appendChild(emptyMessage);
    return;
  }


  if (!cardTemplate) {
    const template = document.querySelector('.appointments-template').content.cloneNode(true)
    const header = template.querySelector('.appointments-header')
    const subheader = template.querySelector('.appointments-subheader')
    const appointment = template.querySelector('.appointment-container')
    header.remove()
    subheader.remove()

    const container = document.querySelector('.content')
    container.appendChild(template)
    cardTemplate = document.querySelector('.appointment-container')
    console.log(cardTemplate);
  }
  // Cria os cards
  appointments.forEach(item => {
    const card = cardTemplate.cloneNode(true);

    // Título e cliente
    card.querySelector('.appointment-container-title h3').textContent = item.service_name;
    card.querySelector('.appointment-client').textContent = item.client_name;

    // Responsável
    const resp = card.querySelector('.appointment-resp');
    resp.textContent = item.user_name ? `Resp: ${item.user_name}` : 'Sem Responsável';

    const price = card.querySelector('.appointment-price');
    price.textContent = 'R$ ' + item.price / 100 + ',00'

    const duration = card.querySelector('.appointment-service-duration span');
    duration.textContent = item.duration + ' min'

    // Hora
    card.querySelector('.appointment-hour').textContent = item.time_begin;

    // Status
    const status = card.querySelector('.appointment-container-status span');
    switch ((item.status || '').toLowerCase()) {
      case 'confirmado':
        status.style.backgroundColor = '#DCFCE7';
        status.style.color = '#166534';
        break;
      case 'pendente':
        status.style.backgroundColor = '#e2e680';
        status.style.color = '#7b7f03';
        break;
      case 'cancelado':
        status.style.backgroundColor = '#d00b0b57';
        status.style.color = '#d00b0bc7';
        break;
      default:
        status.style.backgroundColor = '#ccc';
        status.style.color = '#ccc';
    }
    status.textContent = item.status;

    // Data
    const dateObj = new Date(item.date + 'T00:00:00');
    const dia = String(dateObj.getDate()).padStart(2, '0');
    const mes = mesesAbreviados[dateObj.getMonth()];
    card.querySelector('.appointment-date').textContent = `${dia} ${mes}`;

    // Botões
    const detailBtn = card.querySelector('.appointment-footer-detail');
    detailBtn.dataset.id = item.id;
    detailBtn.addEventListener('click', OpenDetailsModal);

    const cancelBtn = card.querySelector('.appointment-footer-cancel');
    if (cancelBtn) cancelBtn.dataset.id = item.id;

    body.appendChild(card);
  });

  const cards = document.querySelectorAll('.appointment-container')
  cards.forEach(item => {
    const name = item.querySelector('.appointment-client')
    if (name.textContent === 'Example') {
      item.remove()
    }
  })
}

export function RenderAppointments(appointments, total) {
  const template = document.querySelector('.appointments-template');
  const container = document.querySelector('.content');

  // Verifique se os cards já estão presentes dentro do container
  const existingCards = container.querySelectorAll('.appointment-container');
  if (existingCards.length > 0) {
    UpdateAppointmentCards(existingCards, appointments);
    return;
  }

  // Caso contrário, continue com o fluxo normal de renderização
  container.innerHTML = '';

  const clone = template.content.cloneNode(true);
  const body = clone.querySelector('.appointments-body');
  const cardTemplate = clone.querySelector('.appointment-container');
  body.innerHTML = '';  // Limpa a área onde os cards serão inseridos

  if (appointments.length === 0) {
    const emptyMessage = document.createElement('div');
    emptyMessage.classList.add('empty-message');
    emptyMessage.textContent = 'Nenhum agendamento encontrado';
    emptyMessage.style.textAlign = 'center';
    emptyMessage.style.marginTop = '20px';
    body.appendChild(emptyMessage);  // Exibe a mensagem de lista vazia
    container.appendChild(clone);
    return;
  }

  const mesesAbreviados = [
    'jan', 'fev', 'mar', 'abr', 'mai', 'jun',
    'jul', 'ago', 'set', 'out', 'nov', 'dez'
  ];

  appointments.forEach(item => {
    const card = cardTemplate.cloneNode(true);
    card.querySelector('.appointment-container-title h3').textContent = item.service_name;
    card.querySelector('.appointment-client').textContent = item.client_name;

    const resp = card.querySelector('.appointment-resp');
    if (item.user_name) {
      resp.textContent = 'Resp: ' + item.user_name;
    } else {
      resp.textContent = 'Sem Responsável';
    }

    card.querySelector('.appointment-hour').textContent = item.time_begin;

    const status = card.querySelector('.appointment-container-status span');
    switch (item.status.toLowerCase()) {
      case 'confirmado':
        status.style.backgroundColor = '#DCFCE7';
        status.style.color = '#166534';
        break;
      case 'pendente':
        status.style.backgroundColor = '#e2e680';
        status.style.color = '#7b7f03';
        break;
      case 'cancelado':
        status.style.backgroundColor = '#d00b0b57';
        status.style.color = '#d00b0bc7';
        break;
      default:
        status.style.backgroundColor = '#ccc';
        status.style.color = '#ccc';
        break;
    }
    status.textContent = item.status;

    const dateOriginal = item.date;
    const dateObj = new Date(dateOriginal + 'T00:00:00');

    const dia = String(dateObj.getDate());
    let diaFinal;
    if (dia.length < 2) {
      diaFinal = '0' + dia;
    } else {
      diaFinal = dia;
    }

    const indiceMes = dateObj.getMonth();
    const dataFormatada = `${diaFinal} ${mesesAbreviados[indiceMes]}`;
    card.querySelector('.appointment-date').textContent = dataFormatada;

    const detailBtn = card.querySelector('.appointment-footer-detail');
    detailBtn.dataset.id = item.id;
    detailBtn.addEventListener('click', OpenDetailsModal);
    const cancelBtn = card.querySelector('.appointment-footer-cancel');
    if (cancelBtn) {
      cancelBtn.dataset.id = item.id;
    }

    body.appendChild(card);
  });

  container.appendChild(clone);
}


function UpdateAppointmentCards(existingCards, appointments) {
  const body = document.querySelector('.appointments-body');
  const mesesAbreviados = [
    'jan', 'fev', 'mar', 'abr', 'mai', 'jun',
    'jul', 'ago', 'set', 'out', 'nov', 'dez'
  ];

  // Verifica se há agendamentos
  if (appointments.length === 0) {
    // Cria a mensagem de lista vazia, caso ela ainda não exista
    if (!body.querySelector('.empty-message')) {
      const emptyMessage = document.createElement('div');
      emptyMessage.classList.add('empty-message');
      emptyMessage.textContent = 'Nenhum agendamento encontrado';
      emptyMessage.style.textAlign = 'center';
      emptyMessage.style.marginTop = '20px';
      body.appendChild(emptyMessage); // Exibe a mensagem de lista vazia
    }

    // Remove todos os cards existentes
    existingCards.forEach(card => card.remove());
    return;
  }

  // Se houver agendamentos, remove a mensagem de lista vazia, se ela estiver presente
  const emptyMessage = body.querySelector('.empty-message');
  if (emptyMessage) {
    emptyMessage.remove();
  }

  // Atualiza os cards existentes
  existingCards.forEach((card, index) => {
    const item = appointments[index];

    card.querySelector('.appointment-container-title h3').textContent = item.service_name;
    card.querySelector('.appointment-client').textContent = item.client_name;

    const resp = card.querySelector('.appointment-resp');
    if (item.user_name) {
      resp.textContent = 'Resp: ' + item.user_name;
    } else {
      resp.textContent = 'Sem Responsável';
    }

    card.querySelector('.appointment-hour').textContent = item.time_begin;

    const status = card.querySelector('.appointment-container-status span');
    switch (item.status.toLowerCase()) {
      case 'confirmado':
        status.style.backgroundColor = '#DCFCE7';
        status.style.color = '#166534';
        break;
      case 'pendente':
        status.style.backgroundColor = '#e2e680';
        status.style.color = '#7b7f03';
        break;
      case 'cancelado':
        status.style.backgroundColor = '#d00b0b57';
        status.style.color = '#d00b0bc7';
        break;
      default:
        status.style.backgroundColor = '#ccc';
        status.style.color = '#ccc';
        break;
    }
    status.textContent = item.status;

    const dateOriginal = item.date;
    const dateObj = new Date(dateOriginal + 'T00:00:00');

    const dia = String(dateObj.getDate());
    let diaFinal;
    if (dia.length < 2) {
      diaFinal = '0' + dia;
    } else {
      diaFinal = dia;
    }

    const indiceMes = dateObj.getMonth();
    const dataFormatada = `${diaFinal} ${mesesAbreviados[indiceMes]}`;
    card.querySelector('.appointment-date').textContent = dataFormatada;

    // Atualiza os botões, se necessário
    const detailBtn = card.querySelector('.appointment-footer-detail');
    detailBtn.dataset.id = item.id;

    const cancelBtn = card.querySelector('.appointment-footer-cancel');
    if (cancelBtn) {
      cancelBtn.dataset.id = item.id;
    }
  });
}

function RenderDetailModal(info) {
  const fields = {
    name: '#appointment-detail-name',
    service: '#appointment-detail-service',
    date: '#appointment-detail-date',
    hour: '#appointment-detail-hour',
    price: '#appointment-detail-price',
    status: '#appointment-detail-status',
    obs: '#appointment-detail-obs'
  }
  for (let key in fields) {
    if (fields.hasOwnProperty(key)) {
      let id = fields[key]
      const element = detailModal.querySelector(id)

      const span = element.querySelector('span')
      const input = element.querySelector('input')
      span.textContent = info[key]

      switch (key) {
        case 'status':
          const option = element.querySelector('option')
          option.value = info[key]
          break;

        case 'obs':
          const textarea = element.querySelector('textarea')
          textarea.textContent = info[key]
          break

        case 'price':
          span.textContent = 'R$ ' + info[key] + ',00'
          input.value = 'R$ ' + info[key] + ',00'
          break

        case 'date':
          input.value = info['raw_date']
          break

        default:
          input.value = info[key]
          break;
      }
    }
  }
  detailModal.showModal()
}

async function OpenDetailsModal(event) {
  if (isEditing) {
    return
  }
  const id = event.target.dataset.id
  const response = await RequestUniqueAppointment(id)
  RenderDetailModal(response)

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
export function RenderServicesListNewAppointment(data) {
  const service = document.querySelector('.service-list')
  data.forEach(item => {
    const div = document.createElement('div')
    div.className = 'service-option'

    const span = document.createElement('span')
    span.textContent = item.name
    div.appendChild(span)

    const button = document.createElement('button')
    button.addEventListener('click', Listeners.SaveServiceInModal)
    button.textContent = '+'
    div.appendChild(button)

    service.appendChild(div)
  })
}

export function RenderSavedService(name) {
  const listSelectedServices = document.querySelector('.list-selected-services')

  const div = document.createElement('div')
  const span = document.createElement('span')
  span.textContent = name
  div.appendChild(span)
  const button = document.createElement('button')
  button.textContent = 'x'
  div.appendChild(button)

  listSelectedServices.appendChild(div)
  listSelectedServices.style.display = 'flex'
}

function NewAppointmentListeners() {
  const input = document.getElementById('serviceSelect')
  input.addEventListener('input', Listeners.ServiceInputListener)

  document.addEventListener('click', Listeners.CloseServiceList)
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


