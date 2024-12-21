import { type Cookies, type Actions, redirect, fail } from '@sveltejs/kit';
import { BACKEND_URL, COOKIES_AGE_DAY } from "$env/static/private";

export const actions = {
	signup: async ({ cookies, request }: { cookies: Cookies; request: Request }) => {
		const data = await request.formData();
        const name = data.get('name');
        const surname = data.get('surname');
		const login = data.get('login');
        const admin = 0;
		const password = data.get('password');

        if (!login || !password || !name || !surname) {
			return fail(400, { incorrect: true, login, name, surname, message: "All fields are required." });
		}
    
        const response = await fetch(`${BACKEND_URL}/users`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, surname, login, password, admin }),
        });

        if (!response.ok) {
			return fail(400, { incorrect: true, login, name, surname, message: "Something has gone wrong!" });
		}

        const setCookieHeader = await response.headers.get('set-cookie');

        if (!setCookieHeader) {
			return fail(400, { incorrect: true, login, name, surname, message: "Something has gone wrong!" });
		}

        const cookieAgeDay: number = Number(COOKIES_AGE_DAY);
        cookies.set('access_token_cookie', setCookieHeader.split("access_token_cookie=")[1].split(";")[0], { path: '/', maxAge: 60 * 60 * 24 * cookieAgeDay });
        return redirect(303, '/home');
	},
} satisfies Actions;