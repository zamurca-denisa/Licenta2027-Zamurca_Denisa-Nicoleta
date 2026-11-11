const backendStatus = document.getElementById("backend-status");

fetch("http://127.0.0.1:8000/health")
    .then(response => response.json())
    .then(data => {
        backendStatus.textContent = data.status;
    })
    .catch(error => {
        console.error(error);

        backendStatus.textContent = "Backend indisponibil";
    });

const problemsList = document.getElementById("problems-list");

fetch("http://127.0.0.1:8000/problems")
    .then(response => response.json())
    .then(problems => {
        problems.forEach(problem => {
            const problemElement = document.createElement("div");

            problemElement.innerHTML = `
                <h3>${problem.title}</h3>
                <p>Difficulty: ${problem.difficulty}</p>
                <p>Topic: ${problem.topic}</p>
            `;

            problemsList.appendChild(problemElement);
        });
    })
    .catch(error => {
        console.error("Could not load problems:", error);
    });