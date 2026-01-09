const container = document.querySelector('.content-container')

const appointments = [
    {
        service: "Coloração",
        status: "Confirmado",
        client: "Ivan Martins",
        resp: "Manu Oliveira",
        date: "12 Out",
        hour: "12:00"
    },
    {
        service: "Corte Masculino",
        status: "Cancelado",
        client: "Carlos Silva",
        resp: "Ana Souza",
        date: "15 Out",
        hour: "14:30"
    }
];

export function RenderAppointments(appointments) {
    const template = document.querySelector('.appointments-template')
    const container = document.querySelector('.content')

    container.innerHTML = ''
    if (appointments.length === 0) {

        const h1 = document.createElement('h1')
        h1.textContent = 'Nenhum cliente encontrado'
        h1.style.marginTop = '15%'
        h1.style.marginLeft = '35%'

        container.append(h1)
        return;
    }

    const clone = template.content.cloneNode(true)
    const body = clone.querySelector('.appointments-body')
    const cardTemplate = clone.querySelector('.appointment-container')
    body.innerHTML = ''

    appointments.forEach(item => {
        const card = cardTemplate.cloneNode(true)
        card.querySelector('.appointment-container-title h3').textContent = item.service
        card.querySelector('.appointment-client').textContent = item.client
        card.querySelector('.appointment-resp').textContent = item.resp
        card.querySelector('.appointment-date').textContent = item.date
        card.querySelector('.appointment-hour').textContent = item.hour

        const status = card.querySelector('.appointment-container-status span')
        switch (item.status.toLowerCase()) {
            case 'confirmado':
                status.style.backgroundColor = '#DCFCE7'
                status.style.color = '#166534'
                break;
            case 'pendente':
                status.style.backgroundColor = '#e2e680'
                status.style.color = '#7b7f03'
                break
            case 'cancelado':
                status.style.backgroundColor = '#d00b0b57'
                status.style.color = '#d00b0bc7'
                break
            default:
                status.style.backgroundColor = '#ccc'
                status.style.color = '#ccc'
                break
        }

        status.textContent = item.status
        body.appendChild(card)
    })

    container.appendChild(clone)
}
