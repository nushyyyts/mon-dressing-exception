document.addEventListener('DOMContentLoaded', function() {
    const loginLink = document.querySelector('.auth-switch a[href="login.html"]');
    const registerLink = document.querySelector('.auth-switch a[href="register.html"]');
    const loginContainer = document.querySelector('.auth-container:not(.register-container)');
    const registerContainer = document.querySelector('.auth-container.register-container');

    // Fonction pour afficher le formulaire de connexion
    function showLogin() {
        if (loginContainer && registerContainer) {
            loginContainer.style.display = 'block';
            registerContainer.style.display = 'none';
        }
    }

    // Fonction pour afficher le formulaire d'inscription
    function showRegister() {
        if (loginContainer && registerContainer) {
            loginContainer.style.display = 'none';
            registerContainer.style.display = 'block';
        }
    }

    // Gérer l'état initial basé sur l'URL
    const urlParams = new URLSearchParams(window.location.search);
    const formType = urlParams.get('form'); // exemple: login.html?form=register

    if (formType === 'register' || window.location.pathname.includes('register.html')) {
        showRegister();
    } else {
        showLogin();
    }


    // Écouteurs d'événements pour les liens de basculement
    if (loginLink) {
        loginLink.addEventListener('click', function(e) {
            e.preventDefault(); // Empêche le rechargement de la page
            showLogin();
            history.pushState(null, '', 'login.html'); // Met à jour l'URL sans recharger
        });
    }

    if (registerLink) {
        registerLink.addEventListener('click', function(e) {
            e.preventDefault(); // Empêche le rechargement de la page
            showRegister();
            history.pushState(null, '', 'login.html?form=register'); // Met à jour l'URL sans recharger
        });
    }

    // Gérer le cas où l'utilisateur arrive directement sur register.html ou est redirigé
    // Ce bloc vérifie l'URL actuelle et affiche le bon formulaire
    if (window.location.pathname.includes('register.html') && !window.location.search.includes('form=register')) {
        showRegister();
    }
});