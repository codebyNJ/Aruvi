import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const formData = await request.formData();
    const image = formData.get('image') as File | null;

    if (!image) {
      return new NextResponse('No image provided', { status: 400 });
    }

    // Convert the image to base64
    const buffer = await image.arrayBuffer();
    const base64Image = Buffer.from(buffer).toString('base64');

    // Call the Kolam extraction API
    const KOLAM_EXTRACTION_API = 'https://aruvi-2.onrender.com/convert';
    
    const response = await fetch(KOLAM_EXTRACTION_API, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        image: base64Image,
      }),
    });

    if (!response.ok) {
      const error = await response.text();
      console.error('Kolam extraction API error:', error);
      return new NextResponse('Failed to process image', { status: response.status });
    }

    const data = await response.json();
    
    // Ensure the response has the expected format
    if (!data.binary_svg || !data.paths_svg || !data.preview || data.paths_count === undefined) {
      console.error('Invalid response format from Kolam extraction API:', data);
      return new NextResponse('Invalid response format from server', { status: 500 });
    }

    return NextResponse.json(data);
  } catch (error) {
    console.error('Error processing image:', error);
    return new NextResponse('Internal Server Error', { status: 500 });
  }
}
