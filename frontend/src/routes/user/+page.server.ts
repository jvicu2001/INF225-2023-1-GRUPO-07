export const actions = {
    default: async ( {cookies, request } ) => {
        const data = await request.formData();

        const token = await cookies.get("token");

        const upload_response = await fetch('http://storage:8020/upload/?' + new URLSearchParams({
            "dataType": data.get("dataType"),
        }), {
            method: 'POST',
            headers: {
                'accept': 'application/json',
                "Authorization": "Bearer " + token,
            },
            body: data
        });

        const upload_response_json = await upload_response.json();
        console.log(upload_response_json);

        if (upload_response.status === 200) {
            return {
                success: true,
                data: upload_response_json
            }
        }
        else {
            return {
                success: false,
                data: upload_response_json
            }
        }
    }
}