<script lang="ts">
    interface Metadata {
    _id: string;
    fileData: {
        count: number;
        crs: string;
        dtype: string;
        driver: string;
        bounds: [number, number, number, number];
        lnglat: [number, number];
        height: number;
        width: number;
        shape: [number, number];
        res: [number, number];
        nodata: number;
    };
    user: string;
    fileName: string;
    fileDataType: number;
    fileId: string;
}
    import 'leaflet/dist/leaflet.css';
    import { Map, TileLayer, Marker, Popup } from 'svelte-map-leaflet';
 
    const mapOptions = {center:[-35.79348852145885, -71.78329391202294], zoom:4}
    const tileUrl = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";

    export let metadata: Metadata[];
</script>
 
 <div class="container">
    <h1>Mapa</h1>
    <div class="grid">
        <div class="map">
            <Map options={mapOptions}>
                <TileLayer url={tileUrl}></TileLayer>
                {#each metadata as item}
                    <Marker position={item.fileData.lnglat}>
                        <Popup>
                            <p>{item.fileName}</p>
                        </Popup>
                    </Marker>
                {/each}
            </Map>
        </div>
        <div>
            <!--Tabla de datos con búsqueda por nombre-->
                <table>
                    <thead>
                        <tr>
                            <th>Nombre archivo</th>
                            <th>Modelo</th>
                            <th>Subido por</th>
                            <th>Descargar</th>
                        </tr>
                    </thead>
                    <tbody>
                        {#each metadata as item}
                            <tr>
                                <td>{item.fileName}</td>
                                <td>{["DEM", "DTM", "DSM"][item.fileDataType]}</td>
                                <td>{item.user}</td>
                                <td>
                                    <button>Descargar</button>
                                </td>
                            </tr>
                        {/each}
                    </tbody>
                </table>
        </div>
    </div>

</div>
 
<style>
    .map{
        height: 100%;
        width: 100%;
        min-height: 500px;
    }
    
</style>