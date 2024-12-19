import { redirect } from "@sveltejs/kit";

export const actions = {
    logout: async ({ cookies }) => {
        const session = cookies.get("session");

        if (session) {
            cookies.delete("session", { path: "/" });
            cookies.delete("user_id", { path: "/" });
        }

        throw redirect(303, "/login");
    }
};
