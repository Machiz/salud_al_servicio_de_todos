const slider = document.getElementById("search_value_range");
const outputLabel = document.getElementById("search_range_lbl");

// Establecemos el valor inicial al cargar la página
outputLabel.textContent = `Rango de centros de salud  en la zona: ${slider.value} km`;

// Función para actualizar el valor del rango
slider.addEventListener("input", function() {
    // Actualizamos el texto con el valor actual del rango
    outputLabel.textContent = `Rango de centros de salud  en la zona: ${slider.value} km`;
});
//para que el forms solo sea recibido al tener todos los datos
document.addEventListener('DOMContentLoaded', () => {
        
  // By default, submit button is disabled
  document.querySelector('#submit').disabled = true;

  // Enable button only if there is text in the input field
  document.querySelector('#csalud').onkeyup = () => {
      if (document.querySelector('#csalud').value.length > 0  && document.querySelector('#provincia').value !='none' && document.querySelector('#search_range_lbl').value !=0)
          document.querySelector('#submit').disabled = false;
      else
          document.querySelector('#submit').disabled = true;
          document.querySelector('#submit').style.backgroundColor = '#f12323';
  };

  document.querySelector('form').onsubmit = () => {

      // Create new item for list
      const li = document.createElement('li');
      li.innerHTML = document.querySelector('#csalud').value;

      // Clear input field and disable button again
      document.querySelector('#csalud').value = '';
      document.querySelector('#provincia').value = 'none';
      out
      document.querySelector('#search_range_lbl').value = 50 ;
      document.querySelector('#submit').disabled = true;

      // Stop form from submitting
      return false;
  };

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