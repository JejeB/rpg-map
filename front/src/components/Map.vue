<template>
  <div class="wrapper relative">
    <div class="map-container z-0 top-0 left-0" ref="mapContainer" ></div>
    <div class="spot absolute inset-0 flex items-center justify-center z-1" v-show="showSpotDetail">
      <Spot @close="showSpotDetail = false" :details="spotDetails"></Spot>
    </div>
    <img class="loading-icon absolute bottom-0 left-0 z-1" v-show="isLoading" src="/loading.svg" />
  </div>
</template>

<script setup>
import Spot from './Spot.vue'
import { ref, onMounted, onUnmounted, watch } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import axios from 'axios';
const isLoading = ref(false);

const showSpotDetail = ref(false)
const spotDetails = ref()


const preloadDist  = 0.03
const zoomDisplay  = 16
let lastRequest = {
    lat: 0. ,
    lng: 0. ,
}
const props = defineProps({
  lat: { type: Number, default: 48.84389 },
  lng: { type: Number, default: 2.35133 },
  zoom: { type: Number, default: zoomDisplay },
});

const mapContainer = ref(null);
let map = null;
let layerGroup = null;
const fetchAndUpdateSpots = async (north,east,south,west) => {
  console.log('Request ', {north,east,south,west});
  isLoading.value = true;
  try {
    const response = await axios.get('http://localhost:5000/spots/'+north+"/"+east+"/"+south+"/"+west, {
       withCredentials: true});
    const spots = response.data.spots;

    spots.forEach(spot => {
      var unkwonIcon = L.icon({
        iconUrl: 'question.svg',
        iconSize:     [50, 50],
      });
      var discoverIcon = L.icon({
        iconUrl: 'discovered.svg',
        iconSize:     [50, 50],
      }); 
        const marker = L.marker([spot.lat, spot.lon], {icon: spot.discovered ?  discoverIcon : unkwonIcon})
        .addTo(layerGroup);
        marker.on('click', async () => {
            marker.setIcon(discoverIcon)
            spotDetails.value = "..."
            showSpotDetail.value = true
            const response = await axios.get('http://localhost:5000/detail/' + spot.id, {
              withCredentials: true});
            spotDetails.value = response.data.details;
            console.log(response.data.details);
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
    if(map.getZoom() >= zoomDisplay){
      map.addLayer(layerGroup);
      if(Math.abs(map.getCenter().lat - lastRequest.lat)>preloadDist || 
       Math.abs(map.getCenter().lng - lastRequest.lng)>preloadDist){
        lastRequest.lat = map.getCenter().lat
        lastRequest.lng = map.getCenter().lng
        fetchAndUpdateSpots( map.getBounds()._northEast.lat + preloadDist,
                             map.getBounds()._northEast.lng + preloadDist,
                             map.getBounds()._southWest.lat - preloadDist,
                             map.getBounds()._southWest.lng - preloadDist);

      }
    }else{
      map.removeLayer(layerGroup);
    }

});
  
});

onUnmounted(() => {
  if (map) map.remove();
});

</script>

<style>
.map-container { 
  height: 100vh; 
  width: 100%;
}
.loading-icon {
  z-index: 1;
  position: absolute;
  height: 2em;
}
/* .wrapper{
  position: relative;
  height: 100vh; 
  width: 100%;
}

.spot{
  z-index: 1;
  position: absolute;
} */
</style>
