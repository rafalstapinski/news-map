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


$(document).ready(() => {

  // sessionStorage.setItem('map_view', 'bubbles')
  sessionStorage.setItem('map_view', 'choropleth')
  sessionStorage.setItem('category', 'countries')

  window.map = new Datamap({
      element: document.getElementById('map'),
      fills: {
        defaultFill: '#cedac3',
        bubble: '#e3b4ad',
        a: 'rgba(81, 85, 76, 0)',
        b: 'rgba(81, 85, 76, .1)',
        c: 'rgba(81, 85, 76, .2)',
        d: 'rgba(81, 85, 76, .3)',
        e: 'rgba(81, 85, 76, .4)',
        f: 'rgba(81, 85, 76, .5)',
        g: 'rgba(81, 85, 76, .6)',
        h: 'rgba(81, 85, 76, .7)',
        i: 'rgba(81, 85, 76, .8)',
        j: 'rgba(81, 85, 76, .9)',
        k: 'rgba(81, 85, 76, 1)',
      },
      resize: true,
      geographyConfig: {
        popupOnHover: false,
        borderWidth: 0,
      }
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
