<script lang='ts'> 
    import chile2 from '$lib/images/chile.png'
</script>

<!-- Main -->
<main class="container">
  <div class="grid">
    <section>
      <hgroup>
        <h2>Bienvenido a tu sesión </h2>
        <h3></h3>
      </hgroup>
      <p>
        Para actualizar o subir nuevos datos altimétricos de distintas partes de Chile, seleccione el tipo de archivo que desea subir 
      </p>  
        <!-- Select -->
      <form method="POST" enctype="multipart/form-data">
        <select id="select" name="dataType" required>
          <option value="" selected>Select…</option>
          <option value=0>DEM</option>
          <option value=1>DTM</option>
          <option value=2>DSM</option>
        </select>
        <p>
          A continuacion seleccione el archivo que subira 
        </p>
        <!-- File browser -->
        <label for="file"
          >Explorador de archivos
          <input type="file" id="file" name="file" accept="image/tiff" />
            <!-- Buttons -->
          <input type="submit" value="Subir" />
  
      
        </label>
      </form>
      
      
    </section>

    <aside>
        
        <img src={chile2}/>
        
    </aside>
  </div>
</main>

<style>
    img {
    max-width:100%;
    align-items:end;
    
    /* height: auto; */
    /* border-style: none; */
}
</style>
