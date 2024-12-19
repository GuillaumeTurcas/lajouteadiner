import type { PageServerLoad } from './$types';
import { BACKEND_URL } from "$env/static/private";

export const load: PageServerLoad = async ({ cookies }) => {
	const user_id = cookies.get('user_id');
	const session = cookies.get('session');
	const responseUpcoming = await fetch(`${BACKEND_URL}/events/upcoming/${user_id}`, {
		method: 'GET',
		headers: {
			'Cookie': `session=${session}`
		}
	});

	const responseAll = await fetch(`${BACKEND_URL}/events/user/${user_id}`, {
		method: 'GET',
		headers: {
			'Cookie': `session=${session}`
		}
	});

	if (!responseUpcoming.ok || !responseAll.ok) {
		return {
			status: 500,
			error: new Error('Failed to fetch data'),
		};
	}

	const upcoming = await responseUpcoming.json();
	const all = await responseAll.json();
	return {
		event:{
			upcoming: upcoming,
			past: all.filter((event: { date: string }) => (event.date < new Date().toISOString()))
		}
	};
};