const slider = document.getElementById("search_value_range");
const outputLabel = document.getElementById("search_range_lbl");

// Establecemos el valor inicial al cargar la página
outputLabel.textContent = `Rango de centros de salud en la zona: ${slider.value} km`;

// Función para actualizar el valor del rango
slider.addEventListener("input", function() {
    // Actualizamos el texto con el valor actual del rango
    outputLabel.textContent = `Rango de centros de salud en la zona: ${slider.value} km`;
});

//para que el forms solo sea recibido al tener todos los datos
document.addEventListener('DOMContentLoaded', () => {

    // By default, submit button is disabled
    document.querySelector('#submit').disabled = true;

    // Select the individual input elements
    const inputCsalud = document.querySelector('#csalud');
    const inputProvincia = document.querySelector('#provincia');
    const inputNivel = document.querySelector('#nivel');
    const inputCsaludF = document.querySelector('#csaludf');

    // Add event listener for 'keyup' on each input field
    inputCsalud.onkeyup = checkFormValidity;
    inputProvincia.onchange = checkFormValidity;
    inputNivel.onchange = checkFormValidity;
    inputCsaludF.onkeyup = checkFormValidity;

    // Function to check the form validity
    function checkFormValidity() {
        if (
            (inputCsalud.value.length > 0 && inputCsaludF.value.length > 0) ||
            (inputNivel.value !== 'none') ||
            (inputProvincia.value !== 'none')
        ) {
            document.querySelector('#submit').disabled = false;
            document.querySelector('#submit').style.backgroundColor = '#f12323';
        } else {
            document.querySelector('#submit').disabled = true;
        }
    }
});




//maps api (probably moved to another file)
// let map;

// async function initMap() {
//   const { Map } = await google.maps.importLibrary("maps");

//   map = new Map(document.getElementById("map"), {
//     center: { lat: -34.397, lng: 150.644 },
//     zoom: 8,
//   });
// }

// initMap();