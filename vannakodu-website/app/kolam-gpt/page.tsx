import { KolamGPTChat } from "@/components/kolam-gpt-chat"

export default function KolamGPTPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white pt-24 pb-16 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-serif font-bold text-gray-900 mb-2">KolamGPT</h1>
          <p className="text-gray-600">Ask me anything about Kolam art, patterns, and traditions</p>
        </div>
        <KolamGPTChat />
      </div>
    </div>
  )
}
