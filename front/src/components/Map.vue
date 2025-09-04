<template>
  <div class="wrapper">
    <img v-show="isLoading" src="/loading.svg" class="loading-icon"/>
    <div ref="mapContainer" class="map-container"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import axios from 'axios';
const isLoading = ref(false);
const preloadDist  = 0.03
let lastRequest = {
    lat: 0. ,
    lng: 0. ,
}
const props = defineProps({
  lat: { type: Number, default: 48.84389 },
  lng: { type: Number, default: 2.35133 },
  zoom: { type: Number, default: 17 },
});

const mapContainer = ref(null);
let map = null;
let layerGroup = null;
const fetchAndUpdateSpots = async (north,east,south,west) => {
  console.log('Request ', {north,east,south,west});
  isLoading.value = true;
  try {
    const response = await axios.get('http://localhost:5000/spots/'+north+"/"+east+"/"+south+"/"+west);
    const spots = response.data.spots;

    spots.forEach(spot => { 
        const marker = L.marker([spot.lat, spot.lon])
        .addTo(layerGroup);
        marker.on('click', async () => {
            console.log('Clicked spot ID:', spot.id);
            const response = await axios.get('http://localhost:5000/detail/' + spot.id);
            const details = response.data.details;
            console.log(details);
        });
    });
    
  } catch (error) {
    console.error('Error fetching spots:', error);
  }
  isLoading.value = false;
}

onMounted(async () => {
  map = L.map(mapContainer.value).setView([props.lat, props.lng], props.zoom);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap',
  }).addTo(map);
  layerGroup = L.layerGroup().addTo(map);

  map.on('moveend', function() {
    console.log('Moove to', map.getCenter()," from ",lastRequest, " zoom ", map.getZoom());
    if(map.getZoom() >= 17){
      if(Math.abs(map.getCenter().lat - lastRequest.lat)>preloadDist || 
       Math.abs(map.getCenter().lng - lastRequest.lng)>preloadDist){
        lastRequest.lat = map.getCenter().lat
        lastRequest.lng = map.getCenter().lng
        fetchAndUpdateSpots( map.getBounds()._northEast.lat + preloadDist,
                             map.getBounds()._northEast.lng + preloadDist,
                             map.getBounds()._southWest.lat - preloadDist,
                             map.getBounds()._southWest.lng - preloadDist);

      }
    }

});
  
});

onUnmounted(() => {
  if (map) map.remove();
});

</script>

<style>
.wrapper{
  position: relative;
}
.map-container { 
  height: 100vh; 
  width: 100%;
  position: fixed;
}
.loading-icon {
  z-index: 1;
  position: absolute;
  image-rendering: smooth;
  height: 3.5em;
  margin-left: 3%;
  margin-top: 166%;
}
</style>
