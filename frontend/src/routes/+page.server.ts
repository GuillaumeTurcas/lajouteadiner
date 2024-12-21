import { redirect } from "@sveltejs/kit";
import { BACKEND_URL } from "$env/static/private";

export const actions = {
    logout: async ({ cookies }) => {

        const session = cookies.get("access_token_cookie");

        const responseLogout = await fetch(`${BACKEND_URL}/users/logout`, {
            method: "POST",
            headers: {
                Cookie: `access_token_cookie=${session}`,
            },
        });

        if (!responseLogout.ok) {
            throw redirect(303, "/home");
        }

        const is_logged_in = (await responseLogout.json()).message == "Logged out successfully";

        if (session && is_logged_in) {
            cookies.delete("access_token_cookie", { path: "/" });
            throw redirect(303, "/login");
        }

        throw redirect(303, "/home");
    }
};
