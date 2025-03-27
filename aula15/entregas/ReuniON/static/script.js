document.addEventListener('DOMContentLoaded', function() {
    // Modal de reunião (atualizado)
    const modal = document.getElementById('form-modal');
    const span = document.getElementsByClassName('close')[0];
    const addEventButtons = document.getElementsByClassName('add-event');

    for (let button of addEventButtons) {
        button.onclick = function() {
            const day = button.getAttribute('data-day');
            const currentDate = new Date();
            const year = currentDate.getFullYear();
            const month = currentDate.getMonth() + 1;
            
            // Formata a data no formato YYYY-MM-DD
            const formattedDate = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
            
            document.getElementById('event-date').value = formattedDate;
            modal.style.display = 'block';
        };
    }

    span.onclick = function() {
        modal.style.display = 'none';
    };

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    };

    // Mostrar reuniões ao clicar no dia
    const days = document.querySelectorAll('td');
    days.forEach(day => {
        day.addEventListener('click', function(e) {
            if (!e.target.classList.contains('add-event')) {
                const dayNumber = this.querySelector('.day')?.textContent;
                if (dayNumber) {
                    // Aqui você pode implementar a exibição das reuniões do dia
                    alert(`Mostrar reuniões do dia ${dayNumber}`);
                }
            }
        });
    });
});