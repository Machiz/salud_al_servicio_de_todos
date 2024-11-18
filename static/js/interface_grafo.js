
document.addEventListener('DOMContentLoaded', () => {
    inputFrame.onkeyup = reloadFrame;
    function reloadFrame(){
        document.getElementById('mapa').src = document.getElementById('mapa').src;
    }
});