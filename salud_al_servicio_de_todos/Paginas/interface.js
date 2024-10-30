const slider = document.getElementById("search_value_range");
const outputLabel = document.getElementById("search_range_lbl");

// Establecemos el valor inicial al cargar la página
outputLabel.textContent = `Rango de centros de salud  en la zona: ${slider.value} km`;

// Función para actualizar el valor del rango
slider.addEventListener("input", function() {
    // Actualizamos el texto con el valor actual del rango
    outputLabel.textContent = `Rango de centros de salud  en la zona: ${slider.value} km`;
});
