<script lang='ts'>
    import 'bootstrap/dist/css/bootstrap.min.css';
    export let data;
</script>

<nav class="navbar navbar-expand-sm bg-body-tertiary">
    <div class="container-fluid">
        <nav class="navbar bg-body-tertiary">
            <div class="container-fluid">
              <span class="navbar-brand mb-0 h1">La Jout'A Diner</span>
            </div>
          </nav>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        {#if !data.is_logged_in}
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link" href="/login">Login</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/sign-up">Sign Up</a>
                    </li>
                </ul>
            </div>
        {/if}
        {#if data.is_logged_in}
            <form method="post" class="d-flex">
                <button class="btn btn-outline-danger" formaction="/?/logout" type="submit">Logout</button>
            </form>
        {/if}
    </div>
</nav>
<slot />