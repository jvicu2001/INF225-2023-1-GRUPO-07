<script lang="ts">
    import mapa from '$lib/images/mapa-chile.png'
    import ilustra from '$lib/images/ilu.png'
</script>

<header class="hero">
  <div class="hero__wave"></div>

  <section class="hero__main container">
      <img src={mapa}/>

    <h1 class="hero__title">Aquí encontrarás los datos altimétricos de Chile que necesites.</h1>
    <p class="hero__paragraph"> Nuestra plataforma te permite buscar y descargar datos altimétricos en formato GeoTIFF.</p>
      <a href="#" class="hero__cta">  
        
      </a>
  </section>

</header>

  <section class="productive container">

    <figure class="productive__picture">
      <img src={ilustra}/>
    </figure>

    <div class="productive__texts">

      <h3 class="productive__title"> Nuestros datos siempre están actualizados</h3>

      <p class="productive__paragraph"> Los administradores actualizan los datos altimétricos cada vez que se obtienen nuevos archivos GeoTIFF.</p>

      <p class="productive__paragraph">Pero recuerda, no todas las zonas de nuestro país cuentan con datos altimétricos.</p>

    </div>
  </section>

<style>
    img {
    max-width: 30%;
    align-items:end;
    margin-left:30%;
    /* height: auto; */
    /* border-style: none; */
}
</style>