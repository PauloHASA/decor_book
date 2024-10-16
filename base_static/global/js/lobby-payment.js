// document.addEventListener('DOMContentLoaded', function () {
//     const containers = document.querySelectorAll('.container-payment-LobbyPayment');
//     const signPlanButton = document.getElementById('sign-plan');

//     signPlanButton.addEventListener('click', function () {
//         const selectedContainerId = document.querySelector('.select-LobbyPayment').id;

//         // link for payment
//         if (selectedContainerId === 'annual-plan') {
//             window.location.href = 'https://pag.ae/7-qy3f6S4';
//         } else if (selectedContainerId === 'semester-plan') {
//             window.location.href = 'https://sacola.pagbank.com.br/68fd2248-fff2-48a1-9a9b-1dccd839acfb';
//         }
//     });

//     containers.forEach(container => {
//         container.addEventListener('click', function () {
//             containers.forEach(c => c.classList.remove('select-LobbyPayment'));

//             const selectPayments = document.querySelectorAll('.select-payment');
//             selectPayments.forEach(sp => sp.style.display = 'none');

//             this.classList.add('select-LobbyPayment');

//             const selectPayment = this.querySelector('.select-payment');
//             selectPayment.style.display = 'flex';
//         });
//     });
// });