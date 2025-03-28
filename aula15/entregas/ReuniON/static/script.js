document.addEventListener('DOMContentLoaded', function() {
    // Elementos principais
    const addModal = document.getElementById('form-modal');
    const meetingsModal = createMeetingsModal();
    document.body.appendChild(meetingsModal);
    
    // Botões de fechar
    const closeButtons = {
        add: document.querySelector('.close'),
        meetings: document.querySelector('.close-meetings')
    };

    // Inicialização
    initModals();
    initCalendarInteractions();
    initMeetingDeletion();

    // Funções de inicialização
    function createMeetingsModal() {
        const modal = document.createElement('div');
        modal.id = 'meetings-modal';
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <span class="close-meetings">&times;</span>
                <h3>Reuniões do Dia</h3>
                <div id="meetings-list"></div>
            </div>
        `;
        return modal;
    }

    function initModals() {
        // Fechar modais ao clicar nos botões ×
        closeButtons.add.onclick = () => addModal.style.display = 'none';
        closeButtons.meetings.onclick = () => meetingsModal.style.display = 'none';
        
        // Fechar modais ao clicar fora
        window.onclick = function(event) {
            if (event.target === addModal) addModal.style.display = 'none';
            if (event.target === meetingsModal) meetingsModal.style.display = 'none';
        };
    }

    function initCalendarInteractions() {
        // Botão para adicionar reunião
        document.querySelectorAll('.add-event').forEach(button => {
            button.addEventListener('click', function(e) {
                e.stopPropagation();
                const day = this.getAttribute('data-day');
                const currentDate = new Date();
                const formattedDate = formatDate(currentDate, day);
                document.getElementById('event-date').value = formattedDate;
                addModal.style.display = 'block';
            });
        });

        // Células do calendário para mostrar reuniões
        document.querySelectorAll('td').forEach(cell => {
            if (cell.querySelector('.day')) {
                cell.addEventListener('click', function(e) {
                    if (!e.target.classList.contains('add-event')) {
                        const day = cell.querySelector('.day').textContent;
                        const formattedDate = formatDate(new Date(), day);
                        loadMeetings(formattedDate);
                    }
                });
            }
        });
    }

    function initMeetingDeletion() {
        // Deleção dinâmica (para elementos carregados via AJAX)
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('delete-btn')) {
                e.preventDefault();
                e.stopPropagation();
                
                if (confirm('Cancelar esta reunião?')) {
                    const meetingId = e.target.dataset.id;
                    deleteMeeting(meetingId, e.target.closest('.meeting-item'));
                }
            }
        });
    }

    // Funções utilitárias
    function formatDate(date, day) {
        return `${date.getFullYear()}-${(date.getMonth()+1).toString().padStart(2,'0')}-${day.padStart(2,'0')}`;
    }

    function loadMeetings(date) {
        fetch(`/get-meetings?date=${date}`)
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw new Error(err.error || 'Erro na rede'); });
                }
                return response.json();
            })
            .then(data => {
                if (!data.success) throw new Error(data.error || 'Erro desconhecido');
                displayMeetings(data.meetings);
            })
            .catch(error => {
                console.error('Erro:', error);
                alert('Erro: ' + error.message);
            });
    }

    function displayMeetings(meetings) {
        const meetingsList = document.getElementById('meetings-list');
        
        if (meetings && meetings.length > 0) {
            meetingsList.innerHTML = meetings.map(meeting => `
                <div class="meeting-item ${meeting.is_creator ? 'creator' : ''}">
                    <h4>${meeting.title} 
                        ${meeting.is_creator ? 
                            `<button class="delete-btn" data-id="${meeting.id}">×</button>` : ''}
                    </h4>
                    <p><strong>Horário:</strong> ${meeting.time}</p>
                    ${meeting.description ? `<p><strong>Descrição:</strong> ${meeting.description}</p>` : ''}
                    <p><strong>Criador:</strong> ${meeting.creator}</p>
                    <p><strong>Participantes:</strong> 
                        ${meeting.participants.map(p => p.name).join(', ')}
                    </p>
                </div>
            `).join('');
        } else {
            meetingsList.innerHTML = '<p class="no-meetings">Nenhuma reunião agendada para este dia.</p>';
        }
        
        document.getElementById('meetings-modal').style.display = 'block';
    }

    function deleteMeeting(meetingId, element) {
        fetch(`/meeting/delete/${meetingId}`, {
            method: 'GET'
        })
        .then(response => {
            if (!response.ok) throw new Error('Erro ao cancelar reunião');
            return response.json();
        })
        .then(data => {
            if (data.success) {
                element.remove();
                // Atualiza o calendário se necessário
                const currentDate = document.querySelector('#meetings-modal .modal-content h3')
                    .textContent.replace('Reuniões do Dia ', '');
                loadMeetings(currentDate);
            } else {
                throw new Error(data.error || 'Erro ao cancelar reunião');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert(error.message);
        });
    }

    // Atualiza o calendário com eventos existentes
    function highlightMeetings() {
        fetch('/get-meetings?month=current')  // Você precisará criar esta rota
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    data.meetings.forEach(meeting => {
                        const date = new Date(meeting.date);
                        const dayCell = document.querySelector(`td:has(.day:contains("${date.getDate()}"))`);
                        if (dayCell) {
                            dayCell.classList.add('has-meeting');
                        }
                    });
                }
            });
    }
    
    // Inicializa a marcação de reuniões no calendário
    highlightMeetings();
});