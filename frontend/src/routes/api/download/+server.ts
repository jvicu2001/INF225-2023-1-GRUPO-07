export async function GET ({url}){
    const fileId = url.searchParams.get("fileId");
    const fileName = url.searchParams.get("fileName");

    // Descargar archivo desde storage:/download
    const download_response = await fetch('http://storage:8020/download/?' + new URLSearchParams({
        "id": fileId
    }));

    const file = await download_response.blob();

    return new Response({
        body: file,
        status: 200,
        headers: {
            'Content-Disposition': 'attachment; filename=' + fileName,
            'Content-Type': 'image/tiff'
        }
    })
}