const btnOpen = document.querySelector('.btn-open');
const modal = document.querySelector('.appointment-detail-modal');
const btnClose = document.querySelector('.appointment-detail-close');
const btnEdit = document.querySelector('.appointment-detail-edit');

export let isEditing = false;
function EditAppointmentAPI(params) {

}

function LoadEditData(event) {
    const appointmentId = event.target.dataset.id
    const service = document.getElementById('service')
    const date = document.getElementById('date')
    const hour = document.getElementById('hour')
    const price = document.getElementById('price')
    const status = document.getElementById('status')
    const obs = document.querySelector('.detail-textarea')

    const data = {
        id: appointmentId.value,
        service: service.value,
        date: date.value,
        hour: price.value,
        stauts: status.value,
        obs: obs.value
    }
}

export function enterEditMode(event) {
    if (event.target.textContent == 'Salvar') {
        LoadEditData(event)
        return
    }
    modal.style.marginTop = '4%'
    modal.classList.add('is-editing');
    btnEdit.textContent = 'Salvar';
    btnEdit.style.backgroundColor = '#10b981';
    isEditing = true;
}

function saveChanges() {
    const rows = document.querySelectorAll('.detail-input')
    rows.forEach(item => {
        console.log(item.value)
    })
    exitEditMode();
}

function cancelEdit() {
    exitEditMode();
}

export function exitEditMode() {
    if (isEditing) {
        modal.style.marginTop = '7%'
        modal.classList.remove('is-editing');
        btnEdit.textContent = 'Editar';
        btnEdit.style.backgroundColor = '#4f46e5';
        isEditing = false;
    }
}

