"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"

type Message = {
  id: string
  content: string
  isUser: boolean
  timestamp: Date
}

type Document = {
  id: string
  title: string
  type: 'pdf' | 'link' | 'image'
  url: string
  uploadedAt: Date
}

// Kolam pattern as SVG background
const kolamPattern = `
  <svg width="100%" height="100%" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" opacity="0.05">
    <path d="M100 20C100 20, 120 40, 140 40C160 40, 160 20, 180 20" stroke="#1B596F" fill="none" stroke-width="1.5" />
    <path d="M100 180C100 180, 120 160, 140 160C160 160, 160 180, 180 180" stroke="#1B596F" fill="none" stroke-width="1.5" />
    <path d="M20 100C20 100, 40 120, 40 140C40 160, 20 160, 20 180" stroke="#1B596F" fill="none" stroke-width="1.5" />
    <path d="M180 100C180 100, 160 120, 160 140C160 160, 180 160, 180 180" stroke="#1B596F" fill="none" stroke-width="1.5" />
    <circle cx="100" cy="100" r="30" fill="none" stroke="#1B596F" stroke-width="1" />
    <circle cx="100" cy="100" r="10" fill="#1B596F" />
  </svg>
`

export function KolamGPTChat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [isSidebarOpen, setIsSidebarOpen] = useState(true)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  // Sample documents data
  const [documents, setDocuments] = useState<Document[]>([
    {
      id: '1',
      title: 'Introduction to Kolam Art',
      type: 'pdf',
      url: '#',
      uploadedAt: new Date('2025-09-15')
    },
    {
      id: '2',
      title: 'Traditional Kolam Patterns',
      type: 'image',
      url: '#',
      uploadedAt: new Date('2025-09-14')
    },
    {
      id: '3',
      title: 'Kolam in Modern Art',
      type: 'link',
      url: '#',
      uploadedAt: new Date('2025-09-10')
    }
  ])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      content: input,
      isUser: true,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsLoading(true)
    
    setTimeout(() => inputRef.current?.focus(), 0)

    try {
      await new Promise((resolve) => setTimeout(resolve, 1500))
      
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: "I'm KolamGPT, your AI guide to the beautiful world of Kolam art. I can help you explore patterns, history, and cultural significance. What would you like to know?",
        isUser: false,
        timestamp: new Date(),
      }
      
      setMessages((prev) => [...prev, botMessage])
    } catch (error) {
      console.error("Error getting response:", error)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  useEffect(() => {
    if (messages.length === 0) {
      const welcomeMessage: Message = {
        id: 'welcome',
        content: 'Namaste! I\'m your Kolam art assistant. Feel free to ask me anything about Kolam patterns, history, or techniques.',
        isUser: false,
        timestamp: new Date()
      }
      setMessages([welcomeMessage])
    }
  }, [])

  return (
    <div className="fixed inset-0 flex flex-col h-screen bg-gradient-to-br from-[#f0f9ff] to-[#e0f2fe] overflow-hidden">
      {/* Kolam Pattern Background */}
      <div 
        className="absolute inset-0 -z-10 opacity-10"
        dangerouslySetInnerHTML={{ __html: kolamPattern }}
      />

      {/* Sidebar */}
      <div 
        className={`${isSidebarOpen ? 'w-72 translate-x-0' : '-translate-x-full'} 
        fixed left-0 top-0 bottom-0 transition-all duration-300 z-20`}
      >
        <div className="h-full flex flex-col bg-white/30 backdrop-blur-xl border-r border-white/30">
          <div className="p-4 border-b border-white/20">
            <div className="flex justify-between items-center">
              <h2 className="text-lg font-semibold text-[#1B596F] drop-shadow-sm">Kolam References</h2>
              <button 
                onClick={() => setIsSidebarOpen(false)}
                className="text-[#1B596F] hover:text-[#0f4557] transition-colors"
              >
                ✕
              </button>
            </div>
            
            <div className="mt-4">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search documents..."
                  className="w-full px-3 py-2 bg-white/50 border border-white/50 rounded-lg text-sm text-[#1B596F] placeholder-[#7fb6c9] focus:outline-none focus:ring-2 focus:ring-[#1B596F]/30 focus:border-transparent backdrop-blur-sm"
                />
                <span className="absolute right-3 top-2.5 text-[#7fb6c9]">
                  🔍
                </span>
              </div>
            </div>
          </div>
          
          <div className="flex-1 overflow-y-auto p-2 space-y-2 custom-scrollbar">
            {documents.map((doc) => (
              <div 
                key={doc.id} 
                className="p-3 bg-white/40 backdrop-blur-sm rounded-lg hover:bg-white/60 transition-all duration-200 cursor-pointer border border-white/30 hover:border-white/50"
              >
                <div className="text-sm font-medium text-[#1B596F]">{doc.title}</div>
                <div className="flex justify-between items-center mt-1">
                  <span className="text-xs text-[#5c8a9a]">
                    {doc.type.toUpperCase()} • {doc.uploadedAt.toLocaleDateString()}
                  </span>
                </div>
              </div>
            ))}
          </div>
          
          <div className="p-4 border-t border-white/20">
            <button className="w-full py-2.5 bg-[#1B596F]/90 hover:bg-[#1B596F] text-white rounded-lg transition-all duration-200 flex items-center justify-center gap-2 shadow-sm hover:shadow-md">
              <span>+</span> Upload Document
            </button>
          </div>
        </div>
      </div>

      {/* Chat Area */}
      <div className={`flex-1 flex flex-col h-full transition-all duration-300 ${isSidebarOpen ? 'ml-72' : 'ml-0'}`}>
        {/* Chat Header */}
        <div className="p-4 bg-white/30 backdrop-blur-xl border-b border-white/30 flex items-center justify-between">
          <div className="flex items-center">
            {!isSidebarOpen && (
              <button 
                onClick={() => setIsSidebarOpen(true)}
                className="mr-4 text-[#1B596F] hover:text-[#0f4557] transition-colors"
              >
                ☰
              </button>
            )}
            <h2 className="text-lg font-semibold text-[#1B596F] drop-shadow-sm">KolamGPT</h2>
          </div>
          <div className="flex space-x-2">
            <button className="p-2 text-[#1B596F] hover:bg-white/30 rounded-full transition-colors">
              ⚙️
            </button>
          </div>
        </div>

        {/* Messages Container */}
        <div className="flex-1 overflow-y-auto custom-scrollbar relative">
          <div className="max-w-3xl mx-auto w-full p-6 space-y-6">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[85%] rounded-2xl p-4 relative overflow-hidden ${
                    message.isUser
                      ? 'bg-gradient-to-br from-[#1B596F] to-[#2D8BBA] text-white rounded-br-none shadow-lg'
                      : 'bg-white/70 backdrop-blur-sm border border-white/50 shadow-sm rounded-bl-none'
                  }`}
                >
                  {/* Message content */}
                  <div className="relative z-10">
                    <div className="text-sm whitespace-pre-wrap">
                      {message.content}
                    </div>
                    <div className={`text-xs mt-1.5 ${message.isUser ? 'text-blue-100/80' : 'text-gray-500'}`}>
                      {message.timestamp.toLocaleTimeString([], {
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </div>
                  </div>
                  
                  {/* Glass effect overlay */}
                  {!message.isUser && (
                    <div className="absolute inset-0 bg-white/30 backdrop-blur-[1px] -z-0" />
                  )}
                </div>
              </div>
            ))}
            
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-white/70 backdrop-blur-sm border border-white/50 rounded-2xl p-4 max-w-[70%] rounded-bl-none">
                  <div className="flex space-x-2">
                    <div className="h-2 w-2 rounded-full bg-[#1B596F] animate-bounce" style={{ animationDelay: '0ms' }} />
                    <div className="h-2 w-2 rounded-full bg-[#1B596F] animate-bounce" style={{ animationDelay: '150ms' }} />
                    <div className="h-2 w-2 rounded-full bg-[#1B596F] animate-bounce" style={{ animationDelay: '300ms' }} />
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input Area */}
        <div className="p-4 bg-white/30 backdrop-blur-xl border-t border-white/30">
          <form onSubmit={handleSubmit} className="max-w-3xl mx-auto w-full">
            <div className="relative">
              <Textarea
                ref={inputRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about Kolam art..."
                className="min-h-[60px] max-h-48 pr-12 resize-none border border-white/50 bg-white/60 backdrop-blur-sm focus:border-[#1B596F]/50 focus:ring-1 focus:ring-[#1B596F]/30 text-[#1B596F] placeholder-[#7fb6c9]"
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault()
                    handleSubmit(e)
                  }
                }}
                disabled={isLoading}
              />
              <Button
                type="submit"
                size="icon"
                className="absolute right-2 bottom-2 h-8 w-8 rounded-full bg-[#1B596F]/90 hover:bg-[#1B596F] transition-all duration-200 shadow-md hover:shadow-lg"
                disabled={!input.trim() || isLoading}
              >
                {isLoading ? (
                  <span className="animate-pulse">✉️</span>
                ) : (
                  '→'
                )}
              </Button>
            </div>
            <p className="text-xs text-center text-[#5c8a9a] mt-2">
              KolamGPT can make mistakes. Consider checking important information.
            </p>
          </form>
        </div>
      </div>

      <style jsx global>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: rgba(0, 0, 0, 0.03);
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: rgba(27, 89, 111, 0.15);
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: rgba(27, 89, 111, 0.3);
        }
        
        /* Animation for message entry */
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        
        .message-enter {
          animation: fadeIn 0.3s ease-out forwards;
        }
      `}</style>
    </div>
  )
}
