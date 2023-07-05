<script lang='ts'> 
    import chile2 from '$lib/images/chile.png'
</script>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Datos Altimetricos de Chile</title>
    <meta
      name="description"
      content="A classic company or blog layout with a sidebar. Built with Pico CSS."
    />
    <link rel="shortcut icon" href="https://picocss.com/favicon.ico" />
    <link rel="canonical" href="https://picocss.com/examples/company/" />

    <!-- Pico.css -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css" />

    <!-- Custom styles for this example -->
    <link rel="stylesheet" href="custom.css" />
  </head>

  <body>
  

    <!-- Main -->
    <main class="container">
      <div class="grid">
        <section>
          <hgroup>
            <h2>Bienvenido a tu sesión </h2>
            <h3></h3>
          </hgroup>
          <p>
            Para actualizar o subir nuevos datos altimetricos de distintas partes de Chile seleccione el tipo de archivo que desea subir 
          </p>
              <!-- Select -->
            
              <select id="select" name="Seleccionar" required>
                <option value="" selected>Select…</option>
                <option>DEM</option>
                <option>DTM</option>
                <option>DSM</option>
              </select>
              <p>
                A continuacion seleccione el archivo que subira 
              </p>
          <!-- File browser -->
          <label for="file"
            >Explorador de archivos
            <input type="file" id="file" name="file" />
             <!-- Buttons -->
            <input type="submit" value="Subir" onclick="event.preventDefault()" />
       
            
          </label>
         
          
        </section>

        <aside>
            
            <img src={chile2}/>
           
        </aside>
      </div>
    </main>
  </body>
</html>

<style>
    img {
    max-width:100%;
    align-items:end;
    
    /* height: auto; */
    /* border-style: none; */
}
</style>
