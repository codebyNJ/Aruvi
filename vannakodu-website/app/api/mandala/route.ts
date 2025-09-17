import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const baseUrl = 'https://aruvi-1.onrender.com';
    
    // Check if it's a preset request
    const preset = searchParams.get('preset');
    let apiUrl: string;
    const params = new URLSearchParams(searchParams);
    
    if (preset) {
      // Handle preset request - use /preset endpoint with preset as query param
      apiUrl = `${baseUrl}/api/mandala/preset`;
      if (!params.has('size')) {
        params.set('size', '800');
      }
    } else {
      // Handle custom mandala request
      apiUrl = `${baseUrl}/api/mandala`;
    }
    
    // Add all query parameters to the URL
    apiUrl += `?${params.toString()}`;
    
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
    console.error('Mandala API error:', error);
    return new NextResponse(JSON.stringify({ 
      error: 'Failed to generate mandala',
      details: error instanceof Error ? error.message : 'Unknown error',
      url: request.url // Use the request URL instead of undefined apiUrl
    }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }
}
