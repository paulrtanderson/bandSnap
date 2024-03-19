function search() {
    var query = $('#searchInput').val();
    $.ajax({
        url: '/bandsnap/artist-search/',
        data: {
            'query': query
        },
        dataType: 'json',
        success: function(data) {
            $('#searchResults').empty();
            for (var i = 0; i < data.length; i++) {
                $('#searchResults').append(data[i]);
            }
        }
    });
}