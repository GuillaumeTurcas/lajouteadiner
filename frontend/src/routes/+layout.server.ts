import { redirect } from "@sveltejs/kit";
import { BACKEND_URL } from "$env/static/private";

export const load = async ({ cookies, url }: { cookies: any; url: any }) => {
    const token = cookies.get("access_token_cookie");

    if (!token && (url.pathname !== "/login" && url.pathname !== "/sign-up")) {
        throw redirect(307, "/login");
    }

    const response = await fetch(`${BACKEND_URL}/users/is_login`, {
        method: 'GET',
        headers: {
            'Cookie': `access_token_cookie=${token}`
        }
    });

    if (!response.ok) {
        throw redirect(307, "/login");
    }

    const is_logged_in = (await response.json()).is_login;

    if (is_logged_in && (url.pathname === "/login" || url.pathname === "/sign-up" || url.pathname === "/")) {
        throw redirect(307, "/home");
    }

    return { is_logged_in };
};