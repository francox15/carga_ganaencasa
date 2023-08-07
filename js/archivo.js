document.getElementById("contactForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Evitar que el formulario se envíe normalmente.

    const formData = new FormData(event.target); // Obtener los datos del formulario.
    
    fetch("/submit", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));

    fetch("/otro", {
        method: "GET",
        body: formData
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));
});