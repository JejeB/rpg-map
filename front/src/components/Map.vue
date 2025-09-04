<template>
  <div ref="mapContainer" class="map-container"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import axios from 'axios';
const preloadDist  = 0.03
let lastRequest = {
    lat: 48.84389 ,
    lng: 2.35133 ,
}
const props = defineProps({
  lat: { type: Number, default: 48.84389 },
  lng: { type: Number, default: 2.35133 },
  zoom: { type: Number, default: 17 },
});

const mapContainer = ref(null);
let map = null;

onMounted(async () => {
  map = L.map(mapContainer.value).setView([props.lat, props.lng], props.zoom);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 17,
	minZoom: 17,
    attribution: '&copy; OpenStreetMap',
  }).addTo(map);
  map.on('moveend', function() {
    console.log('Moove to', map.getCenter()," from ",lastRequest);
    if(Math.abs(map.getCenter().lat - lastRequest.lat)>preloadDist || Math.abs(map.getCenter().lng - lastRequest.lng)>preloadDist){
        lastRequest.lat = map.getCenter().lat
        lastRequest.lng = map.getCenter().lng
        console.log('New request', map.getBounds());

    }
});
  try {
    const response = await axios.get('http://localhost:5000/spots');
    const spots = response.data.spots;

    spots.forEach(spot => { 
        const marker = L.marker([spot.lat, spot.lon])
        .addTo(map);
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
});

onUnmounted(() => {
  if (map) map.remove();
});

</script>

<style>
.map-container { height: 100vh; width: 100%; }
</style>
