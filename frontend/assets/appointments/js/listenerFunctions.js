import { LoadAppointmentsPage, RenderSavedService, RenderServicesListNewAppointment } from "./appointments.js";

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

export function ServiceInputListener(event) {
    const conteudo = event.target.value
    clearTimeout(timer)

    const data = [
        {
            'name': 'Coloração'
        },
        {
            'name': 'Corte'
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
    const element = event.target.closest('.service-option')
    const span = element.querySelector('span')

    RenderSavedService(span.textContent)
}
