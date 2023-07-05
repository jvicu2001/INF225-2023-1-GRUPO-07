<script lang="ts">
    export let data;
</script>

<nav class="container-fluid">
    <ul>
        <li>
            <a href="/">Datos Altimetricos de Chile</a>
        </li>
    </ul>
    <ul>
        {#if data.user}
            <li>
                <a href="/user">Subir Datos</a>
            </li>
        {/if}
        <li>
            <a href="/map">Mapa</a>
        </li>
        <li>
            {#if data.user}
                <form action="logout" method="POST">
                    <button type="submit" class="navbutton">Logout</button>
                </form>
            {:else}
                <a role="button" href="/login">Login</a>
            {/if}
        </li>
    </ul>
</nav>

<slot></slot>

<style>
    form{
        margin: 0% 0% 0% 0%;
    }
</style>