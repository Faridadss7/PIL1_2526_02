document.addEventListener("DOMContentLoaded", () => {

    const typeSession = document.getElementById("typeSession");

    const champLien = document.getElementById("champLien");

    const champLieu = document.getElementById("champLieu");

    if(typeSession){

        typeSession.addEventListener("change", () => {

            if(typeSession.value === "presentiel"){

                champLien.classList.add("d-none");

                champLieu.classList.remove("d-none");

            }

            else{

                champLieu.classList.add("d-none");

                champLien.classList.remove("d-none");

            }

        });

    }

});