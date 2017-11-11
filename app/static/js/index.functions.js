const choropleth = (category) => {

  const data = JSON.parse(sessionStorage.getItem(category))

  let min = Number.MAX_SAFE_INTEGER
  let max = -1

  // for (let point in data) {
  //
  //   if
  //
  // }

  window.map.data = {
    USA: {fillKey: 'bubbles'}
  }


}

const bubbles = (category) => {

  if (category == 'all') {

  } else {

    let data = JSON.parse(sessionStorage.getItem(category))

    let bubbles = []

    for (let dot in data) {

      let popup = '<p >'
      var track = []

      for (let i = 0; i < data[dot].articles.length; i++) {

        if (track.indexOf(data[dot].articles[i].title) == -1) {

          track.push(data[dot].articles[i].title)
          popup += data[dot].articles[i].title + '</p><p >'

        }
      }

      popup += '</p>'

      bubbles.push({
        name: dot,
        radius: Math.sqrt(data[dot].count * 16),
        latitude: data[dot].lat,
        longitude: data[dot].lng,
        fillKey: 'bubble',
        popup: popup
      })

    }

    window.map.bubbles(bubbles, {
      popupTemplate: (geo, data) => {
        return '<div class="hoverinfo" >' + data.popup + '</div>'
      },
      borderWidth: 0,
    })
  }
}

const update_map = () => {

  if (sessionStorage.getItem('map_view') === 'bubbles') {
    bubbles(sessionStorage.getItem('category'))
  } else if (sessionStorage.getItem('map_view') === 'choropleth') {
    choropleth(sessionStorage.getItem('category'))
  }

}

const consolidate = (articles) => {

  let countries = {}

  for (let i = 0; i < articles.countries.length; i++) {

    let article = articles.countries[i]

    if (article.country_name in countries) {

      countries[article.country_name].count++

      countries[article.country_name].articles.push({
        'title': article.title,
        'summary': article.summary,
        'web_url': article.web_url
      })

    } else {

      let country = {
        'count': 1,
        'articles': [
          {
            'title': article.title,
            'summary': article.summary,
            'web_url': article.web_url
          }
        ],
        'lat': article.country_lat,
        'lng': article.country_lng
      }

      countries[article.country_name] = country

    }

  }

  sessionStorage.setItem('countries', JSON.stringify(countries))

}

const fetch_articles = () => {
  $.ajax({
      method: 'get',
      url: 'http://localhost:8080/articles',
      data: {
          'start_date': $('#start_date').val(),
          'end_date': $('#end_date').val()
      },
      success: (data) => {
        consolidate(data.articles)
        update_map()
      }
  })
}
