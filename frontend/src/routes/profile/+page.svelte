<script lang="ts">
    import type { PageData, ActionData } from './$types';
    let { data, form }: { data: PageData, form : ActionData} = $props();
    const user = data.event?.user;

    let password1 = $state('');
    let password2 = $state('');
    let passwordMatch = $derived(password1 == password2 && password1.length > 0 && password2.length > 0);

</script>

<div class="container-fluid p-3 mx-auto col-sm-4">
    <div class="row g-3">
        <div class="col-12">
            <div class="card shadow-sm text-center">
                <div class="card-body">
                    <h2 class="text-center">Profile</h2>
                    <h5 class="card-title">{user.name} {user.surname}</h5>
                    <p class="card-text mb-0">Identifier: {user.login}</p>
                    <p class="card-text">Admin Status: Niveau {user.admin}</p>
                </div>
            </div>
        </div>
    </div>
    <div class="row g-3 mt-4">
        <div class="col-12">
            <div class="card shadow-sm text-center">
                <div class="card-body">
                <h2 class="text-center">Change Your Password</h2>
                    <form method="post" action="?/changepassword">
                        <div class="mb-3">
                            <input type="password" class="form-control" id="oldpassword" name="oldpassword" 
                            placeholder="Current password" autocomplete="current-password" required>
                        </div>
                        <div class="mb-3">
                            <input type="password" class="form-control" id="password1" name="password1" bind:value={password1}
                            placeholder="New password" autocomplete="new-password"
                            class:is-valid={passwordMatch} class:is-invalid={!passwordMatch} required>
                        </div>
                        <div class="mb-3">
                            <input type="password" class="form-control" id="password2" name="password2" bind:value={password2}
                            placeholder="Confirm your new password" autocomplete="new-password" 
                            class:is-valid={passwordMatch} class:is-invalid={!passwordMatch} required>
                        </div>
                        <button type="submit" class="btn btn-primary d-block mx-auto mb-3" disabled={!passwordMatch}>CHANGE PASSWORD</button>
                    </form>
                    {#if form?.message}
                        <p class="text-center text-danger">{form.message}</p>
                    {/if}
                </div>
            </div>
        </div>
    </div>
</div>