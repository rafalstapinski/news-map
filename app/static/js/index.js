const fetch_articles = () => {
  $.ajax({
      method: 'get',
      url: 'http://localhost:8080/articles',
      data: {
          'start_date': $('#start_date').val(),
          'end_date': $('#end_date').val()
      },
      success: (data) => {
        console.log(data)
      }
  });
}


$(document).ready(() => {

  const dmap = new Datamap({
      element: document.getElementById('map')
  })

  const start_date = new Pikaday({
      field: document.getElementById('start_date'),
      format: 'YYYY/MM/DD',
      toString(date, format) {
          const day = ("0" + date.getDate()).slice(-2)
          const month = ("0" + (date.getMonth() + 1)).slice(-2)
          const year = date.getFullYear();
          return `${year}/${month}/${day}`
      },
  })

  const end_date = new Pikaday({
      field: document.getElementById('end_date'),
      format: 'YYYY/MM/DD',
      toString(date, format) {
          const day = ("0" + date.getDate()).slice(-2)
          const month = ("0" + (date.getMonth() + 1)).slice(-2)
          const year = date.getFullYear()
          return `${year}/${month}/${day}`
      }
  })

  const today = new Date()
  const day = ("0" + today.getDate()).slice(-2)
  const month = ("0" + (today.getMonth() + 1)).slice(-2)
  const year = today.getFullYear()
  $('.datepicker').val(year + '/' + month + '/' + day)

  fetch_articles()

})

$('#fetch_articles').click(() => {
  fetch_articles()
})
