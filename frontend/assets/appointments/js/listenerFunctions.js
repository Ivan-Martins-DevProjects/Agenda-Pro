import { LoadAppointmentsPage } from "./appointments.js";

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

