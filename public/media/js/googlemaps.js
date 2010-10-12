var map = null;
var geocoder = null;

geocoder = new GClientGeocoder();

function addressPopup(address, map, point) {
    var marker = new GMarker(point);
    map.addOverlay(marker);
    //marker.openInfoWindowHtml(address);
}

function mapInit(element, address, point, zoomlevel) {
    if(zoomlevel==undefined) {
        zoomlevel = 15;
    }
    if (GBrowserIsCompatible()) {
        map = new GMap2(document.getElementById(element));
        //map.setCenter(new GLatLng(37.4419, -122.1419), 13);
        geocoder = new GClientGeocoder();

        if(point!==undefined&&point!='') {
        } else {
            //assume we've got a text address to lookup
            if (geocoder) {
            geocoder.getLatLng(
                address,
                function(point) {
                    if (!point) {
                        //alert(address + " not found");
                    } else {
                        map.setCenter(point, zoomlevel);
                        addressPopup(address, map, point);
                    }
                });
            }
        }
    } else {
        alert('Your browser does not support Google Maps');
    }
}


function addMarker(element, address) {
    map = new GMap2(document.getElementById(element));
    geocoder.getLatLng(
    address,
    function(point) {
        addressPopup(address, map, point);
        map.setCenter(point, 11);
    });
}
