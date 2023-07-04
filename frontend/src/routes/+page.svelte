<script lang="ts">
    import mapa from '$lib/images/mapa-chile.png'
    import ilustra from '$lib/images/ilu.png'
</script>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0"> <!-- displays site properly based on user's device -->
  <link rel="icon" type="image/png" sizes="32x32" href="../images/favicon-32x32.png">
  <title>Datos altimetricos de Chile</title>
  <link rel="stylesheet" href="../css/styles.css">
</head>
<body>

  
  <header class="hero">
    <div class="hero__wave"></div>

    <section class="hero__main container">
        <img src={mapa}/>

      <h1 class="hero__title">Aqui encontraras los dato altimetrico de Chile que necesites.</h1>
      <p class="hero__paragraph"> Nuestra plataforma te permite buscar y descargar datos altimetricos en formato  GeoTIFF.</p>
        <a href="#" class="hero__cta">  
         
        </a>
    </section>

  </header>

    <section class="productive container">

      <figure class="productive__picture">
        <img src={ilustra}/>
      </figure>

      <div class="productive__texts">

        <h3 class="productive__title"> Nuestros datos siempre estan actualizados</h3>

        <p class="productive__paragraph"> Los administradores actualizan los datos almimetricos cada vez que se obtienen nuevos archivos GeoTIFF.</p>

        <p class="productive__paragraph">Pero recuerda no todas las zonas de nuestro pais cuentan con datos altimetricos.</p>


      </div>
    </section>

</body>
</html>
<style>
    img {
    max-width: 30%;
    align-items:end;
    margin-left:30%;
    /* height: auto; */
    /* border-style: none; */
}
</style>