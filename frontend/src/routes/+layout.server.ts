import { redirect } from "@sveltejs/kit";

export const load = async ({ cookies, url }: { cookies: any; url: any }) => {
    const token = cookies.get("session");

    if (!token && (url.pathname !== "/login" && url.pathname !== "/sign-up")) {
        throw redirect(307, "/login");
    }

    if (token && (url.pathname === "/login" || url.pathname === "/sign-up" || url.pathname === "/")) {
        throw redirect(307, "/home");
    }

    const is_logged_in = !!token;
    return { is_logged_in };
};