document.addEventListener('DOMContentLoaded', function() {
    const addItemFormSection = document.querySelector('.add-item-form-section');
    const editItemFormSection = document.querySelector('.edit-item-form-section'); // Nouveau
    const editItemForm = document.querySelector('.edit-item-form'); // Nouveau

    // Fonction pour afficher le formulaire d'ajout d'article
    window.showAddItemForm = function() {
        if (addItemFormSection) {
            addItemFormSection.style.display = 'block';
            editItemFormSection.style.display = 'none'; // Cache le formulaire d'édition
            window.scrollTo({
                top: addItemFormSection.offsetTop - 50,
                behavior: 'smooth'
            });
        }
    };

    // Fonction pour masquer le formulaire d'ajout d'article
    window.hideAddItemForm = function() {
        if (addItemFormSection) {
            addItemFormSection.style.display = 'none';
        }
    };

    // Fonction pour afficher le formulaire de modification et le pré-remplir
    window.showEditItemForm = function(itemId) {
        // Dans un vrai projet, vous feriez une requête AJAX pour récupérer les détails de l'article par son ID.
        // Pour cet exemple, on va simuler la récupération ou utiliser les données disponibles si possible.
        // Puisque Flask passe déjà l'objet 'item_to_edit' à la page my-showcase.html quand on arrive via /edit/<id>,
        // cette logique serait généralement gérée côté Flask.
        // Ici, on va juste s'assurer que le formulaire apparaît si le JS est appelé manuellement.

        const itemCard = document.querySelector(`.item-card form[action$="/delete/${itemId}"]`).closest('.item-card');
        if (itemCard) {
            const name = itemCard.querySelector('h3').textContent;
            const detailsText = itemCard.querySelector('.item-details').innerHTML;
            const descriptionMatch = detailsText.match(/Description: ([^<]+)/); // Ceci n'est pas fiable, idéalement passe la description du back-end
            const yearMatch = detailsText.match(/Année: (\d{4})/);
            const conditionMatch = detailsText.match(/État: ([^<]+)/);
            const isRare = detailsText.includes('✨ Pièce Rare');
            const imageUrl = itemCard.querySelector('img').src;

            // Remplir le formulaire de modification
            document.getElementById('edit-item-id').value = itemId;
            document.getElementById('edit-item-name').value = name;
            // document.getElementById('edit-item-description').value = descriptionMatch ? descriptionMatch[1].trim() : ''; // Plus complexe sans la description directe
            if (yearMatch) document.getElementById('edit-item-year').value = yearMatch[1];
            if (conditionMatch) document.getElementById('edit-item-condition').value = conditionMatch[1].trim();
            document.getElementById('edit-is-rare').checked = isRare;
            document.getElementById('current-item-image').src = imageUrl;

            // Définir l'action du formulaire pour qu'il pointe vers la route de modification de Flask
            editItemForm.action = `/my-showcase/edit/${itemId}`;
        }
        
        if (editItemFormSection) {
            editItemFormSection.style.display = 'block';
            addItemFormSection.style.display = 'none'; // Cache le formulaire d'ajout
            window.scrollTo({
                top: editItemFormSection.offsetTop - 50,
                behavior: 'smooth'
            });
        }
    };

    // Fonction pour masquer le formulaire de modification
    window.hideEditItemForm = function() {
        if (editItemFormSection) {
            editItemFormSection.style.display = 'none';
        }
    };

    // Gestion du lien de déconnexion (inchangé)
    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', function(e) {
            e.preventDefault();
            const confirmLogout = confirm('Êtes-vous sûr de vouloir vous déconnecter ?');
            if (confirmLogout) {
                window.location.href = this.href; // Laisse Flask gérer la déconnexion via la route /logout
            }
        });
    }

    // Gérer l'affichage initial du formulaire d'édition si la page est chargée avec un item_to_edit (venant de Flask)
    // C'est utile si Flask redirige vers my-showcase.html après une erreur de modification
    // ou si on accède directement à /my-showcase/edit/<id>
    const urlPath = window.location.pathname;
    if (urlPath.includes('/my-showcase/edit/') && editItemFormSection) {
        const itemIdMatch = urlPath.match(/\/my-showcase\/edit\/(\d+)/);
        if (itemIdMatch && itemIdMatch[1]) {
            // Le pré-remplissage du formulaire et l'affichage sont mieux gérés par Flask
            // quand il rend le template avec item_to_edit.
            // Ce JS assure juste que le bon formulaire est visible si on accède directement.
            editItemFormSection.style.display = 'block';
            addItemFormSection.style.display = 'none';
            window.scrollTo({
                top: editItemFormSection.offsetTop - 50,
                behavior: 'smooth'
            });
        }
    }
});