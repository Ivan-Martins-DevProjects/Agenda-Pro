import ErrorModal, { api_url, token } from "../../index/js/index.js";

const modal = document.querySelector('.appointment-detail-modal');
const btnEdit = document.querySelector('.appointment-detail-edit');

export let isEditing = false;

export async function EditAppointmentAPI(data, id) {
  const resp = await fetch(`${api_url}/api/appointments/update?id=${id}`, {
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
    return
  } else if (!resp.ok) {
    ErrorModal(response.message, response.code)
    return
  }

  alert('Agendamento atualizado com sucesso')
  modal.close()
  return
}

export function LoadEditData(event) {
  const modal = document.getElementById('bookingDialog')

  const appointmentId = event.target.dataset.id
  const date = modal.querySelector('#dateDisplay')
  const hour = modal.querySelector('#timeInput')
  const price = modal.querySelector('#displayPriceText')
  const duration = modal.querySelector('#duration')
  const obs = modal.querySelector('#description')

  const priceValue = price.textContent
  let finalPrice
  if (priceValue) {
    finalPrice = priceValue.replace(/[^\d.]/g, '')
  }

  const serviceData = []
  const servicesList = modal.querySelectorAll('.service-selected-option')
  servicesList.forEach(item => {
    const data = {
      duration: item.dataset.duration,
      price: item.dataset.price,
      id: item.dataset.id,
      name: item.textContent
    }

    serviceData.push(data)
  })

  const data = {
    services: serviceData,
    date: date.value,
    time_begin: hour.value,
    price: finalPrice,
    obs: obs.value,
    duration: duration.value.replace(/[^\d.]/g, '')
  }
  console.log(data)

  return [appointmentId, data]
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
