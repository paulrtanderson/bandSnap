    // $(document).ready(function() {
    //     search(); // Call the search function when the page is first loaded
    // });
    document.addEventListener('DOMContentLoaded', function() {
        search(); // Call the search function when the DOM content is loaded
    });

    function search() {
        
        // var query = $('#searchInput').val();
        
        // $.ajax({
        //     url: '/bandsnap/artist-search/',
        //     data: {
        //         'query': query
        //     },
        //     dataType: 'json',
        //     success: function(data) {
        //         $('#searchResults').empty();
        //         for (var i = 0; i < data.length; i++) {
        //             $('#searchResults').append(data[i]);
        //         }
        //     }
        // });

        var query = document.getElementById("searchInput").value;
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function (){
            if (this.readyState == 4 && this.status == 200) {
                var results = document.getElementById("searchResults");
                results.innerHTML = "";
                var data = JSON.parse(this.responseText);
                for (var i = 0; i < data.length; i++) {
                    results.innerHTML += data[i];
                }
            }
        };
        xhttp.open("GET", "/bandsnap/artist-search/?query=" + query, true);
        xhttp.send();
        
    }