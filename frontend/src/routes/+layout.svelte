<script lang='ts'>
    import 'bootstrap/dist/css/bootstrap.min.css';
    import type { PageData } from './$types';

    let { data, children }: { data: PageData, children: any } = $props();

    import { onMount } from 'svelte';

    let previousLoginStatus = data.is_logged_in;

    onMount(() => {
        previousLoginStatus = data.is_logged_in;
    });

    $effect(() => {
        if (previousLoginStatus !== data.is_logged_in && !data.is_logged_in) {
            location.reload();
        }
        previousLoginStatus = data.is_logged_in;
    });
</script>

<nav class="navbar navbar-expand-sm bg-body-tertiary">
    <div class="container-fluid">
        <nav class="navbar bg-body-tertiary">
            <div class="container-fluid">
              <a class="navbar-brand mb-0 h1" href="/home">La Jout'A Diner</a>
            </div>
          </nav>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        {#if !data.is_logged_in}
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav mb-0 mb-lg-0">
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
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav mb-0 mb-lg-0 me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/home">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/profile">Profile</a>
                    </li>
                </ul>
                <form method="post" class="d-flex ms-auto">
                    <button class="btn btn-outline-danger" formaction="/?/logout" type="submit">Logout</button>
                </form>
            </div>

        {/if}
    </div>
</nav>

{@render children()}