function search() {
    var query = document.getElementById('searchInput').value;

    $.ajax({
        type: 'GET',
        url: '/bandsnap/search-request/',
        data: {query:query},
        success: function(response){
            var searchResultsElement = document.getElementById('searchResults');
            searchResultsElement.innerHTML = response.results;
        },
        error: function(xhr, status, error) {
            console.error('AJAX Error:', status, error);
        }
    });
}