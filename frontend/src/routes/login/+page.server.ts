import { type Cookies, type Actions, redirect, fail } from '@sveltejs/kit';
import { BACKEND_URL, COOKIES_AGE_DAY } from "$env/static/private";

export const actions = {
	login: async ({ cookies, request }: { cookies: Cookies; request: Request }) => {
		const data = await request.formData();
		const login = data.get('login');
		const password = data.get('password');

        if (!login || !password) {
			return fail(400, { incorrect: true, login, message: "Both fields are required." });
		}
    
        const response = await fetch(`${BACKEND_URL}/users/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ login, password }),
        });

        if (!response.ok) {
			return fail(400, { incorrect: true, login, message: "Something has gone wrong!" });
		}
        
        const setCookieHeader = await response.headers.get('set-cookie');

        if (!setCookieHeader) {
			return fail(400, { incorrect: true, login, message: "Invalid credentials!" });
		}

        const cookieAgeDay: number = Number(COOKIES_AGE_DAY);
        cookies.set('access_token_cookie', setCookieHeader.split("access_token_cookie=")[1].split(";")[0], { path: '/', maxAge: 60 * 60 * 24 * cookieAgeDay });
        return redirect(303, '/home');
	},
} satisfies Actions;