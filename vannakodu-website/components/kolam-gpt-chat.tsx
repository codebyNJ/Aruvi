"use client"

import React, { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import ReactMarkdown from 'react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/cjs/styles/prism'

interface Message {
  role: 'user' | 'assistant' | 'system'
  content: string
  isLoading?: boolean
  error?: string
}

export function KolamGPTChat() {
  const [messages, setMessages] = useState<Message[]>([
    { role: "system", content: "Welcome to KolamGPT! I can help you with anything related to Kolam art, from basic patterns to advanced techniques. What would you like to know?" },
  ])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return
    
    const userMessage: Message = { role: 'user', content: input }
    const loadingMessage: Message = { role: 'assistant', content: '', isLoading: true }
    
    setMessages(prev => [...prev, userMessage, loadingMessage])
    setInput("")
    setIsLoading(true)

    try {
      const response = await fetch('https://codenj-rag-kolam.hf.space/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: input
        })
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      
      setMessages(prev => {
        const newMessages = [...prev]
        // Remove the loading message
        newMessages.pop()
        // Add the assistant's response
        return [...newMessages, {
          role: 'assistant',
          content: data.data.data.answer,
          isLoading: false
        }]
      })
    } catch (error) {
      console.error('Error fetching response:', error)
      setMessages(prev => {
        const newMessages = [...prev]
        // Remove the loading message
        newMessages.pop()
        // Add error message
        return [...newMessages, {
          role: 'assistant',
          content: 'Sorry, I encountered an error while processing your request. Please try again later.',
          error: error instanceof Error ? error.message : 'Unknown error',
          isLoading: false
        }]
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  // Custom renderers for ReactMarkdown to handle code blocks and tables
  const renderers = {
    parseTable(markdown: string) {
      const lines = markdown.split('\n').filter(line => line.trim() !== '');
      if (lines.length < 2) return null;
      
      const header = lines[0].split('|').map(cell => cell.trim()).filter(Boolean);
      const alignments = lines[1].split('|').map(cell => {
        const content = cell.trim();
        if (content.startsWith(':-') && content.endsWith('-:')) return 'center';
        if (content.endsWith(':')) return 'right';
        return 'left';
      }).filter(Boolean);
      
      const rows = lines.slice(2).map(line => 
        line.split('|').map(cell => cell.trim()).filter(Boolean)
      );
      
      return { header, alignments, rows };
    },
    code({ node, inline, className, children, ...props }: any) {
      const match = /language-(\w+)/.exec(className || '')
      return !inline ? (
        <div className="bg-gray-800 rounded-md p-4 my-2 overflow-x-auto">
          <SyntaxHighlighter
            style={oneDark}
            language={match ? match[1] : 'text'}
            PreTag="div"
            {...props}
            customStyle={{
              margin: 0,
              backgroundColor: 'transparent',
              fontSize: '0.9em'
            }}
          >
            {String(children).replace(/\n$/, '')}
          </SyntaxHighlighter>
        </div>
      ) : (
        <code className="bg-gray-100 px-1.5 py-0.5 rounded text-sm font-mono text-red-600">
          {children}
        </code>
      )
    },
    table({ node, children }: any) {
      // Handle both markdown and HTML table formats
      if (node?.children?.[0]?.type === 'paragraph') {
        const tableContent = node.children[0].children[0]?.value || '';
        const tableData = renderers.parseTable(tableContent);
        
        if (!tableData) return <div className="my-4">{children}</div>;
        
        return (
          <div className="overflow-x-auto my-6 rounded-lg border border-gray-200 shadow-sm">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  {tableData.header.map((cell, i) => (
                    <th 
                      key={i}
                      className={`px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap ${
                        tableData.alignments[i] === 'right' ? 'text-right' : 
                        tableData.alignments[i] === 'center' ? 'text-center' : ''
                      }`}
                    >
                      {cell}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {tableData.rows.map((row, rowIndex) => (
                  <tr key={rowIndex} className="hover:bg-gray-50 transition-colors">
                    {row.map((cell, cellIndex) => (
                      <td 
                        key={cellIndex}
                        className={`px-6 py-4 text-sm text-gray-800 ${
                          tableData.alignments[cellIndex] === 'right' ? 'text-right' : 
                          tableData.alignments[cellIndex] === 'center' ? 'text-center' : ''
                        }`}
                      >
                        <div className="prose prose-sm max-w-none">
                          <ReactMarkdown components={{
                            ...renderers,
                            // Disable nested tables to prevent infinite recursion
                            table: ({ children }) => <div className="inline-block">{children}</div>,
                            thead: ({ children }) => <thead>{children}</thead>,
                            tbody: ({ children }) => <tbody>{children}</tbody>,
                            tr: ({ children }) => <tr>{children}</tr>,
                            th: ({ children }) => <th>{children}</th>,
                            td: ({ children }) => <td>{children}</td>,
                          }}>
                            {cell}
                          </ReactMarkdown>
                        </div>
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );
      }
      
      // Default table rendering for HTML tables
      return (
        <div className="overflow-x-auto my-6 rounded-lg border border-gray-200 shadow-sm">
          <table className="min-w-full divide-y divide-gray-200">
            {children}
          </table>
        </div>
      );
    },
    thead({ children }: any) {
      return (
        <thead className="bg-gray-50">
          <tr>
            {children}
          </tr>
        </thead>
      )
    },
    tbody({ children }: any) {
      return (
        <tbody className="bg-white divide-y divide-gray-200">
          {children}
        </tbody>
      )
    },
    tr({ children, isHeaderRow }: any) {
      return (
        <tr className="hover:bg-gray-50 transition-colors">
          {children}
        </tr>
      )
    },
    th({ children, isHeaderRow }: any) {
      return (
        <th 
          scope="col" 
          className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
        >
          {children}
        </th>
      )
    },
    td({ children, isHeaderRow }: any) {
      return (
        <td className="px-6 py-4 text-sm text-gray-800 align-top">
          <div className="prose prose-sm max-w-none">
            {children}
          </div>
        </td>
      )
    },
    p({ children }: any) {
      return <p className="my-3 leading-relaxed">{children}</p>
    },
    h1({ children }: any) {
      return <h1 className="text-2xl font-bold my-4">{children}</h1>
    },
    h2({ children }: any) {
      return <h2 className="text-xl font-semibold my-3">{children}</h2>
    },
    h3({ children }: any) {
      return <h3 className="text-lg font-medium my-2">{children}</h3>
    },
    ul({ children }: any) {
      return <ul className="list-disc pl-6 my-3 space-y-1">{children}</ul>
    },
    ol({ children }: any) {
      return <ol className="list-decimal pl-6 my-3 space-y-1">{children}</ol>
    },
    li({ children }: any) {
      return <li className="my-1">{children}</li>
    },
    strong({ children }: any) {
      return <strong className="font-semibold">{children}</strong>
    },
    em({ children }: any) {
      return <em className="italic">{children}</em>
    },
    blockquote({ children }: any) {
      return <blockquote className="border-l-4 border-gray-300 pl-4 my-3 text-gray-600">{children}</blockquote>
    },
    hr() {
      return <hr className="my-4 border-t border-gray-200" />
    },
    a({ href, children }: any) {
      return (
        <a 
          href={href} 
          className="text-blue-600 hover:text-blue-800 hover:underline"
          target="_blank"
          rel="noopener noreferrer"
        >
          {children}
        </a>
      )
    }
  }

  return (
    <div className="flex h-screen bg-gray-100 overflow-hidden">
      {/* Left Sidebar - Removed for simplicity */}
      
      {/* Main Chat Area */}
      <div className="flex-1 p-6 flex flex-col w-full">
        <div className="flex items-start justify-between mb-4">
          <h1 className="text-7xl font-serif">KolamGPT</h1>
          <p className="text-xs max-w-sm text-right font-sans leading-relaxed">
            A sophisticated Retrieval-Augmented Generation (RAG) system specifically designed for Kolam-related queries.
            This system supports both Tamil and English queries with domain-specific optimizations for traditional Tamil
            floor art documentation.
          </p>
        </div>

        <div className="flex-1 overflow-y-auto mb-4 space-y-4">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`p-4 rounded-2xl max-w-3xl ${msg.role === 'user' ? 'ml-auto bg-[#1B596F] text-white' : 'bg-gray-100 text-gray-800'}`}
            >
              {msg.isLoading ? (
                <div className="flex space-x-2">
                  <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce" style={{ animationDelay: '0ms' }}></div>
                  <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce" style={{ animationDelay: '150ms' }}></div>
                  <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
              ) : msg.error ? (
                <div className="text-red-500">
                  <p>{msg.content}</p>
                  <p className="text-xs mt-1">Error: {msg.error}</p>
                </div>
              ) : (
                <div className="prose max-w-none">
                  <ReactMarkdown components={renderers}>
                    {msg.content}
                  </ReactMarkdown>
                </div>
              )}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        <div className="mt-auto">
          <div className="flex items-center gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              className="flex-1 p-3 focus:outline-none font-sans text-sm border-2 border-[#1B596F] rounded-full"
              placeholder="Ask me anything about Kolam art..."
              disabled={isLoading}
            />
            <Button
              onClick={sendMessage}
              disabled={isLoading || !input.trim()}
              className="px-6 py-3 text-white hover:opacity-90 text-sm rounded-full"
              style={{ backgroundColor: "#1B596F" }}
            >
              {isLoading ? 'Sending...' : 'Send'}
            </Button>
          </div>
          <p className="text-xs text-gray-500 mt-2 text-center">
            KolamGPT can help with patterns, techniques, history, and more about Kolam art
          </p>
        </div>
      </div>
    </div>
  )
}
