import ErrorModal, { api_url, token } from "../../index/js/index.js";

const modal = document.querySelector('.appointment-detail-modal');
const btnEdit = document.querySelector('.appointment-detail-edit');

export let isEditing = false;

export async function EditAppointmentAPI(data, id, status) {
  const resp = await fetch(`${api_url}/api/appointments/update?id=${id}&status=${status}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': token
    },
    body: JSON.stringify(data)
  })
  const response = await resp.json()

  // Tratamento de erros de autenticação
  if (!resp.ok && resp.status == 401) {
    alert('Acesso não autorizado')
    window.location.replace(`${FrontendURL}/login.html`)
  } else if (!resp.ok) {
    ErrorModal(response.message, response.code)
  }

  alert('Agendamento atualizado com sucesso')
  modal.close()
  return
}

export function LoadEditData(event) {
  const appointmentId = event.target.dataset.id
  const service = document.getElementById('service')
  const date = document.getElementById('date')
  const hour = document.getElementById('hour')
  const price = document.getElementById('price')
  const rawstatus = document.getElementById('status')
  const obs = document.querySelector('.detail-textarea')

  const status = rawstatus.value

  const data = {
    service: service.value,
    date: date.value,
    hour: hour.value,
    price: price.value,
    obs: obs.value
  }

  return [appointmentId, status, data]
}

export function enterEditMode() {
  modal.style.marginTop = '4%'
  modal.classList.add('is-editing');
  btnEdit.textContent = 'Salvar';
  btnEdit.style.backgroundColor = '#10b981';
  isEditing = true;
}

export function cancelEdit() {
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
