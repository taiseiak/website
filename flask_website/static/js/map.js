/*
Javascript file for map
*/

$.getJSON("/_setup_map", function(data) {
    var map_info = data.result;
    var map = L.map('map')


    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox.streets',
        accessToken: map_info.mapbox
    }).addTo(map);

    map.locate({setView: true, maxZoom: 16});

    var userPos = map.getCenter();
    var userLat = userPos.lat;
    var userLng = userPos.lng;

    function onLocationError(e) {
        alert(e.message);
    }

    map.on('locationerror', onLocationError);

    /*$.getJSON("/_get_poi", {lat: userLat, lng: userLng},
        function(data) {
            console.log(data);
            data.forEach(function(place) {
                console.log(place.name);
                var marker = L.marker([place.geometry.location.lat, place.geometry.location.lng])
                    .bindPopup(place.name + "<br>" + place.vicinity)
                    .addTo(map);
            })
        })*/

    var popup = L.popup();

    function onMapClick(e) {
        var latlng = e.latlng
        $.getJSON("/_get_addy", {lat: userLat, lng: userLng},
            function(data) {
                var address = data.result;
                console.log("address json" + address.address);
                popup
                    .setLatLng(e.latlng)
                    .setContent(address.address)
                    .openOn(map);
            }
        )
    }

    map.on('click', onMapClick);
})

