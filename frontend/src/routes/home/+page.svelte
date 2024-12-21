<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
	const upcoming = data.event?.upcoming;
	const users = data.event?.users;

	function formatDate(dateStr: string): string {
		const date = new Date(dateStr);

		const day = String(date.getDate()).padStart(2, '0');
		const month = String(date.getMonth() + 1).padStart(2, '0');
		const year = date.getFullYear();
		const hours = String(date.getHours()).padStart(2, '0');
		const minutes = String(date.getMinutes()).padStart(2, '0');

		return `${day}/${month}/${year} à ${hours}h${minutes}`;
	}

	function capitalizeFirstLetter(str: string) {
		return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
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
						<p class="card-text mb-0">
							<strong>Date:</strong> {formatDate(event.date)}
						</p>
						<p class="card-text mb-0">
							<strong>Place:</strong> {event.place}
						</p>
						<p class="card-text mb-0">
							<strong>Organizer:</strong> {users[event.organizer].name} {users[event.organizer].surname}
						</p>
						<p class="card-text mb-0">
							<strong>Guest{#if event.guest.length > 1}s{/if}:</strong>
							{#each event.guest as user}
								<span class="badge bg-primary me-1">{capitalizeFirstLetter(users[user.user].name)} {capitalizeFirstLetter(users[user.user].surname)}</span>
							{/each}
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
						<p class="card-text mb-0">
							<strong>Date:</strong> {formatDate(event.date)}
						</p>
						<p class="card-text mb-0">
							<strong>Place:</strong> {event.place}
						</p>
						<p class="card-text mb-0">
							<strong>Organizer:</strong> {users[event.organizer].name} {users[event.organizer].surname}
						</p>
						<p class="card-text">
							<strong>Guest{#if event.guest.length > 1}s{/if}:</strong>
							{#each event.guest as user}
								<span class="badge bg-primary me-1">{capitalizeFirstLetter(users[user.user].name)} {capitalizeFirstLetter(users[user.user].surname)}</span>
							{/each}
						</p>

					</div>
				</div>
			</div>
		{/each}
	</div>
</div>