import { type Cookies, type Actions, fail } from '@sveltejs/kit';
import { BACKEND_URL } from "$env/static/private";
import jwt from 'jsonwebtoken';

function convertToISO8601(dateString: string){
    const localDate = new Date(dateString.replace(" ", "T") + ":00");
    return localDate.toISOString();
}

export const actions = {
    createevent: async ({ cookies, request }: { cookies: Cookies; request: Request }) => {
        const data = await request.formData();
        const event = data.get('event');
        const place = data.get('place');
        const datedate = data.get('datedate');
        const datetime = data.get('datetime');
        const deadlinedate = data.get('deadlinedate');
        const deadlinetime = data.get('deadlinetime');

        const date = convertToISO8601(datedate + " " + datetime);
        const deadline = convertToISO8601(deadlinedate + " " + deadlinetime);

        let user_id = null;
        
        if (!event || !place || !datedate || !datetime || !deadlinedate || !deadlinetime) {
            return { message: "All fields are required." };
        }

        const session = cookies.get("access_token_cookie");
        if (session) {
            const decoded = jwt.decode(session);
            if (decoded && typeof decoded.sub === 'string') {
                user_id = JSON.parse(decoded.sub).user_id;
            }
        }

        const responseCreateEvent = await fetch(`${BACKEND_URL}/events/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Cookie": `access_token_cookie=${session}`,
            },
            body: JSON.stringify({ event, date, deadline, place, "organizer": user_id }),
        });

        if (!responseCreateEvent.ok) {
            console.error("test");
            return fail(400, { message: "Something has gone wrong!" });
        }

        const isEventCreated = (await responseCreateEvent.json()).id;

        if (!isEventCreated) return { message: "Event not created." };
        else return { message: "Event created successfully." };
    }
} satisfies Actions;