document.addEventListener('DOMContentLoaded', function() {
    // Cette partie est maintenant gérée principalement par Flask qui passe les données au template
    // const urlParams = new URLSearchParams(window.location.search);
    // const userId = urlParams.get('user');

    // // Exemple de mise à jour du titre basé sur l'URL (pour la démonstration)
    // // Dans un vrai site, ceci viendrait du back-end
    // if (userId) {
    //     document.title = `Vitrine de ${userId} - Mon Dressing d'Exception`;
    //     const profileHeader = document.querySelector('.profile-info h1');
    //     if (profileHeader) {
    //         profileHeader.textContent = `Vitrine de ${userId.charAt(0).toUpperCase() + userId.slice(1)}`;
    //     }
    //     const userItemsSection = document.querySelector('.user-items-section h2');
    //     if (userItemsSection) {
    //         userItemsSection.textContent = `Collection de ${userId.charAt(0).toUpperCase() + userId.slice(1)}`;
    //     }
    // }

    // Gérer les clics sur les boutons "Voir les détails"
    const viewDetailButtons = document.querySelectorAll('.view-item-detail-button');
    viewDetailButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Ici, dans un vrai projet, cela redirigerait vers une page de détail de l'article
            // ou ouvrirait une modale avec les infos de l'article.
            alert("Fonctionnalité 'Voir les détails de l'article' à implémenter !");
            // window.location.href = `item-detail.html?itemid=${itemId}`;
        });
    });

    // Ici, vous ajouteriez du code JavaScript pour :
    // - Effectuer une requête au back-end pour récupérer les détails de l'utilisateur et ses articles
    // - Remplir dynamiquement le `profile-header` et `items-grid` avec les données reçues
    // - Gérer la pagination si nécessaire
});