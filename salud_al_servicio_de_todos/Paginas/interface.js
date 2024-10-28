const input_range = document.querySelector("#search_value_range");
const lbl_size = document.querySelector("#search_range_lbl");
//const lbl_size_conexion_ramge = document.querySelector("#value_conexion");
//const matrix_form = document.querySelector("#matrix_form");
//const btn_random = document.querySelector("#btn_random_matrix");
//const conexion_range = document.querySelector("#range_conexion");
function updateMatrix() {
    //const size = getSizeMatrix();
    lbl_size.innerText = `rango de busqueda: ${size} km`;
    updateConexionRange();
    //generateMatrix(size);
    //getMatrix(size);
}
function getConexionRange() {
    return parseInt(conexion_range.value);
}
  
  // función para obtener la celda de la matriz
  function updateConexionRange() {
    const value = getConexionRange();
    lbl_size_conexion_ramge.innerText = `Conexion: ${value}%`;
  }
  function getSizeMatrix() {
    return parseInt(input_range.value);
  }