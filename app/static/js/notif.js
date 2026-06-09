/* =====================================
   NOTIFICATIONS
===================================== */

document.addEventListener("DOMContentLoaded", () => {

    const boutonToutLu = document.getElementById("btnToutLu");
    const badgeNotifications = document.getElementById("badgeNotifications");
    const notifications = document.querySelectorAll(".carte-notification");

    // TOUT MARQUER COMME LU
    if (boutonToutLu) {
        boutonToutLu.addEventListener("click", () => {
            notifications.forEach(notification => {
                notification.classList.remove("non-lue");
            });
            if (badgeNotifications) {
                badgeNotifications.textContent = "0";
            }
        });
    }

    // UNE NOTIFICATION DEVIENT LUE AU CLIC
    notifications.forEach(notification => {
        notification.addEventListener("click", () => {
            if (notification.classList.contains("non-lue")) {
                notification.classList.remove("non-lue");
                if (badgeNotifications) {
                    let compteur = parseInt(badgeNotifications.textContent) || 0;
                    compteur = Math.max(0, compteur - 1);
                    badgeNotifications.textContent = compteur;
                }
            }
        });
    });

});
