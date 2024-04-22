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