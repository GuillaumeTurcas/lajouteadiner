import type { PageServerLoad } from './$types';
import { type Cookies, type Actions, fail } from '@sveltejs/kit';
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

    const responseUserFullDetail = await fetch(`${BACKEND_URL}/users/full/${user_id}`, {
        method: 'GET',
        headers: {
            'Cookie': `access_token_cookie=${session}`
        }
    });

    if (!responseUserFullDetail.ok) {
        return {
            status: 500,
            error: new Error('Failed to fetch data'),
        };
    }

    const userFullDetail = await responseUserFullDetail.json();

    return {
        event:{
            user: userFullDetail,
        }
    };
};

export const actions = {
    changepassword: async ({ cookies, request }: { cookies: Cookies; request: Request }) => {
        const data = await request.formData();
        const oldPassword = data.get('oldpassword');
        const newPassword1 = data.get('password1');
        const newPassword2 = data.get('password2');
        let user_id = null;
        
        if (!oldPassword || !newPassword1 || !newPassword2) {
            return { message: "All fields are required." };
        }

        if (newPassword1 !== newPassword2) {
            return { message: "New passwords do not match." };
        }

        const session = cookies.get("access_token_cookie");
        if (session) {
            const decoded = jwt.decode(session);
            if (decoded && typeof decoded.sub === 'string') {
                user_id = JSON.parse(decoded.sub).user_id;
            }
        }

        const responseChangePassword = await fetch(`${BACKEND_URL}/users/change_password/${user_id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Cookie": `access_token_cookie=${session}`,
            },
            body: JSON.stringify({ "old_password": oldPassword, "new_password": newPassword1 }),
        });

        if (!responseChangePassword.ok) {
            console.error("test");
            return fail(400, { message: "Something has gone wrong!" });
        }

        const isPasswordChanged = (await responseChangePassword.json()).change_password;

        if (!isPasswordChanged) {
            return { message: "Invalid old password." };
        }
        else return { message: "Password changed successfully." };
    }
} satisfies Actions;