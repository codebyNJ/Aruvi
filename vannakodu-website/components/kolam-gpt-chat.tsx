"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"

const documents = [
  {
    name: "Document 1",
    content: "This document contains information about basic Kolam patterns and their geometric foundations.",
  },
  {
    name: "Document 2",
    content: "Advanced Kolam techniques including symmetrical designs and traditional motifs used in Tamil culture.",
  },
  {
    name: "Document 3",
    content: "Historical significance of Kolam art and its role in South Indian traditions and festivals.",
  },
  {
    name: "Document 4",
    content: "Step-by-step guide to creating complex Kolam patterns with dots and continuous lines.",
  },
  {
    name: "Document 5",
    content: "Regional variations of Kolam across different Tamil Nadu districts and their unique characteristics.",
  },
  {
    name: "Document 6",
    content: "Modern interpretations of Kolam art and its influence on contemporary design and architecture.",
  },
  {
    name: "Document 7",
    content: "Mathematical principles behind Kolam patterns including fractals and geometric progressions.",
  },
]

export function KolamGPTChat() {
  const [messages, setMessages] = useState([
    { role: "system", content: "Welcome to KolamGPT! How can I help you today?" },
  ])
  const [input, setInput] = useState("")
  const [selectedDocument, setSelectedDocument] = useState<{ name: string; content: string } | null>(null)

  const sendMessage = () => {
    if (!input.trim()) return
    setMessages([...messages, { role: "user", content: input }])
    setInput("")
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const handleDocumentClick = (doc: { name: string; content: string }) => {
    setSelectedDocument(selectedDocument?.name === doc.name ? null : doc)
  }

  return (
    <div className="flex h-screen bg-gray-100 overflow-hidden">
      {/* Left Sidebar */}
      <div className="w-64 bg-slate-200 p-4 flex flex-col" style={{ borderRadius: "0 35px 35px 0" }}>
        <div className="mb-4">
          <h2 className="font-sans text-3xl">Reference</h2>
          <h2 className="font-serif italic text-4xl">Documents</h2>
        </div>

        <div
          className="space-y-3 text-white p-4 flex-1 flex flex-col"
          style={{ backgroundColor: "#1B596F", borderRadius: "35px" }}
        >
          <div className="space-y-3 flex-shrink-0">
            {documents.map((doc, index) => (
              <button
                key={index}
                onClick={() => handleDocumentClick(doc)}
                className="w-full flex justify-between items-center hover:bg-white/10 p-2 rounded-lg transition-colors"
              >
                <span className="font-serif text-base leading-tight">{doc.name}</span>
                <span className="text-lg">+</span>
              </button>
            ))}
          </div>

          {selectedDocument && (
            <div className="mt-4 p-3 bg-white/10 rounded-lg flex-1 overflow-y-auto">
              <div className="flex justify-between items-center mb-2">
                <h3 className="font-serif text-sm text-white">{selectedDocument.name}</h3>
                <button onClick={() => setSelectedDocument(null)} className="text-white/70 hover:text-white text-sm">
                  ✕
                </button>
              </div>
              <p className="text-xs font-sans text-white/90 leading-relaxed">{selectedDocument.content}</p>
            </div>
          )}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 p-6 flex flex-col">
        <div className="flex items-start justify-between mb-4">
          <h1 className="text-7xl font-serif">KolamGPT</h1>
          <p className="text-xs max-w-sm text-right font-sans leading-relaxed">
            A sophisticated Retrieval-Augmented Generation (RAG) system specifically designed for Kolam-related queries.
            This system supports both Tamil and English queries with domain-specific optimizations for traditional Tamil
            floor art documentation.
          </p>
        </div>

        <div className="flex justify-end gap-3 mt-1 mb-4">
          <Button
            variant="outline"
            className="px-3 py-1 text-xs font-sans rounded-full border-[#1B596F] text-[#1B596F] hover:bg-[#1B596F] hover:text-white transition"
          >
            Back to Home
          </Button>
          <Button
            className="px-3 py-1 text-xs font-sans rounded-full bg-[#1B596F] text-white hover:opacity-90 transition"
          >
            Kolam Generator
          </Button>
          <Button
            className="px-3 py-1 text-xs font-sans rounded-full bg-[#1B596F] text-white hover:opacity-90 transition"
          >
            Kolam Extractor
          </Button>
        </div>


        <div className="absolute bottom-0 p-4 md:top-45 md:left-70 md:right-5 sm:left-0 sm:right-0 sm:top-auto" style={{ backgroundColor: "#1B596F", borderRadius: "35px 35px 0 0" }}>
          <Card className="h-full flex flex-col bg-white" style={{ borderRadius: "35px", border: "none" }}>
            <CardContent className="flex-1 overflow-y-auto p-4 space-y-3">
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`p-2 rounded-2xl max-w-lg font-sans text-sm ${
                    msg.role === "user" ? "text-gray-800 self-end ml-auto" : "bg-gray-200 text-gray-800 self-start"
                  }`}
                  style={msg.role === "user" ? { backgroundColor: "#1B596F", color: "white" } : {}}
                >
                  {msg.content}
                </div>
              ))}
            </CardContent>

            <div className="p-3 flex items-center gap-3">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                className="flex-1 p-2 focus:outline-none font-sans text-sm"
                style={{
                  borderRadius: "35px",
                  border: `2px solid #1B596F`,
                }}
                placeholder="Type your message..."
              />
              <Button
                onClick={sendMessage}
                className="px-4 py-2 text-white hover:opacity-90 text-sm"
                style={{
                  borderRadius: "35px",
                  backgroundColor: "#1B596F",
                }}
              >
                Send
              </Button>
            </div>
          </Card>
        </div>
      </div>
    </div>
  )
}
