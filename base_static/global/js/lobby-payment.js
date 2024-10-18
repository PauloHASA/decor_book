function selectPlan(planId) {
    console.log(planId);
    document.getElementById('plan_id').value = planId;
}
document.addEventListener('DOMContentLoaded', function () {
    const containers = document.querySelectorAll('.container-payment-LobbyPayment');

    containers.forEach(container => {
        container.addEventListener('click', function () {
            containers.forEach(c => c.classList.remove('select-LobbyPayment'));

            const selectPayments = document.querySelectorAll('.select-payment');
            selectPayments.forEach(sp => sp.style.display = 'none');

            this.classList.add('select-LobbyPayment');

            const selectPayment = this.querySelector('.select-payment');
            selectPayment.style.display = 'flex';
        });
    });
});