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