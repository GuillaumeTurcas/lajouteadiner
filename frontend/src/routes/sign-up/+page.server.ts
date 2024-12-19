import { type Cookies, type Actions, redirect, fail } from '@sveltejs/kit';
import { BACKEND_URL, COOKIE_PATH } from "$env/static/private";

export const actions = {
	signup: async ({ cookies, request }: { cookies: Cookies; request: Request }) => {
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
			return fail(400, { incorrect: true, login, message: "Invalid credentials!" });
		}

        const user = await response.json();

        if (!user?.token) {
			return fail(400, { incorrect: true, login, message: "Invalid credentials!" });
		}

        cookies.set('token', user.token, { path: `/${COOKIE_PATH}` });
        return redirect(303, '/home');
	},
} satisfies Actions;