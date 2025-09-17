"use client"

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Download, Loader2 } from 'lucide-react';

type KolamType = 'traditional' | 'geometric' | 'iyal' | 'rangoli' | 'kavi';
type BrushType = 'round' | 'flat' | 'calligraphy' | 'dot';
type BackgroundType = 'white' | 'black' | 'sand' | 'red' | 'custom';
type ColorScheme = 'vibrant' | 'pastel' | 'monochrome' | 'contrast' | 'earthy';

const KOLAM_TYPES = [
  { value: 'traditional', label: 'Traditional' },
  { value: 'geometric', label: 'Geometric' },
  { value: 'iyal', label: 'Iyal' },
  { value: 'rangoli', label: 'Rangoli' },
  { value: 'kavi', label: 'Kavi' },
];

const SHAPES = ['circle', 'square'];
const MOTIF_TYPES = [''];
const BRUSH_TYPES: BrushType[] = ['round'];
const BACKGROUNDS: BackgroundType[] = ['white', 'black', 'sand', 'red', 'custom'];
const COLOR_SCHEMES: ColorScheme[] = ['vibrant', 'pastel', 'monochrome', 'contrast', 'earthy'];

const API_BASE_URL = 'https://aruvi.onrender.com';

export default function KolamGenerator() {
  // Common parameters
  const [type, setType] = useState<KolamType>('traditional');
  const [size, setSize] = useState(500);
  const [background, setBackground] = useState<BackgroundType>('white');
  const [brush, setBrush] = useState<BrushType>('round');
  
  // Type-specific parameters
  const [shape, setShape] = useState('circle');
  const [complexity, setComplexity] = useState(5);
  const [flowIntensity, setFlowIntensity] = useState(0.5);
  const [organicFactor, setOrganicFactor] = useState(0.5);
  const [motifType, setMotifType] = useState('floral');
  const [colorScheme, setColorScheme] = useState<ColorScheme>('vibrant');
  const [lineThickness, setLineThickness] = useState(1.0);
  const [precision, setPrecision] = useState(0.8);
  
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedImage, setGeneratedImage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const generateKolam = async () => {
    setIsGenerating(true);
    setError(null);
    
    try {
      // Prepare parameters
      const params = new URLSearchParams({
        type: type, // 'traditional' or other types
        size: type === 'traditional' 
          ? Math.min(Math.max(Math.floor(size / 100), 3), 15).toString()
          : Math.min(Math.max(size / 100, 3), 15).toString(),
        background: background === 'white' ? '#ffffff' : 
                   background === 'black' ? '#000000' :
                   background === 'sand' ? '#f5e7d8' :
                   background === 'red' ? '#7b3306' : '#ffffff',
        brush: brush === 'round' ? '#ffffff' :
               brush === 'flat' ? '#f8f1f1' :
               brush === 'calligraphy' ? '#e8e8e8' : '#f0f0f0'
      });
  
      // Add type-specific parameters for non-traditional kolams
      if (type !== 'traditional') {
        switch (type) {
          case 'geometric':
            params.append('shape', shape);
            params.append('complexity', Math.min(Math.max(complexity, 1), 5).toString());
            break;
          case 'iyal':
            params.append('flow_intensity', Math.min(Math.max(flowIntensity, 0.1), 1).toFixed(1));
            params.append('organic_factor', Math.min(Math.max(organicFactor, 0), 1).toFixed(1));
            break;
          case 'rangoli':
            params.append('motif_type', motifType);
            params.append('color_scheme', colorScheme);
            params.append('complexity', Math.min(Math.max(complexity, 1), 5).toString());
            break;
          case 'kavi':
            params.append('line_thickness', Math.min(Math.max(lineThickness, 0.5), 5).toFixed(1));
            params.append('precision', Math.min(Math.max(precision, 0.1), 1).toFixed(1));
            break;
        }
      }
  
      // Call our API route
      const response = await fetch(`/api/kolam?${params.toString()}`);
  
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to generate Kolam: ${response.status} ${response.statusText} - ${errorText}`);
      }
  
      // Get the SVG as text and convert to data URL
      const svgText = await response.text();
      const svgBlob = new Blob([svgText], { type: 'image/svg+xml' });
      const svgUrl = URL.createObjectURL(svgBlob);
      setGeneratedImage(svgUrl);
    } catch (err) {
      console.error('Error generating Kolam:', err);
      setError(err instanceof Error ? err.message : 'Failed to generate Kolam. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const downloadKolam = () => {
    if (!generatedImage) return;
    
    const link = document.createElement('a');
    link.href = generatedImage;
    link.download = `kolam-${type}-${Date.now()}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Render parameter controls based on selected type
  const renderTypeSpecificControls = () => {
    switch (type) {
      case 'geometric':
        return (
          <>
            <div className="space-y-2">
              <Label htmlFor="shape">Shape</Label>
              <Select value={shape} onValueChange={setShape}>
                <SelectTrigger>
                  <SelectValue placeholder="Select shape" />
                </SelectTrigger>
                <SelectContent>
                  {SHAPES.map((s) => (
                    <SelectItem key={s} value={s}>
                      {s.charAt(0).toUpperCase() + s.slice(1)}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label>Complexity: {complexity}/10</Label>
              <Slider
                min={1}
                max={10}
                step={1}
                value={[complexity]}
                onValueChange={([value]) => setComplexity(value)}
              />
            </div>
          </>
        );
      
      case 'iyal':
        return (
          <>
            <div className="space-y-2">
              <Label>Flow Intensity: {flowIntensity.toFixed(1)}</Label>
              <Slider
                min={0}
                max={1}
                step={0.1}
                value={[flowIntensity]}
                onValueChange={([value]) => setFlowIntensity(value)}
              />
            </div>
            <div className="space-y-2">
              <Label>Organic Factor: {organicFactor.toFixed(1)}</Label>
              <Slider
                min={0}
                max={1}
                step={0.1}
                value={[organicFactor]}
                onValueChange={([value]) => setOrganicFactor(value)}
              />
            </div>
          </>
        );

      case 'rangoli':
        return (
          <>
            <div className="space-y-2">
              <Label htmlFor="motif">Motif Type</Label>
              <Select value={motifType} onValueChange={setMotifType}>
                <SelectTrigger>
                  <SelectValue placeholder="Select motif" />
                </SelectTrigger>
                <SelectContent>
                  {MOTIF_TYPES.map((m) => (
                    <SelectItem key={m} value={m}>
                      {m.charAt(0).toUpperCase() + m.slice(1)}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label>Color Scheme</Label>
              <Select value={colorScheme} onValueChange={(v: ColorScheme) => setColorScheme(v)}>
                <SelectTrigger>
                  <SelectValue placeholder="Select color scheme" />
                </SelectTrigger>
                <SelectContent>
                  {COLOR_SCHEMES.map((c) => (
                    <SelectItem key={c} value={c}>
                      {c.charAt(0).toUpperCase() + c.slice(1)}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label>Complexity: {complexity}/10</Label>
              <Slider
                min={1}
                max={10}
                step={1}
                value={[complexity]}
                onValueChange={([value]) => setComplexity(value)}
              />
            </div>
          </>
        );

      case 'kavi':
        return (
          <>
            <div className="space-y-2">
              <Label>Line Thickness: {lineThickness.toFixed(1)}</Label>
              <Slider
                min={0.1}
                max={3}
                step={0.1}
                value={[lineThickness]}
                onValueChange={([value]) => setLineThickness(value)}
              />
            </div>
            <div className="space-y-2">
              <Label>Precision: {precision.toFixed(1)}</Label>
              <Slider
                min={0.1}
                max={1}
                step={0.1}
                value={[precision]}
                onValueChange={([value]) => setPrecision(value)}
              />
            </div>
          </>
        );

      default: // traditional
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Kolam Generator</h1>
          <p className="text-lg text-gray-600">Create beautiful Kolam designs with AI</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Controls */}
          <div className="lg:col-span-1">
            <Card className="sticky top-8">
              <CardHeader>
                <CardTitle>Design Your Kolam</CardTitle>
                <CardDescription>Customize the parameters to generate your perfect Kolam</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="space-y-2">
                  <Label htmlFor="type">Kolam Type</Label>
                  <Select value={type} onValueChange={(v: KolamType) => setType(v)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select type" />
                    </SelectTrigger>
                    <SelectContent>
                      {KOLAM_TYPES.map((t) => (
                        <SelectItem key={t.value} value={t.value}>
                          {t.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label>Size: {size}px</Label>
                  <Slider
                    min={100}
                    max={1000}
                    step={50}
                    value={[size]}
                    onValueChange={([value]) => setSize(value)}
                  />
                </div>

                <div className="space-y-2">
                  <Label>Background</Label>
                  <Select value={background} onValueChange={(v: BackgroundType) => setBackground(v)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select background" />
                    </SelectTrigger>
                    <SelectContent>
                      {BACKGROUNDS.map((bg) => (
                        <SelectItem key={bg} value={bg}>
                          {bg.charAt(0).toUpperCase() + bg.slice(1)}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label>Brush Type</Label>
                  <Select value={brush} onValueChange={(v: BrushType) => setBrush(v)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select brush" />
                    </SelectTrigger>
                    <SelectContent>
                      {BRUSH_TYPES.map((b) => (
                        <SelectItem key={b} value={b}>
                          {b.charAt(0).toUpperCase() + b.slice(1)}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Type-specific controls */}
                <div className="space-y-4 pt-2 border-t border-gray-100">
                  {renderTypeSpecificControls()}
                </div>

                <Button 
                  className="w-full mt-6" 
                  size="lg"
                  onClick={generateKolam}
                  disabled={isGenerating}
                >
                  {isGenerating ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Generating...
                    </>
                  ) : (
                    'Generate Kolam'
                  )}
                </Button>

                {error && (
                  <div className="p-3 text-sm text-red-600 bg-red-50 rounded-md">
                    {error}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Preview */}
          <div className="lg:col-span-2">
            <Card className="h-full">
              <CardHeader>
                <div className="flex justify-between items-center">
                  <CardTitle>Your Kolam</CardTitle>
                  {generatedImage && (
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={downloadKolam}
                      className="flex items-center gap-2"
                    >
                      <Download className="h-4 w-4" />
                      Download
                    </Button>
                  )}
                </div>
              </CardHeader>
              <CardContent className="flex items-center justify-center p-8 min-h-[500px] bg-gray-50">
                {generatedImage ? (
                  <div className="relative w-full h-full flex items-center justify-center">
                    <img 
                      src={generatedImage} 
                      alt="Generated Kolam" 
                      className="max-w-full max-h-[600px] object-contain"
                    />
                  </div>
                ) : (
                  <div className="text-center text-gray-400">
                    <p>Your generated Kolam will appear here</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
