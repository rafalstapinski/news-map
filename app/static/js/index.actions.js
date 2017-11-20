$('#fetch_articles').click(() => {
  fetch_articles()
})

$('#map_view_select').change(() => {

  sessionStorage.setItem('map_view', $('#map_view_select').val())

})
