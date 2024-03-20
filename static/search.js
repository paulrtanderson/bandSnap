document.addEventListener('DOMContentLoaded', function() {
    search(); // Call the search function when the DOM content is loaded
});

function search() {
    var query = document.getElementById("searchInput").value;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function (){
        if (this.readyState == 4) {
            if (this.status = 200) {
                var fullData = JSON.parse(this.responseText);
                for (var key in fullData) {
                    data = fullData[key]
                    var results = document.getElementById("searchResults"+key);
                    results.innerHTML = "";
                    
                    for (var i = 0; i < data.length; i++) {
                        results.innerHTML += data[i];
                    }
                }

            } else {
                console.error('Error fetching data. Status code:', this.status);
            }
        }
    };
    xhttp.open("GET", "/bandsnap/artist-search/?query=" + query, true);
    xhttp.send();
}