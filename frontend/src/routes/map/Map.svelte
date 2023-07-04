<script lang="ts">
   import 'leaflet/dist/leaflet.css';
   import { Map, TileLayer, Marker, Popup } from 'svelte-map-leaflet';

    const mapOptions = {center:[-35.79348852145885, -71.78329391202294], zoom:4}
    const tileUrl = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
</script>

<div class="container">
    <h1>Mapa</h1>
    <div class="map">
        <Map options={mapOptions}>
            <TileLayer url={tileUrl}></TileLayer>
        </Map>
    </div>
</div>

<style>
    .map{
        height: 500px;
        width: 300px;
    }
</style>