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
