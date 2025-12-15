export default function RenderServices(services) {
    const content = document.querySelector('.content')

    content.innerHTML = ''

    if (services.length === 0) {
        document.createElement('h1')
        h1.textContent = 'Nenhum serviço encontrado'
        h1.style.marginTop = '15%'
        h1.style.marginLeft = '35%'
    }

    const header = document.createElement('div')

    // Header
    const headerDiv = document.createElement('div')
    headerDiv.className = 'services-header'

    const headerTitle = document.createElement('h2')
    headerTitle.textContent = 'Serviços Cadastrados'

    const headerBtn = document.createElement('button')
    headerBtn.className = 'new-service'
    headerBtn.textContent = 'Novo cadastro'

    headerDiv.appendChild(headerTitle)
    headerDiv.appendChild(headerBtn)
    header.appendChild(headerDiv)
    content.appendChild(header)

    const containers = document.createElement('div')
    containers.className = 'services-containers'

    services.forEach(item => {
        // Header do Card
        const main = document.createElement('div')
        main.className = 'container'

        const headerDiv = document.createElement('div')
        headerDiv.className = 'services-card-header'

        const h3 = document.createElement('h3')
        h3.textContent = item.name

        headerDiv.appendChild(h3)
        main.appendChild(headerDiv)

        // Descrição card
        const body = document.createElement('div')
        body.className = 'services-card-body'

        const p = document.createElement('p')
        p.textContent = item.description

        body.appendChild(p)
        main.appendChild(body)

        // Preço e duração card
        const info = document.createElement('div')
        info.className = 'services-card-price-duration'

        const price = document.createElement('span')
        price.className = 'services-price'
        price.textContent = 'R$ ' + item.price + ',00'

        const duration = document.createElement('span')
        duration.className = 'services-duration'
        duration.textContent = item.duration + ' min'

        info.appendChild(price)
        info.appendChild(duration)
        main.appendChild(info)

        // Botões footer card
        const footer = document.createElement('div')
        footer.className = 'services-card-footer'

        const editBtn = document.createElement('button')
        editBtn.className = 'btn-services-edit'
        editBtn.textContent = 'Editar'

        const excludeBtn = document.createElement('button')
        excludeBtn.className = 'btn-services-exclude'
        excludeBtn.textContent = 'Excluir'

        footer.appendChild(editBtn)
        footer.appendChild(excludeBtn)
        main.appendChild(footer)

        containers.appendChild(main)
        content.appendChild(containers)
    });

}
