import {api_url, token} from "./index.js"
import { ActionComplete, FrontendURL, PaginationListener, CreatePagination, nextPage } from "./clientes.js"
import ErrorModal from "./index.js"
//
// --- 1. DADOS DE SERVIÇOS (Desacoplado do HTML) ---
// Simulando dados que viriam do seu backend
const servicesData = [
    { id: "1", name: "Consultoria" },
    { id: "2", name: "Manutenção" },
    { id: "3", name: "Design" },
    { id: "4", name: "Desenvolvimento" }
];

// Função dedicada para renderizar a lista de serviços
function renderAppointmentServices() {
    const selectElement = document.getElementById('serviceSelect');

    // Limpa opções existentes (mantendo a primeira padrão se necessário, ou recriando tudo)
    selectElement.innerHTML = '<option value="" disabled selected>Selecione um serviço</option>';

    servicesData.forEach(service => {
        const option = document.createElement('option');
        option.value = service.id;
        option.textContent = service.name;
        selectElement.appendChild(option);
    });
}

// --- 2. LÓGICA DO DIALOG E CALENDÁRIO ---

// Elementos do Dialog
const dialog = document.getElementById('bookingDialog');
const cancelBtn = document.getElementById('cancelBtn');

// Fechar Modal (Botão Cancelar)
cancelBtn.addEventListener('click', () => {
    dialog.close();
    resetForm();
});

// Fechar Modal ao clicar no backdrop (fundo escuro)
dialog.addEventListener('click', (event) => {
    if (event.target === dialog) {
        dialog.close();
        resetForm();
    }
});

// Configurações e Estado do Calendário
const state = {
    currentDate: new Date(),
    selectedDate: null
};

const months = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
];

// Elementos DOM
const calendarDays = document.getElementById('calendarDays');
const currentMonthYear = document.getElementById('currentMonthYear');
const prevMonthBtn = document.getElementById('prevMonth');
const nextMonthBtn = document.getElementById('nextMonth');

const form = document.getElementById('bookingForm');
const contactInput = document.getElementById('contactName');
const serviceSelect = document.getElementById('serviceSelect');
const dateDisplay = document.getElementById('dateDisplay');
const timeInput = document.getElementById('timeInput');
const displayPriceText = document.getElementById('displayPriceText');
const priceValueHidden = document.getElementById('priceValue');

prevMonthBtn.addEventListener('click', () => {
    changeMonth(-1)
})

nextMonthBtn.addEventListener('click', () => {
    changeMonth(1)
})

// Funções do Calendário
function renderCalendar() {
    calendarDays.innerHTML = "";

    const year = state.currentDate.getFullYear();
    const month = state.currentDate.getMonth();

    // Atualizar cabeçalho
    currentMonthYear.textContent = `${months[month]} ${year}`;

    // Lógica de dias
    const firstDayIndex = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const today = new Date();

    // Espaços vazios
    for (let i = 0; i < firstDayIndex; i++) {
        const emptyDiv = document.createElement('div');
        emptyDiv.classList.add('appointment-day', 'appointment-empty');
        calendarDays.appendChild(emptyDiv);
    }

    // Dias do mês
    for (let i = 1; i <= daysInMonth; i++) {
        const dayDiv = document.createElement('div');
        dayDiv.classList.add('appointment-day');
        dayDiv.textContent = i;

        // Hoje
        if (i === today.getDate() && month === today.getMonth() && year === today.getFullYear()) {
            dayDiv.classList.add('appointment-today');
        }

        // Selecionado
        if (state.selectedDate &&
            i === state.selectedDate.getDate() &&
            month === state.selectedDate.getMonth() &&
            year === state.selectedDate.getFullYear()) {
            dayDiv.classList.add('appointment-selected');
        }

        dayDiv.addEventListener('click', () => selectDate(i));
        calendarDays.appendChild(dayDiv);
    }
}

function selectDate(day) {
    const year = state.currentDate.getFullYear();
    const month = state.currentDate.getMonth();

    state.selectedDate = new Date(year, month, day, 12, 0, 0);

    renderCalendar();

    // Formatar data para o input
    const isoDate = state.selectedDate.toISOString().split('T')[0];
    const displayDateFormatted = state.selectedDate.toLocaleDateString('pt-BR');

    dateDisplay.value = displayDateFormatted;
    dateDisplay.dataset.dateIso = isoDate;

    // Feedback visual
    dateDisplay.style.backgroundColor = '#e0e7ff';
    setTimeout(() => {
        dateDisplay.style.backgroundColor = '#f8fafc';
    }, 300);
}

function changeMonth(offset) {
    state.currentDate.setMonth(state.currentDate.getMonth() + offset);
    renderCalendar();
}

serviceSelect.addEventListener('change', async (e) => {
    const serviceId = e.target.value;
    // Aqui você chamaria seu backend para pegar o preço real
});

function updatePriceDisplay(value) {
    displayPriceText.textContent = parseFloat(value).toLocaleString('pt-BR', { minimumFractionDigits: 2 });
    priceValueHidden.value = value;
}

function resetForm() {
    form.reset();
    state.selectedDate = null;
    updatePriceDisplay("0,00");
    renderCalendar();
}

// Feedback Visual (Toast)
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const toastMsg = document.getElementById('toastMessage');

    toast.className = `appointment-toast appointment-${type} appointment-show`;
    toastMsg.textContent = message;

    setTimeout(() => {
        toast.classList.remove('appointment-show');
    }, 3000);
}

// Submissão do Formulário
form.addEventListener('submit', (e) => {
    e.preventDefault();

    // Captura de dados para enviar ao Backend
    const formData = {
        contact: contactInput.value,
        serviceId: serviceSelect.value,
        date: dateDisplay.dataset.dateIso,
        time: timeInput.value
    };

    if (!state.selectedDate) {
        showToast("Selecione uma data no calendário.", "error");
        return;
    }

    console.log("Enviando dados para o backend:", formData);

    // Simulação de envio
    showToast("Agendamento enviado com sucesso!", "success");
    dialog.close();

    setTimeout(() => {
        resetForm();
    }, 500);
});

// Inicializar
document.addEventListener('DOMContentLoaded', () => {
    renderAppointmentServices(); // Renderiza a lista de serviços
    renderCalendar();             // Renderiza o calendário
});


