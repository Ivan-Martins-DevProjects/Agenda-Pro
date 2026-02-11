import { CloseModalRemoveListeners } from "../../clients/js/clientes.js";
import ErrorModal, { api_url, token } from "../../index/js/index.js";
import { ListNameOptionsCreateAppointment, ListServiceOptionsCreateAppointment } from "../../services/js/services.js";
import { appointmentsListeners, detailListeners, LoadAppointmentsPage, LoadNewAppointmentListeners, RenderNameListNewAppointment, RenderSavedService, RenderServicesListNewAppointment } from "./appointments.js";
import { EditAppointmentAPI, LoadEditData } from "./detailAppointments.js";
import { Request, UpdateStatusAPI } from "./requests.js";
let timer

export function FilterDropboxActive(event) {
  const filterContainer = document.querySelector('.custom-filter')
  event.stopPropagation()
  filterContainer.classList.toggle('active')
}

export function ItemsDropbox(event) {
  event.stopPropagation();
  const options = document.querySelectorAll('.filter-option')
  options.forEach(item => {
    item.classList.remove('selected')
  })

  const option = event.target
  option.classList.add('selected')

  const selectedText = document.querySelector('.selected-text')
  selectedText.textContent = option.textContent.trim()
  selectedText.dataset.type = option.dataset.type
  selectedText.dataset.value = option.dataset.value

  const filterContainer = document.querySelector('.custom-filter')
  filterContainer.classList.remove('active')

  const filter = selectedText.dataset.value
  const filterType = selectedText.dataset.type
  LoadAppointmentsPage(filter, filterType)
}

export function NamesInputListener(event) {
  clearTimeout(timer)
  CloseNamesList()

  timer = setTimeout(async () => {
    const name = event.target.value
    const data = await ListNameOptionsCreateAppointment(name)
    RenderNameListNewAppointment(data)
  }, 1000)
}

export function CloseNamesList() {
  const nameList = document.querySelectorAll('.name-option')
  if (nameList) {
    nameList.forEach(item => {
      item.remove()
    })
  }
}

export function SaveNameInModal(event) {
  const button = event.target
  const span = button.previousElementSibling
  const id = span.dataset.id

  const name = span.textContent
  const field = document.querySelector('#contactName')
  field.value = name
  field.dataset.id = id
}

export function ServiceInputListener(event) {
  clearTimeout(timer)
  const serviceList = document.querySelectorAll('.service-option')
  if (serviceList) {
    serviceList.forEach(item => {
      item.remove()
    })
  }

  timer = setTimeout(async () => {
    const name = event.target.value
    const data = await ListServiceOptionsCreateAppointment(name)
    RenderServicesListNewAppointment(data)
  }, 1000)
}

export function CloseServiceList() {
  const listServices = document.querySelectorAll('.service-option')
  if (listServices) {
    listServices.forEach(item => {
      item.remove()
    })
  }
}

export function SaveServiceInModal(event) {
  const button = event.target
  const span = button.previousElementSibling

  const id = span.dataset.id
  const name = span.textContent
  const price = span.dataset.price
  const duration = span.dataset.duration

  const data = {
    id: id,
    name: name,
    price: price,
    duration: duration
  }

  RenderSavedService(data)
}

export function OpenNewServiceModal() {
  const modal = document.getElementById('bookingDialog');
  modal.showModal()

  LoadNewAppointmentListeners()
}

export async function CreateNewAppointment(e) {
  e.preventDefault()
  const data = GetNewAppointmentData()

  await InsertNewAppointmentAPI(data)
}

async function InsertNewAppointmentAPI(data) {
  const resp = await fetch(`${api_url}/api/appointments/create`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': token
    },
    body: JSON.stringify(data)
  })

  const response = await resp.json()

  if (!resp.ok && resp.status == 401) {
    alert('Acesso não autorizado')
    window.location.replace(`${FrontendURL}/login.html`)
  } else if (!resp.ok) {
    ErrorModal(response.message, response.code)
    return
  }

  alert('Agendamento cadastrado com sucesso')
}

function GetNewAppointmentData() {
  const modal = document.getElementById('bookingForm')
  const fields = {
    clientName: ['#contactName', 'Nome'],
    description: ['#description', 'Observação'],
    date: ['#dateDisplay', 'Data'],
    hour: ['#timeInput', 'Hora'],
    duration: ['#duration', 'Duração'],
    price: ['#displayPriceText', 'Preço']
  }

  const data = Object.fromEntries(
    Object.entries(fields).map(([key, [value, translate]]) => {
      const element = modal.querySelector(value)
      let content = element.textContent
      if (content === "" || !content) {
        content = element.value
        if (!content) {
          ErrorModal(`${translate} inexistente`, 'Parâmetros Inválidos')
          return
        }
      }
      return [key, content]
    })
  )

  const dataServices = []
  const listServices = modal.querySelectorAll('.service-selected-option')
  if (!listServices) {
    ErrorModal(`Por favor selecione ao menos 1 serviço`, 'Parâmetros Inválidos')
  }
  listServices.forEach(item => {
    const info = {
      name: item.textContent,
      id: item.dataset.id,
      price: item.dataset.price,
      duration: item.dataset.duration
    }
    dataServices.push(info)
  })
  data.services = dataServices

  const clientId = document.querySelector('#contactName').dataset.id
  data.clientId = clientId

  return data
}

export async function DeleteAppointmentListener(event) {
  const id = event.target.dataset.id
  const modal = document.querySelector('.appointment-detail-modal')

  const confirm = window.confirm('Deseja continuar?')
  if (!confirm) {
    return
  }

  const response = await Request('/api/appointments', 'DELETE', `id=${id}`)
  if (response) {
    alert(response)
  }
  CloseModalRemoveListeners(modal, detailListeners)
  CloseModalRemoveListeners(undefined, appointmentsListeners)
  LoadAppointmentsPage()
}

export async function UpdateAppointmentStatus(event) {
  const id = event.target.dataset.id
  const rawStatus = event.target.textContent

  let status
  switch (rawStatus) {
    case 'Confirmar':
      status = 'confirmado'
      break;
    case 'Cancelar':
      status = 'cancelado'
      break;
    case 'Aguardar':
      status = 'pendente'
      break;
    default:
      break;
  }

  const response = await UpdateStatusAPI(id, status)
  if (response) {
    alert(response)
  }

  CloseModalRemoveListeners(undefined, appointmentsListeners)
  LoadAppointmentsPage()
}

export async function UpdateAppointment(event, price) {
  event.preventDefault()
  const resp = LoadEditData(event, price)
  const id = resp[0]
  const data = resp[1]

  await EditAppointmentAPI(data, id)
  CloseModalRemoveListeners(modal, detailListeners)
  CloseModalRemoveListeners(undefined, appointmentsListeners)
  LoadAppointmentsPage()
}

