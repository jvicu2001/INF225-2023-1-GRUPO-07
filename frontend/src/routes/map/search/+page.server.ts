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

export async function load({params}) {
    const query = params.query ? params.query : "";
    const results = await fetch("http://metadata:8010/metadata/?" + new URLSearchParams({
        "query": query,
        "limit": 50
    }), {
        method: "GET",
    })

    const metadata: Metadata[] = await results.json();

    console.log(metadata);
    
    return {
        metadata
    }
}