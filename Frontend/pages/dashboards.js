
document.addEventListener("DOMContentLoaded", () => {

    const counters = document.querySelectorAll(".counter");

    counters.forEach(counter => {

        const target = parseInt(
            counter.dataset.target
        );

        let current = 0;

        const increment = Math.max(
            1,
            Math.ceil(target / 60)
        );

        const updateCounter = () => {

            current += increment;

            if(current < target){

                counter.textContent = current;

                requestAnimationFrame(updateCounter);

            }

            else{

                counter.textContent = target;

            }

        };

        updateCounter();

    });

});

const progressBar =
    document.getElementById("progressBar");

const progressText =
    document.getElementById("progressText");

const targetProgress = 75;

let progress = 0;

const animateProgress = () => {

    if(progress <= targetProgress){

        progressBar.style.width =
            progress + "%";

        progressText.textContent =
            progress + "%";

        progress++;

            setTimeout(
                animateProgress,
                20
            );
    }

};

animateProgress();