// pages/api/mandala/route.ts
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
    
    console.log('Calling external API:', apiUrl);
    
    const response = await fetch(apiUrl, {
      headers: {
        'Accept': 'image/svg+xml',
      },
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('External API error:', response.status, errorText);
      return NextResponse.json(
        { error: 'Failed to generate mandala', details: errorText },
        { status: response.status }
      );
    }

    // Get the response content - it should be SVG from the Python backend
    const svgContent = await response.text();
    
    // Check if we have valid SVG content
    if (!svgContent.trim().startsWith('<?xml') && !svgContent.trim().startsWith('<svg')) {
      console.error('Response is not valid SVG:', svgContent.substring(0, 100));
      return NextResponse.json(
        { error: 'API returned non-SVG content', content: svgContent.substring(0, 200) },
        { status: 500 }
      );
    }
    
    // Clean up the SVG content if it has XML declaration (which can cause issues)
    let cleanSvgContent = svgContent;
    if (svgContent.trim().startsWith('<?xml')) {
      // Remove XML declaration to make it compatible with data URLs
      cleanSvgContent = svgContent.replace(/<\?xml.*?\?>/, '').trim();
    }
    
    // Return the SVG with proper headers
    return new NextResponse(cleanSvgContent, {
      status: 200,
      headers: {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'public, max-age=3600',
      },
    });
    
  } catch (error) {
    console.error('Mandala API error:', error);
    return NextResponse.json(
      { 
        error: 'Failed to generate mandala',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}