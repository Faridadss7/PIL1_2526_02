/* =====================================
   NOTIFICATIONS
===================================== */

document.addEventListener("DOMContentLoaded", () => {

    // Bouton "Tout marquer comme lu"
    const boutonToutLu =
        document.getElementById("btnToutLu");

    // Badge compteur
    const badgeNotifications =
        document.getElementById("badgeNotifications");

    // Toutes les notifications
    const notifications =
        document.querySelectorAll(".carte-notification");


    // ==========================
    // TOUT MARQUER COMME LU
    // ==========================

    if(boutonToutLu){

        boutonToutLu.addEventListener("click", () => {

            notifications.forEach(notification => {

                notification.classList.remove("non-lue");

            });

            if(badgeNotifications){

                badgeNotifications.textContent = "0";

            }

        });

    }

});
/* =====================================
   UNE NOTIFICATION DEVIENT LUE
===================================== */

notifications.forEach(notification => {

    notification.addEventListener("click", () => {

        // Seulement si elle est non lue
        if(notification.classList.contains("non-lue")){

            notification.classList.remove("non-lue");

            if(badgeNotifications){

                let compteur =
                    parseInt(badgeNotifications.textContent);

                compteur--;

                if(compteur < 0){

                    compteur = 0;

                }

                badgeNotifications.textContent = compteur;

            }

        }

    });

});