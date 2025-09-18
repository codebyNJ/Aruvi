"use client"

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Download, Loader2 } from 'lucide-react';

type GeneratorMode = 'kolam' | 'mandala';
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

const PATTERN_TYPES = [
  { value: 'circles', label: 'Circles' },
  { value: 'petals', label: 'Petals' },
  { value: 'geometric', label: 'Geometric' },
  { value: 'dots', label: 'Dots' },
  { value: 'lines', label: 'Lines' },
  { value: 'triangles', label: 'Triangles' },
  { value: 'stars', label: 'Stars' },
];

const COLOR_SCHEMES_MANDALA = [
  { value: 'rainbow', label: 'Rainbow' },
  { value: 'warm', label: 'Warm' },
  { value: 'cool', label: 'Cool' },
  { value: 'monochrome', label: 'Monochrome' },
  { value: 'earth', label: 'Earth Tones' },
];

const API_BASE_URL = 'https://aruvi.onrender.com';

export default function KolamGenerator() {
  const [mode, setMode] = useState<GeneratorMode>('kolam');
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
  
  // Mandala specific state
  const [layers, setLayers] = useState<number>(6);
  const [symmetry, setSymmetry] = useState<number>(8);
  const [patternTypes, setPatternTypes] = useState<string[]>(['circles', 'petals']);
  const [usePreset, setUsePreset] = useState<boolean>(false);
  const [preset, setPreset] = useState<string>('classic');
  const [colorSchemeMandala, setColorSchemeMandala] = useState('rainbow');

  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedImage, setGeneratedImage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const generateArt = async () => {
    if (mode === 'kolam') {
      return generateKolam();
    } else {
      return generateMandala();
    }
  };

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

  const generateMandala = async () => {
    setIsGenerating(true);
    setError(null);
    
    try {
      const params = new URLSearchParams();
      
      if (usePreset) {
        params.append('preset', preset);
      } else {
        params.append('size', size.toString());
        params.append('layers', layers.toString());
        params.append('symmetry', symmetry.toString());
        params.append('pattern_types', patternTypes.join(','));
        params.append('color_scheme', colorSchemeMandala);
        params.append('complexity', complexity.toString());
      }
  
      const apiBaseUrl = 'https://aruvi-1.onrender.com';
      const response = await fetch(`${apiBaseUrl}/api/mandala?${params.toString()}`, {
        method: 'GET',
        headers: {
          'Accept': 'image/svg+xml',
        },
        mode: 'cors',
      });
  
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to generate Mandala: ${response.status} ${response.statusText} - ${errorText}`);
      }
  
      // Get the response as text
      const responseText = await response.text();
      
      // Check if the response is already an SVG (starts with <svg)
      if (responseText.trim().startsWith('<svg')) {
        // It's already an SVG, use it directly
        const svgBlob = new Blob([responseText], { type: 'image/svg+xml' });
        const svgUrl = URL.createObjectURL(svgBlob);
        setGeneratedImage(svgUrl);
      } else {
        // Try to decode as hex if it's not already SVG
        try {
          // Convert hex string to Uint8Array
          const bytes = new Uint8Array(responseText.length / 2);
          for (let i = 0; i < responseText.length; i += 2) {
            bytes[i / 2] = parseInt(responseText.substring(i, i + 2), 16);
          }
          
          // Convert to string
          const decoder = new TextDecoder('utf-8');
          const svgText = decoder.decode(bytes);
          
          // Create data URL
          const svgBlob = new Blob([svgText], { type: 'image/svg+xml' });
          const svgUrl = URL.createObjectURL(svgBlob);
          setGeneratedImage(svgUrl);
        } catch (hexError) {
          console.error('Hex decoding failed:', hexError);
          // If hex decoding fails, try to use the response as is
          const svgBlob = new Blob([responseText], { type: 'image/svg+xml' });
          const svgUrl = URL.createObjectURL(svgBlob);
          setGeneratedImage(svgUrl);
        }
      }
      
    } catch (err) {
      console.error('Error generating Mandala:', err);
      setError(err instanceof Error ? err.message : 'Failed to generate Mandala. Please try again.');
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

  const downloadImage = () => {
  if (!generatedImage) return;
  
  const link = document.createElement('a');
  link.href = generatedImage;
  link.download = `mandala-${Date.now()}.svg`;
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
        

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Controls */}
          <div className="lg:col-span-1">
            <Card className="sticky top-8">
              <CardHeader>
                <div className="flex justify-between items-center">
                  <CardTitle>
                    {mode === 'kolam' ? 'Kolam Generator' : 'Mandala Generator'}
                  </CardTitle>
                  <div className="inline-flex rounded-md shadow-sm" role="group">
                    <button
                      type="button"
                      onClick={() => setMode('kolam')}
                      className={`px-4 py-2 text-sm font-medium rounded-l-lg ${
                        mode === 'kolam'
                          ? 'bg-indigo-600 text-white'
                          : 'bg-white text-gray-700 hover:bg-gray-50'
                      }`}
                    >
                      Kolam Generator
                    </button>
                    <button
                      type="button"
                      onClick={() => setMode('mandala')}
                      className={`px-4 py-2 text-sm font-medium rounded-r-lg ${
                        mode === 'mandala'
                          ? 'bg-indigo-600 text-white'
                          : 'bg-white text-gray-700 hover:bg-gray-50'
                      }`}
                    >
                      Mandala Generator
                    </button>
                  </div>
                </div>
                <CardDescription>
                  {mode === 'kolam' 
                    ? 'Create beautiful Kolam designs' 
                    : 'Generate intricate Mandala patterns'}
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {mode === 'kolam' ? (
                  // Existing Kolam controls
                  <>
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
                  </>
                ) : (
                  // Mandala controls
                  <>
                    <div className="flex items-center space-x-2">
                      <input 
                        type="checkbox" 
                        id="use-preset" 
                        checked={usePreset}
                        onChange={(e) => setUsePreset(e.target.checked)}
                        className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                      />
                      <Label htmlFor="use-preset">Use Preset</Label>
                    </div>

                    {usePreset ? (
                      <div>
                        <Label htmlFor="preset">Preset</Label>
                        <Select 
                          value={preset} 
                          onValueChange={setPreset}
                        >
                          <SelectTrigger className="w-full">
                            <SelectValue placeholder="Select a preset" />
                          </SelectTrigger>
                          <SelectContent>
                            {['classic', 'complex', 'simple', 'floral', 'geometric'].map((p) => (
                              <SelectItem key={p} value={p}>
                                {p.charAt(0).toUpperCase() + p.slice(1)}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>
                    ) : (
                      <>
                        <div>
                          <Label htmlFor="size">Canvas Size: {size}px</Label>
                          <Slider
                            id="size"
                            min={200}
                            max={2000}
                            step={100}
                            value={[size]}
                            onValueChange={([value]) => setSize(value)}
                            className="mt-2"
                          />
                        </div>

                        <div>
                          <Label htmlFor="layers">Layers: {layers}</Label>
                          <Slider
                            id="layers"
                            min={1}
                            max={15}
                            value={[layers]}
                            onValueChange={([value]) => setLayers(value)}
                            className="mt-2"
                          />
                        </div>

                        <div>
                          <Label htmlFor="symmetry">Symmetry: {symmetry}</Label>
                          <Slider
                            id="symmetry"
                            min={3}
                            max={24}
                            value={[symmetry]}
                            onValueChange={([value]) => setSymmetry(value)}
                            className="mt-2"
                          />
                        </div>

                        <div>
                          <Label>Pattern Types</Label>
                          <div className="mt-2 space-y-2">
                            {PATTERN_TYPES.map((type) => (
                              <div key={type.value} className="flex items-center space-x-2">
                                <input
                                  type="checkbox"
                                  id={`pattern-${type.value}`}
                                  checked={patternTypes.includes(type.value)}
                                  onChange={(e) => {
                                    if (e.target.checked) {
                                      setPatternTypes([...patternTypes, type.value]);
                                    } else {
                                      setPatternTypes(patternTypes.filter(t => t !== type.value));
                                    }
                                  }}
                                  className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                                />
                                <Label htmlFor={`pattern-${type.value}`}>
                                  {type.label}
                                </Label>
                              </div>
                            ))}
                          </div>
                        </div>

                        <div>
                          <Label htmlFor="color-scheme">Color Scheme</Label>
                          <Select 
                            value={colorSchemeMandala} 
                            onValueChange={setColorSchemeMandala}
                          >
                            <SelectTrigger className="w-full mt-2">
                              <SelectValue placeholder="Select a color scheme" />
                            </SelectTrigger>
                            <SelectContent>
                              {COLOR_SCHEMES_MANDALA.map((scheme) => (
                                <SelectItem key={scheme.value} value={scheme.value}>
                                  {scheme.label}
                                </SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                        </div>
                      </>
                    )}
                  </>
                )}
              </CardContent>
              <CardFooter>
                <Button 
                  onClick={generateArt}
                  disabled={isGenerating}
                  className="w-full"
                >
                  {isGenerating ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      {mode === 'kolam' ? 'Generating Kolam...' : 'Generating Mandala...'}
                    </>
                  ) : (
                    `Generate ${mode === 'kolam' ? 'Kolam' : 'Mandala'}`
                  )}
                </Button>
              </CardFooter>
            </Card>
          </div>

          {/* Preview */}
          <div className="lg:col-span-2">
            <Card className="h-full">
              <CardHeader>
                <CardTitle>Preview</CardTitle>
                <CardDescription>
                  {mode === 'kolam' 
                    ? 'Your generated kolam will appear here' 
                    : 'Your generated mandala will appear here'}
                </CardDescription>
              </CardHeader>
              <CardContent className="flex flex-col items-center justify-center p-6 min-h-[500px] bg-gray-50 rounded-lg">
                {error ? (
                  <div className="text-red-500 text-center">
                    <p>Error generating {mode}:</p>
                    <p className="text-sm mt-2">{error}</p>
                  </div>
                ) : generatedImage ? (
                  <div className="relative w-full max-w-md">
                    <div className="w-full bg-white p-4 rounded-lg shadow-lg flex items-center justify-center">
                      <img 
                        src={generatedImage} 
                        alt={mode === 'kolam' ? 'Generated Kolam' : 'Generated Mandala'}
                        className="max-w-full h-auto"
                      />
                    </div>
                    <Button 
                      onClick={mode === 'kolam' ? downloadKolam : downloadImage}
                      className="mt-4 w-full"
                      variant="outline"
                    >
                      <Download className="mr-2 h-4 w-4" />
                      {mode === 'kolam' ? 'Download Kolam' : 'Download Mandala'}
                    </Button>
                  </div>
                ) : (
                  <div className="text-gray-400 text-center">
                    <p>Click &quot;Generate {mode === 'kolam' ? 'Kolam' : 'Mandala'}&quot; to create your design</p>
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
