<script lang="ts">
    import { enhance, applyAction } from '$app/forms';
    import { goto } from '$app/navigation';
    import type { ActionData } from './$types';

    let { form }: { form: ActionData } = $props();
</script>

<div class="container p-3 mx-auto col-3">
    <div class="mb-3">
        <p class="text-center">Log in to continue</p>
    </div>
    <form
        method="POST"
        action="?/login"
        use:enhance={() => {
            return async ({ result }) => {
                if (result.type === 'redirect') {
                    goto(result.location);
                } else {
                    await applyAction(result);
                    
                }
            };
        }}
    >
        <div class="mb-3">
            <input type="text" class="form-control" id="login" name="login" 
            value={form?.login ?? ''}  placeholder="Username" autocomplete="username" required>
          </div>
        <div class="mb-3">
          <input type="password" class="form-control" id="password" name="password"
          value={form?.incorrect ? '' : undefined} placeholder="Password" autocomplete="current-password" required>
        </div>
            <button type="submit" class="btn btn-primary d-block mx-auto mb-3">LOG IN</button>
        {#if form?.incorrect}
            <p class="text-danger text-center">Invalid credentials!</p>
        {/if}
    </form>
</div>