const btnDashboard = document.getElementById('page-dashboard')
const api_url = 'http://localhost:8181'

window.addEventListener('DOMContentLoaded', () => {
    try {
        menuLinks.forEach(l => l.classList.remove('active'))
        btnDashboard.classList.add('active')

        const data = LoadDashboard(api_url)
        console.log(data)

    } catch (error) {
        console.log('Erro ao carregar dashboard' + error)
    }
})

btnDashboard.addEventListener('click', () => {
    try {
        menuLinks.forEach(l => l.classList.remove('active'))
        btnDashboard.classList.add('active')

        const data = LoadDashboard(api_url)
        console.log(data)

    } catch (error) {
        console.log('Erro ao carregar dashboard' + error)
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

        const data = await response.json()

        if (!response.ok) {
            console.error('Erro com a requisição')
        }
        return data
    } catch (error) {
        console.error(error)
        throw error
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

