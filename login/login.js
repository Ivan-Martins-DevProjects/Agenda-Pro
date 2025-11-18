    const api_url = "http://localhost:8181"
    // Login
     document.getElementById('login-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {

        const response = await fetch(`${api_url}/api/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                senha: password
            })
        });

        const data = await response.json()

        if (!response.ok) {
            console.log(data)
            return ErrorModal(data.message, data.code)
        }

        console.log(`Login bem-sucedido! Redirecionando`)
        window.location.href = '/#'

    } catch (error) {
        console.error("Erro no Login:", error);
        ErrorModal(error.message, 500);
    }
});

    // Modal de Erro
    function ErrorModal(message, code) {
        const errorModal = document.getElementById('error-modal-template')
        const errorClone = errorModal.content.cloneNode(true)
        errorClone.querySelector('#modal-message').textContent = message
        document.body.appendChild(errorClone)

    }

    // Fechar modal de Erro
    document.body.addEventListener('click', function(event) {
            if (event.target.matches('.close-modal-btn') || event.target.matches('.modal-overlay')) {
                const modalOverlay = event.target.closest('.modal-overlay');
                if (modalOverlay) {
                    modalOverlay.remove();
                }
            }
        });
