function toggleActive(checkbox) {
    var user_id = checkbox.closest('tr').querySelector('.field-id').innerText;
    var url = '/admin/your_appname/customusermodel/' + user_id + '/toggle_active/';
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao alternar ativação do usuário');
            }
            return response.json();
        })
        .then(data => {
            checkbox.checked = data.is_active;
        })
        .catch(error => {
            console.error('Erro:', error);
        });
}

function togglePaid(checkbox) {
    var user_id = checkbox.closest('tr').querySelector('.field-id').innerText;
    var url = '/admin/your_appname/customusermodel/' + user_id + '/toggle_paid/';
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao alternar status de pagamento do usuário');
            }
            return response.json();
        })
        .then(data => {
            checkbox.checked = data.is_paid;
        })
        .catch(error => {
            console.error('Erro:', error);
        });
}



const linkElement = document.getElementById('pub-ProjectPage-link');
const buttonElement = document.getElementById('pub-ProjectPage-btn');
const modalElement = document.getElementById('modal-PubPage');

linkElement.addEventListener('click', toggleModalDisplay);
buttonElement.addEventListener('click', toggleModalDisplay);

function toggleModalDisplay() {
    if (modalElement.style.display === 'none' || modalElement.style.display === '') {
        modalElement.style.display = 'flex';
    } else {
        modalElement.style.display = 'none';
    }
}