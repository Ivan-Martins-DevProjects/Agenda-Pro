const btnClientes = document.getElementById('page-clientes');
const menuLinks = document.querySelectorAll('.menu-link')
const container = document.getElementById('content-container');

const token = sessionStorage.getItem('access-token')

// Cria lista para Renderizar a tabela de clientes
let todosClientes = []

// Adiciona a função carregar clientes ao botão "Clientes" no menu lateral
btnClientes.addEventListener('click', carregarClientes)

async function carregarClientes() {
    try {
        // Remove o estilo de opção ativa de todos os outros elementos
        menuLinks.forEach(l => l.classList.remove('active'))
        // Adicona o estilo de opção ativa ao item Clientes
        btnClientes.classList.add('active')

        // Coleta o token armazenado pela requisição de login
        const token = sessionStorage.getItem('access-token')

        // Requisição para o endpoint que retorna a lista de clientes
        const resposta = await fetch(`${api_url}/api/clients`, {
            method: 'GET',
            headers: {
                'Authorization': token
            }
        })

        const clientes = await resposta.json()

        if (!resposta.ok) {
            ErrorModal(clientes.message, 'Erro ao carregar clientes')
            throw new Error(clientes.message)
        }

        // Adicona a lista recebida a lista vazia criada antes
        todosClientes = clientes.data
        // Renderiza a tabela com as informações recebidas
        renderClients(clientes.data)

    } catch (erro) {
        console.log(erro.message)
        return
    }
}

function renderClients(clientes) {
  if (clientes.length === 0) {
    ;
    return;
  }

  // 1️⃣ Clona o conteúdo do template
  const template = document.getElementById('cliente-template').content.cloneNode(true);

  // 2️⃣ Insere o template no container visível
  container.innerHTML = ''; // limpa conteúdo anterior
  container.appendChild(template);

  // 3️⃣ Seleciona o tbody dentro do template clonado
  const tbody = container.querySelector('#client-table tbody');
  const rowTemplate = tbody.querySelector('tr'); // linha de modelo

  // 4️⃣ Limpa o tbody e adiciona as linhas dos clientes
  tbody.innerHTML = '';

  clientes.forEach(cliente => {
    const clone = rowTemplate.cloneNode(true);
    const info = clone.querySelector('.cliente-nome')
    // Insere o id do cliente diretamente no HTML
    info.textContent = cliente.name;
    info.setAttribute('data-client-id', cliente.id)
    clone.querySelector('.cliente-email').textContent = cliente.email;
    clone.querySelector('.cliente-numero').textContent = cliente.phone
    clone.querySelector('.cliente-responsavel').textContent = cliente.resp;
    clone.querySelector('.cliente-contato').textContent = cliente.last_contact

    // Valida os estilos de status de acordo com a resposta recebida pela api
    const status = clone.querySelector('.status')
    if (cliente.status === 'ativo') {
        status.classList.add('active')
        status.textContent = 'Ativo'
    } else if (cliente.status == 'potencial') {
        status.classList.add('pending')
        status.textContent = 'Potencial'
    } else if (cliente.status == 'inativo') {
        status.classList.add('inactive')
        status.textContent = 'Inativo'
    }

    // Cria o template com as informações recebidas
    tbody.appendChild(clone);

  });
}

async function RequestUniqueContact(id) {
    try {
        const token = sessionStorage.getItem('access-token')

        const response = await fetch(`${api_url}/api/client/${id}/info`, {
            method: 'GET',
            headers: {
                'Content-Type':'application/json',
                'Authorization': token
            }
        })

        const content = await response.json()

        if (!response.ok){
            ErrorModal(content.message, 'Erro ao coletar informações do usuário')
            throw new Error(content.message)
        }


        RenderModalContact(content.data)
        return

    } catch (error) {
        console.error(error)
        return
    }
}

async function DeleteContact(id) {
    try {
        const response = await fetch(`${api_url}/api/clients/delete/${id}`,{
            method: 'DELETE',
            headers: {
                'Content-Type':'application/json',
                'Authorization':token
            }
        })
        const content = await response.json()

        if (!response.ok){
            ErrorModal(content.message, 'Erro ao deletar usuário')
            throw new Error(content.message)
        }

        alert('Contato excluído com sucesso')
    } catch (error) {
        console.error(error)
        return
    }
}

function RenderModalContact(data, message) {
    const modal = document.getElementById('modal-cliente');

    // Preenche os campos do modal
    document.getElementById('nome').value = data.nome;
    document.getElementById('email').value = data.email;
    document.getElementById('telefone').value = data.telefone;
    document.getElementById('cpf').value = data.cpf;
    document.getElementById('rua').value = data.rua;
    document.getElementById('numero').value = data.numero;
    document.getElementById('bairro').value = data.bairro;
    document.getElementById('cidade').value = data.cidade;
    document.getElementById('gasto').value = data.gasto;
    document.getElementById('visitas').value = data.visitas;
    document.getElementById('obs').value = data.obs;

    const title = document.querySelector('.modal-title');
    title.textContent = message;

    modal.showModal();

}

// Abrir modal de adicionar clientes (Método utilizado para evitar problemas com elemento não criado)
document.addEventListener('click', function (e) {
    switch (true) {
        case e.target.matches('.btn-new-contact'):
            const modal = document.getElementById('modal-cliente')
            inputs = [
                'nome', 'email', 'telefone', 'cpf', 'rua', 'numero', 'bairro', 'cidade',
                'gasto', 'visitas', 'obs'
            ]
            inputs.forEach(id => {
                document.getElementById(id).value = ''
            })

            document.querySelector('.modal-title').textContent = 'Cadastro de Clientes';

            register = document.querySelector('.btn-register')
            register.onclick = async (e) => {
                e.preventDefault()
                const token = sessionStorage.getItem('access-token')

                body = {}
                inputs.forEach(id => {
                    body[id] = document.getElementById(id).value
                })

                const response = await fetch(`${api_url}/api/clients/create`,{
                    method : 'POST',
                    headers: {
                        'Content-Type':'application/json',
                        'Authorization': token
                    },
                    body: JSON.stringify(body)
                })

                const content = await response.json()

                document.addEventListener('error-closed', () => {
                        console.log('sucesso')
                        // RenderModalContact(data, 'Cadastro de Clientes')
                    })

                if (!response.ok){
                    modal.close()
                    ErrorModal(content.message, 'Erro ao registrar usuário')
                    return
                } else {
                    modal.close()
                    alert('Contato criado com sucesso')
                    return
                }
            }

            modal.showModal()
            break;

        case e.target.matches('.btn-exit'):
            e.preventDefault()
            const modalClose = document.getElementById('modal-cliente')

            modalClose.close()
            break

        default:
            break;
    }
});

// Função para abrir o modal de edição de contato
document.addEventListener('click', async function (event) {
    // Verifica se o alvo é um botão de edição
    if (event.target && event.target.matches('.edit-contact')) {
        event.stopPropagation()

        const row = event.target.closest('tr')

        const info = row.querySelector('.cliente-nome')
        const id = info.getAttribute('data-client-id')

        const response = await RequestUniqueContact(id)

        RenderModalContact(response)

    } else if (event.target.matches('.exclude-contact')) {
        const row = event.target.closest('tr')
        const info = row.querySelector('.cliente-nome')
        const id = info.getAttribute('data-client-id')

        await DeleteContact(id)
        carregarClientes()
    }
});

