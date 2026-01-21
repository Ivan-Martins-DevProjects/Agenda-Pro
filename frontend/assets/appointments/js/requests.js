import { api_url, token } from "../../index/js/index.js"
import { FrontendURL } from "../../clients/js/clientes.js"
import ErrorModal from "../../index/js/index.js"

export async function Request(endpoint, method, params) {
  let url
  try {
    if (params) {
      url = `${api_url}${endpoint}?${params}`
    } else {
      url = `${api_url}${endpoint}`
    }

    const request = await fetch(url, {
      method: method,
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
      const message = response.message
      const code = response.code
      if (!message || !code) {
        ErrorModal('Erro interno do Cliente', 'CLIENT_INTERNAL_ERROR')
        throw new Error('Erro do cliente')
      }
      ErrorModal(response.message, response.code)
      throw new Error(response.code)
    }

    return response

  } catch (error) {
    console.warn(error)
  }
}


export async function UpdateStatusAPI(id, status) {
  try {
    const request = await fetch(`${api_url}/api/appointments/status?id=${id}&status=${status}`, {
      method: 'PUT',
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
      const message = response.message
      const code = response.code
      if (!message || !code) {
        ErrorModal('Erro interno do Cliente', 'CLIENT_INTERNAL_ERROR')
        throw new Error('Erro do cliente')
      }
      ErrorModal(response.message, response.code)
      throw new Error(response.code)
    }

    return response

  } catch (error) {
    console.warn(error)
    return
  }
}

export async function AppointmentsAPI(offset, filter, filterType) {
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
