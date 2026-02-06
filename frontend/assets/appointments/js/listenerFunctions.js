import { CloseModalRemoveListeners } from "../../clients/js/clientes.js";
import { appointmentsListeners, detailListeners, LoadAppointmentsPage, LoadNewAppointmentListeners, RenderSavedService, RenderServicesListNewAppointment } from "./appointments.js";
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

export function ServiceInputListener() {
  clearTimeout(timer)
  const data = [
    {
      'name': 'Coloração',
      'duration': 30,
      'price': 50
    },
    {
      'name': 'Corte',
      'duration': 40,
      'price': 80
    }
  ]

  const serviceList = document.querySelectorAll('.service-option')
  if (serviceList) {
    serviceList.forEach(item => {
      item.remove()
    })
  }

  timer = setTimeout(() => {
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
  const element = event.target.closest('div')
  const span = element.querySelector('span')

  const name = span.textContent
  const price = span.dataset.price
  const duration = span.dataset.duration

  const data = {
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

export function GetNewAppointmentData() {
  const modal = document.getElementById('bookingForm')

  const formData = new FormData(modal)
  const dados = Object.fromEntries(formData.entries())
  return dados
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
  const resp = LoadEditData(event, price)
  const id = resp[0]
  const data = resp[1]

  await EditAppointmentAPI(data, id)
  CloseModalRemoveListeners(modal, detailListeners)
  CloseModalRemoveListeners(undefined, appointmentsListeners)
  LoadAppointmentsPage()
}

