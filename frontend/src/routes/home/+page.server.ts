import type { PageServerLoad } from './$types';
import { BACKEND_URL } from "$env/static/private";
import jwt from 'jsonwebtoken';
export const load: PageServerLoad = async ({ cookies }) => {
	const session = cookies.get('access_token_cookie');
	let user_id = null;
	if (session) {
		const decoded = jwt.decode(session);
		if (decoded && typeof decoded.sub === 'string') {
			user_id = JSON.parse(decoded.sub).user_id;
		}
	}

	const [responseUpcoming, responseAll, responseUser] = await Promise.all([
		fetch(`${BACKEND_URL}/events/upcoming/${user_id}`, {
			method: 'GET',
			headers: {
				'Cookie': `access_token_cookie=${session}`
			}
		}),
		fetch(`${BACKEND_URL}/events/user/${user_id}`, {
			method: 'GET',
			headers: {
				'Cookie': `access_token_cookie=${session}`
			}
		}),
		fetch(`${BACKEND_URL}/users/`, {
			method: 'GET',
			headers: {
				'Cookie': `access_token_cookie=${session}`
			}
		})
	]);

	if (!responseUpcoming.ok || !responseAll.ok || !responseUser.ok) {
		return {
			status: 500,
			error: new Error('Failed to fetch data'),
		};
	}

	const [upcoming, all, users] = await Promise.all([
		responseUpcoming.json(),
		responseAll.json(),
		responseUser.json()
	]);

	interface User {
		id: number;
		name: string;
		surname: string;
	}

	const usersDict = users.reduce((acc: Record<number, User>, item: User) => {
		acc[item.id] = item;
		return acc;
	}, {} as Record<number, User>);

	return {
		event: {
			upcoming: upcoming,
			past: all.filter((event: { date: string }) => (event.date < new Date().toISOString())),
			users: usersDict
		}
	};
};