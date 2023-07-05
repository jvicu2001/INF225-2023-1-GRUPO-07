export const ssr = false;

export const actions = {
    default: async ( {cookies} ) => {
        await cookies.set("token", "", {httpOnly: true, maxAge: 0, path: "/"});
        return {
            status: 304,
            headers: {
                location: "/"
            }
        }
    }
}