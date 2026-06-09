/* ==================================================
   MESSAGERIE
================================================== */

document.addEventListener("DOMContentLoaded", () => {

    // ==================================================
    // ELEMENTS PRINCIPAUX
    // ==================================================

    const conversations = document.querySelectorAll(".conversation-item");

    const etatVide = document.querySelector(".etat-vide-discussion");

    const conversationActive = document.getElementById("conversationActive");

    const recherche = document.getElementById("rechercheConversation");

    const champMessage = document.getElementById("champMessage");

    const boutonEnvoyer = document.querySelector(".btn-envoyer");

    const historiqueMessages = document.getElementById("historiqueMessages");

    const boutonEmoji = document.querySelector(".btn-emoji");

    const menuEmojis = document.querySelector(".menu-emojis");

    const emojis = document.querySelectorAll(".menu-emojis span");

    const fichierMessage = document.getElementById("fichierMessage");


    // ==================================================
    // OUVERTURE D'UNE CONVERSATION
    // ==================================================

    conversations.forEach(conversation => {

        conversation.addEventListener("click", () => {

            // retire active partout
            conversations.forEach(item => {

                item.classList.remove("active");

            });

            // ajoute active
            conversation.classList.add("active");

            // cache l'état vide
            if(etatVide){

                etatVide.classList.add("d-none");

            }

            // affiche la discussion
            if(conversationActive){

                conversationActive.classList.remove("d-none");

            }

            // supprime badge non lu
            const badge = conversation.querySelector(".badge-non-lu");

            if(badge){

                badge.remove();

            }

        });

    });


    // ==================================================
    // RECHERCHE DE CONVERSATION
    // ==================================================

    if(recherche){

        recherche.addEventListener("keyup", () => {

            const valeur = recherche.value.toLowerCase();

            conversations.forEach(conversation => {

                const nom = conversation
                    .querySelector("h6")
                    .textContent
                    .toLowerCase();

                if(nom.includes(valeur)){

                    conversation.style.display = "flex";

                }

                else{

                    conversation.style.display = "none";

                }

            });

        });

    }


    // ==================================================
    // AFFICHAGE DU MENU EMOJI
    // ==================================================

    if(boutonEmoji){

        boutonEmoji.addEventListener("click", () => {

            menuEmojis.classList.toggle("d-none");

        });

    }


    // ==================================================
    // INSERTION D'UN EMOJI
    // ==================================================

    emojis.forEach(emoji => {

        emoji.addEventListener("click", () => {

            champMessage.value += emoji.textContent;

            menuEmojis.classList.add("d-none");

            champMessage.focus();

        });

    });


    // ==================================================
    // ENVOI D'UN MESSAGE
    // ==================================================

    function envoyerMessage(){

        const texte = champMessage.value.trim();

        if(texte === "") return;

        const heure = new Date();

        const heureActuelle =
            heure.getHours().toString().padStart(2,"0")
            + ":"
            +
            heure.getMinutes().toString().padStart(2,"0");


        // création du message
        const message = document.createElement("div");

        message.classList.add(
            "message",
            "message-envoye"
        );

        message.innerHTML = `
            <div class="contenu-message">
                ${texte}
            </div>

            <span class="heure-message">
                ${heureActuelle}
            </span>
        `;

        historiqueMessages.appendChild(message);

        // vide le champ
        champMessage.value = "";

        // scroll vers le bas
        historiqueMessages.scrollTop =
            historiqueMessages.scrollHeight;

    }


    // clic sur envoyer

    if(boutonEnvoyer){

        boutonEnvoyer.addEventListener(
            "click",
            envoyerMessage
        );

    }


    // touche Entrée

    if(champMessage){

        champMessage.addEventListener("keydown", (e) => {

            if(e.key === "Enter"){

                envoyerMessage();

            }

        });

    }


    // ==================================================
    // PIECES JOINTES
    // ==================================================

    if(fichierMessage){

        fichierMessage.addEventListener("change", () => {

            if(!fichierMessage.files.length) return;

            const nomFichier =
                fichierMessage.files[0].name;

            const heure = new Date();

            const heureActuelle =
                heure.getHours().toString().padStart(2,"0")
                + ":"
                +
                heure.getMinutes().toString().padStart(2,"0");

            const message = document.createElement("div");

            message.classList.add(
                "message",
                "message-envoye"
            );

            message.innerHTML = `
                <div class="contenu-message">

                    📎 ${nomFichier}

                </div>

                <span class="heure-message">

                    ${heureActuelle}

                </span>
            `;

            historiqueMessages.appendChild(message);

            historiqueMessages.scrollTop =
                historiqueMessages.scrollHeight;

        });

    }

});