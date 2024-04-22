
const searchInput = document.getElementById('search-input');

searchInput.addEventListener('input', function() {
    const searchText = this.value.trim().toLowerCase();

    const posts = document.querySelectorAll('.img-timeline');

    console.log("Search Text:", searchText); // Verificando o texto de busca

    posts.forEach(post => {
        const userName = post.querySelector('.user-info-TimeLine h1:first-child').textContent.toLowerCase();
        const userProfession = post.querySelector('.user-info-TimeLine h1:nth-child(2)').textContent.toLowerCase();

        console.log("User Name:", userName); // Verificando o nome do usuário
        console.log("User Profession:", userProfession); // Verificando a profissão do usuário

        if (userName.includes(searchText) || userProfession.includes(searchText)) {
            post.style.display = 'block';
        } else {
            post.style.display = 'none';
        }
    });

    if (searchText === '') {
        posts.forEach(post => {
            post.style.display = 'block';
        });
    }
});