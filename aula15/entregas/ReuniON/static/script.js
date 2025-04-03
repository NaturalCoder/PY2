document.addEventListener('DOMContentLoaded', function() {
    // Elementos dos modais
    const formModal = document.getElementById('form-modal');
    const meetingsModal = document.getElementById('meetings-modal');
    const closeButtons = document.querySelectorAll('.close');
    
    // Modal de agendamento
    const setupAddEventButtons = () => {
        document.querySelectorAll('.add-event').forEach(button => {
            button.addEventListener('click', function(e) {
                e.stopPropagation();
                const day = this.getAttribute('data-day');
                const currentDate = new Date();
                const formattedDate = `${currentDate.getFullYear()}-${(currentDate.getMonth()+1).toString().padStart(2,'0')}-${day.padStart(2,'0')}`;
                document.getElementById('event-date').value = formattedDate;
                formModal.style.display = 'block';
            });
        });
    };

    // Modal de visualização de reuniões
    const setupDayClickHandlers = () => {
        document.querySelectorAll('td').forEach(cell => {
            const dayElement = cell.querySelector('.day');
            if (dayElement) {
                cell.addEventListener('click', function() {
                    const day = dayElement.textContent;
                    const currentDate = new Date();
                    const dateStr = `${currentDate.getFullYear()}-${(currentDate.getMonth()+1).toString().padStart(2,'0')}-${day.padStart(2,'0')}`;
                    
                    fetch(`/get-meetings?date=${dateStr}`)
                        .then(response => {
                            if (!response.ok) throw new Error('Erro na requisição');
                            return response.json();
                        })
                        .then(meetings => {
                            renderMeetings(meetings, day, currentDate);
                        })
                        .catch(error => {
                            console.error('Erro:', error);
                            alert('Erro ao carregar reuniões');
                        });
                });
            }
        });
    };

    // Renderizar reuniões no modal
    const renderMeetings = (meetings, day, currentDate) => {
        const meetingsList = document.getElementById('meetings-list');
        meetingsList.innerHTML = '';
        
        if (meetings.length > 0) {
            meetings.forEach(meeting => {
                const meetingEl = document.createElement('div');
                meetingEl.className = 'meeting-item';
                meetingEl.innerHTML = `
                    <div class="meeting-header">
                        <h4>${meeting.title}</h4>
                        <span class="meeting-time">${meeting.time}</span>
                    </div>
                    <div class="meeting-details">
                        ${meeting.location ? `<p><strong>Local:</strong> ${meeting.location}</p>` : ''}
                        ${meeting.participants.length ? `<p><strong>Participantes:</strong> ${meeting.participants.join(', ')}</p>` : ''}
                    </div>
                    <div class="meeting-actions">
                        <button class="btn-delete" onclick="deleteMeeting(${meeting.id})">
                            Cancelar Reunião
                        </button>
                    </div>
                `;
                meetingsList.appendChild(meetingEl);
            });
        } else {
            meetingsList.innerHTML = '<div class="no-meetings">Nenhuma reunião agendada para este dia</div>';
        }
        
        document.getElementById('selected-date').textContent = 
            `Reuniões em ${day.padStart(2,'0')}/${(currentDate.getMonth()+1).toString().padStart(2,'0')}`;
        meetingsModal.style.display = 'block';
    };

    // Fechar modais
    const setupCloseHandlers = () => {
        closeButtons.forEach(btn => {
            btn.addEventListener('click', function() {
                formModal.style.display = 'none';
                meetingsModal.style.display = 'none';
            });
        });

        window.addEventListener('click', function(event) {
            if (event.target === formModal || event.target === meetingsModal) {
                formModal.style.display = 'none';
                meetingsModal.style.display = 'none';
            }
        });
    };

    // Função para deletar reunião (disponível globalmente)
    window.deleteMeeting = function(id) {
        if (confirm('Tem certeza que deseja cancelar esta reunião?')) {
            fetch(`/meeting/delete/${id}`, { 
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                }
            })
            .then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    alert('Erro ao cancelar reunião');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Erro ao cancelar reunião');
            });
        }
    };

    // Obter token CSRF (proteção contra ataques)
    const getCSRFToken = () => {
        const csrfToken = document.querySelector('meta[name="csrf-token"]');
        return csrfToken ? csrfToken.content : '';
    };

    // Inicialização
    setupAddEventButtons();
    setupDayClickHandlers();
    setupCloseHandlers();

    // Destacar dias com reuniões
    highlightDaysWithMeetings();
});

// Função para destacar dias com reuniões
function highlightDaysWithMeetings() {
    // Esta função pode ser preenchida com lógica para destacar dias
    // Exemplo: adicionar classe 'has-meetings' aos dias com eventos
}