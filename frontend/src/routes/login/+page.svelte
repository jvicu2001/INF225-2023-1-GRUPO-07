<script lang='ts'> 
    import chile2 from '$lib/images/chile2.png'
    </script> 
    
    
    <!DOCTYPE html>
    <html lang="en">
        <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Datos Altimetricos de Chile2</title>
        <meta name="description" content="A minimalist layout for Login pages. Built with Pico CSS." />
        <link rel="shortcut icon" href="https://picocss.com/favicon.ico" />
        <link rel="canonical" href="https://picocss.com/examples/sign-in/" />
    
        <!-- Pico.css -->
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css" />
    
        <!-- Custom styles for this example -->
        <link rel="stylesheet" href="custom.css" />
        </head>
    
        <body>
    
    
        <!-- Main -->
        <main class="container">
            <article class="grid">
            <div>
                <hgroup>
                <h1>Chile 3D</h1>
                <h2> Ingresa a tu cuenta para gestionar los datos altimetricos</h2>
                </hgroup>
                <form>
                <input
                    type="text"
                    name="login"
                    placeholder="Email"
                    aria-label="Login"
                    autocomplete="nickname"
                    required
                />
                <input
                    type="password"
                    name="password"
                    placeholder="contraseña"
                    aria-label="Password"
                    autocomplete="current-password"
                    required
                />
                <fieldset>
                    <label for="remember">
                    <input type="checkbox" role="switch" id="remember" name="remember" />
                    Recuerdame
                    </label>
                </fieldset>
                <button type="submit" class="contrast" onclick="event.preventDefault()">Ingresar</button>
                </form>
            </div>
            <div> 
                <img src={chile2}/>
            </div>
            </article>
        </main>
        <!-- ./ Main -->
        <!-- Minimal theme switcher -->
        <script src="js/minimal-theme-switcher.js"></script>
        </body>
    </html>
  