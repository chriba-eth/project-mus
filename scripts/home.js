function clickLike() {
  
  $.post('/results', {'artist': 'Katy Perry', 'region': 'Latin America'}, function(response) {
    // Update the number in the "like" element.

    $('#playlist').html(response);
  });
}

$('.submit').click(clickLike);
