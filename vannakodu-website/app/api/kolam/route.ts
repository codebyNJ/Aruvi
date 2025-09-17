import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const kolamType = searchParams.get('type');
    
    // Use different base URL for traditional kolam
    const baseUrl = kolamType === 'traditional' 
      ? 'https://zen-kolam.vercel.app' 
      : 'https://aruvi.onrender.com';
    
    // Remove our custom type parameter and forward the rest
    const params = new URLSearchParams(searchParams);
    params.delete('type');
    
    const apiUrl = `${baseUrl}/api/kolam${kolamType && kolamType !== 'traditional' ? `/${kolamType}` : ''}?${params.toString()}`;
    
    const response = await fetch(apiUrl, {
      headers: {
        'Accept': 'image/svg+xml',
      },
    });

    if (!response.ok) {
      const errorText = await response.text();
      return new NextResponse(errorText, {
        status: response.status,
        statusText: response.statusText,
      });
    }

    // Get the SVG content
    const svg = await response.text();
    
    // Return the SVG with proper headers
    return new NextResponse(svg, {
      status: 200,
      headers: {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'public, max-age=3600',
      },
    });
    
  } catch (error) {
    console.error('Kolam API error:', error);
    return new NextResponse(JSON.stringify({ error: 'Failed to generate kolam' }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }
}
