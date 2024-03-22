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
function setBandUsername(bandusername){
    var bandUsernameInput = document.getElementById('bandUsernameInput');
        bandUsernameInput.value = bandusername;
}

/*

function swapSearchHeadings(element) {
    var x = document.getElementById(element);
    if (x === artist)
    {
        x.style.display = "block";
        band.style.display = "none";
        gig.style.display= "none";
    }
    else if (x === band)
    {
        x.style.display = "block";
        artist.style.display = "none";
        gig.style.display= "none";
    }
    else if (x === gig)
    {
        x.style.display = "block";
        artist.style.display = "none";
        band.style.display= "none";
    }
}

function removeArtist(artist)
{
  1. Receive artist object 
  2. Access relevant object and it's artist list
  3. Remove artist
}

function chooseUserType()
{
  1. Receive type based on what div element user clicks (either band or artist)
  2. Access created object and assign type
}




*/