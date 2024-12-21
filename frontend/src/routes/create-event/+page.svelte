<script lang="ts">
    import type { ActionData } from './$types';
    let { form }: { form : ActionData} = $props();
</script>

<div class="container-fluid p-3 mx-auto col-sm-4">
	<div class="row g-3">
        <div class="col-12">
            <div class="card shadow-sm text-center">
                <div class="card-body">
                	<h2 class="text-center">Create Your Event !</h2>
                    <form method="POST" action="?/createevent">
                        <div class="mb-3">
                            <input type="text" class="form-control" id="event" name="event" 
                            placeholder="Name" autocomplete="off" required>
                        </div>
                        <div class="mb-3">
                            <input type="text" class="form-control" id="place" name="place"
                            placeholder="Place" autocomplete="off" required>
                        </div>
                        <div class="mb-3 text-start">
                            <label for="datedate" class="form-label">Date</label>
                            <div class="d-flex">
                                <input id="datedate" name="datedate" class="form-control me-2" type="date" />
                                <input id="datetime" name="datetime" class="form-control" type="time" value="00:00" />
                            </div>
                        </div>
                        <div class="mb-3 text-start">
                            <label for="deadlinedate" class="form-label">Deadline</label>
                            <div class="d-flex">
                                <input id="deadlinedate" name="deadlinedate" class="form-control me-2" type="date" />
                                <input id="deadlinetime" name="deadlinetime" class="form-control" type="time" value="00:00" />
                            </div>
                        </div>
                        <button type="submit" class="btn btn-primary d-block mx-auto mb-3">CREATE EVENT</button>
                    </form>
                    {#if form?.message}
                        <p class="text-center text-danger">{form.message}</p>
                    {/if}
                </div>
            </div>
        </div>
    </div>
</div>