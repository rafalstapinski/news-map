var dmap = new Datamap({
    element: document.getElementById('map')
})


$.ajax({
    method: 'get',
    url: 'http://localhost:8080/locations',
    data: {
        'start_date': '2017/10/01',
        'end_date': '2017/10/10'
    },
    success: function(data) {
        dmap.bubbles(data.locations, {
          popupTemplate: function(geo, data) {
            return ''
          }
        });
    }
});
