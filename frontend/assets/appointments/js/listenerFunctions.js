
export function FilterDropboxActive(event) {
    const filterContainer = document.querySelector('.custom-filter')
    event.stopPropagation()
    filterContainer.classList.toggle('active')
}

export function ItemsDropbox(event) {
    const filterContainer = document.querySelector('.custom-filter')
    e.stopPropagation();

    options.forEach(opt => opt.classList.remove('selected'));
    option.classList.add('selected');
    selectedText.textContent = option.textContent.trim();
    filterContainer.classList.remove('active');

    const filter = option.getAttribute('data-value')
    LoadAppointmentsPage(filter)
}

