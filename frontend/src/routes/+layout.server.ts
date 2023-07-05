export async function load ( { cookies } ) {
    const token = await cookies.get("token");
    if (token) {
        return {
            user: true
        }
    }
    return {
        user: false
    }
}