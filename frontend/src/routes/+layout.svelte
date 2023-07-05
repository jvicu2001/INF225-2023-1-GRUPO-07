<script lang="ts">
    export let user;
</script>

<nav class="container-fluid">
    <ul>
        <li>
            <a href="/">Datos Altimetricos de Chile</a>
        </li>
    </ul>
    <ul>
        <li>
            <a href="/user">sesion</a>
        </li>
        <li>
            <a href="/map">Mapa</a>
        </li>
        <li>
            {#if $user}
                <a href="/logout">Logout</a>
            {/if}
            {#if !$user}
                <a href="/login">Login</a>
            {/if}
        </li>
    </ul>
</nav>

<slot></slot>