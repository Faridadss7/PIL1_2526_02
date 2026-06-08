
// Fonction qui vérifie quels éléments doivent apparaître

function revealElements(){

    // Sélectionne tous les éléments ayant la classe "reveal"
    const reveals = document.querySelectorAll(".reveal");

    // Parcourt chaque élément trouvé
    reveals.forEach(element => {

        // Hauteur visible de la fenêtre du navigateur
        const windowHeight = window.innerHeight;

        // Distance entre le haut de l'élément et le haut de l'écran
        const revealTop = element.getBoundingClientRect().top;

        // Distance avant l'apparition de l'élément
        // Plus cette valeur est grande, plus l'animation démarre tôt
        const revealPoint = 100;

        // Vérifie si l'élément est suffisamment visible dans la fenêtre
        if(revealTop < windowHeight - revealPoint){

            // Ajoute la classe "active"
            // Ce qui déclenche l'animation CSS
            element.classList.add("active");
        }

    });

}

 // Exécute la fonction à chaque défilement de la page
 window.addEventListener("scroll", revealElements);

 // Exécute une première fois la fonction au chargement de la page
 // Cela permet d'animer les éléments déjà visibles sans attendre un scroll
 revealElements();

 // Sélectionne tous les liens ayant la classe page-transition
 const links = document.querySelectorAll(".page-transition");

 links.forEach(link => {

     link.addEventListener("click", function(e){

         // Empêche l'ouverture immédiate
         e.preventDefault();

         // Récupère l'adresse du lien
         const destination = this.href;

         // Lance l'animation
         document.body.classList.add("fade-out");

         // Attend 500ms puis change de page
         setTimeout(() => {
             window.location.href = destination;
         }, 500);

     });

});
