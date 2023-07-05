// Lógica login
export const actions = {
    default: async ( {cookies, request } ) => {
        const data = await request.formData();
        const username = data.get('username');
        const password = data.get('password');

        const login_response = await fetch('http://storage:8020/auth/token', {
            method: 'POST',
            headers: {
                'accept': 'application/json'
            },
            body: new URLSearchParams({
                'grant_type': '',
                'username': username,
                'password': password,
                'scope': '',
                'client_id': '',
                'client_secret': ''
            })
        });

        if (login_response.status === 200) {
            const auth_response = await login_response.json();
            cookies.set("token", auth_response["access_token"], {httpOnly: true, maxAge: 7200, path: "/"});  
            return {
                success: true
            }
        }
        else {
            return {
                success: false
            }
        }
    }
}