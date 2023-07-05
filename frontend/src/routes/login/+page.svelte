<script lang='ts'>
    import chile2 from '$lib/images/chile2.png'

    export let form;
</script> 

<main class="container">
    <article class="grid">
    <div>
        <hgroup>
        <h1>Chile 3D</h1>
        <h2> Ingresa a tu cuenta para gestionar los datos altimetricos</h2>
        </hgroup>
        <form action="login" method="POST">
            <input
                type="text"
                name="username"
                placeholder="Usuario"
                aria-label="Username"
                autocomplete="nickname"
                required
            />
            <input
                type="password"
                name="password"
                placeholder="Contraseña"
                aria-label="Password"
                autocomplete="current-password"
                required
            />
        <!--<fieldset>
            <label for="remember">
            <input type="checkbox" role="switch" id="remember" name="remember" />
            Mantener iniciada sesión
            </label>
        </fieldset>-->
        <button type="submit" class="contrast">Ingresar</button>
        </form>
    </div>
    <div> 
        <img src={chile2}/>
    </div>
    </article>
</main>

  