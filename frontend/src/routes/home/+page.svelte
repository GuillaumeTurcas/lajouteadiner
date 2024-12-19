<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
	console.log(data);
	const upcoming = data.event?.upcoming;

	function formatDate(dateStr: string): string {
		const date = new Date(dateStr);

		const day = String(date.getDate()).padStart(2, '0');
		const month = String(date.getMonth() + 1).padStart(2, '0');
		const year = date.getFullYear();
		const hours = String(date.getHours()).padStart(2, '0');
		const minutes = String(date.getMinutes()).padStart(2, '0');

		return `${day}/${month}/${year} à ${hours}h${minutes}`;
	}
</script>

<div class="container-fluid p-3 mx-auto col-4">
	<h2 class="text-center mb-4">Upcoming Events</h2>
	<div class="row g-3">
		{#each upcoming as event}
			<div class="col-12">
				<div class="card shadow-sm text-center">
					<div class="card-body">
						<h5 class="card-title">{event.event}</h5>
						<p class="card-text mb-1">
							<strong>Date:</strong> {formatDate(event.date)}
						</p>
						<p class="card-text">
							<strong>Place:</strong> {event.place}
						</p>
					</div>
				</div>
			</div>
		{/each}
	</div>
	<h2 class="text-center mt-4">Past Events</h2>
	<div class="row g-3">
		{#each data.event?.past as event}
			<div class="col-12">
				<div class="card shadow-sm text-center">
					<div class="card-body">
						<h5 class="card-title">{event.event}</h5>
						<p class="card-text mb-1">
							<strong>Date:</strong> {formatDate(event.date)}
						</p>
						<p class="card-text">
							<strong>Place:</strong> {event.place}
						</p>
					</div>
				</div>
			</div>
		{/each}
	</div>
</div>