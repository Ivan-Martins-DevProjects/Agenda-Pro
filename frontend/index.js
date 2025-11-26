const btnDashboard = document.getElementById('page-dashboard')
const api_url = 'http://127.0.0.1:8585'

window.addEventListener('DOMContentLoaded', async() => {
    try {
        menuLinks.forEach(l => l.classList.remove('active'))
        btnDashboard.classList.add('active')

        const data = await LoadDashboard(api_url)
        if (!data || data.length === 0) {
            throw new Error ('Erro ao renderizar página')
        }
        console.log(data)

    } catch (error) {
        console.log('Erro ao carregar dashboard' + error)
        return null
    }
})

btnDashboard.addEventListener('click', async() => {
    try {
        const container = document.getElementById('content-container');
        container.innerHTML = ''

        menuLinks.forEach(l => l.classList.remove('active'))
        btnDashboard.classList.add('active')

        const data = await LoadDashboard(api_url)
        if (!data || data.length === 0) {
            container.innerHTML = '<p>Nenhum cliente encontrado.</p>';
            throw new Error('Erro ao renderizar página')
        }
        console.log(data)

    } catch (error) {
        console.log('Erro ao carregar dashboard' + error)
        return null
    }

})

async function LoadDashboard(api_url) {
    try {
        const response = await fetch(`${api_url}/api/dashboard`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })

        if (!response.ok) {
            console.error('Erro com a requisição')
            throw new Error('Requisição inválida')
        }

        const data = await response.json()
        return data

    } catch (error) {
        console.error(error)
        return null
    }
}

// Evento de Dropdown das informações do usuário
document.addEventListener('DOMContentLoaded', function(){
            const dropdown = document.getElementById('userDropdown')
            const dropdownButton = dropdown.querySelector('.user-info')

            dropdownButton.addEventListener('click', function(event){
                event.stopPropagation()
                dropdown.classList.toggle('active')
            })

            document.addEventListener('click', function(event) {
                if (!event.target.closest('.user-dropdown')) {
                    dropdown.classList.remove('active')
                }
            })
        })

