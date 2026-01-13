const filterContainer = document.getElementById('customFilter');
const trigger = filterContainer.querySelector('.filter-trigger');
const options = filterContainer.querySelectorAll('.filter-option');
const selectedText = filterContainer.querySelector('.selected-text');

trigger.addEventListener('click', (e) => {
    e.stopPropagation();
    filterContainer.classList.toggle('active');
});

options.forEach(option => {
    option.addEventListener('click', (e) => {
        e.stopPropagation();

        options.forEach(opt => opt.classList.remove('selected'));

        option.classList.add('selected');

        selectedText.textContent = option.textContent.trim();

        filterContainer.classList.remove('active');

        console.log("Filtro selecionado:", option.getAttribute('data-value'));
    });
});

document.addEventListener('click', (e) => {
    if (!filterContainer.contains(e.target)) {
        filterContainer.classList.remove('active');
    }
});
