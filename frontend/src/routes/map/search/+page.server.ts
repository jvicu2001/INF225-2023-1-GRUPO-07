export const ssr = false;

interface Metadata {
    _id: string;
    fileData: {
        count: number;
        crs: string;
        dtype: string;
        driver: string;
        bounds: [number, number, number, number];
        lnglat: [number, number];
        height: number;
        width: number;
        shape: [number, number];
        res: [number, number];
        nodata: number;
    };
    user: string;
    fileName: string;
    fileDataType: number;
    fileId: string;
}


export async function load({url}) {
    const query = url.searchParams.get("query") ? url.searchParams.get("query") : "";
    const limit = url.searchParams.get("limit") ? url.searchParams.get("limit") : 50;
    const page = url.searchParams.get("page") ? url.searchParams.get("page") : 1;

    const results = await fetch("http://metadata:8010/metadata/?" + new URLSearchParams({
        "query": query,
        "limit": limit,
        "page": page
    }), {
        method: "GET",
    })

    const metadata: Metadata[] = await results.json();
    
    return {metadata};
}