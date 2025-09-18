"use client"

import Image from "next/image"
import { Button } from "@/components/ui/button"
import { useEffect, useState } from "react"
import { AuthModal } from "./auth-modal"
import Link from "next/link"

export function Header() {
  const [isScrolled, setIsScrolled] = useState(false)
  const [activeTab, setActiveTab] = useState<"login" | "signup">("signup")
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [modalMode, setModalMode] = useState<"login" | "signup">("login")

  useEffect(() => {
    let ticking = false

    const handleScroll = () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          setIsScrolled(window.scrollY > 30)
          ticking = false
        })
        ticking = true
      }
    }

    window.addEventListener("scroll", handleScroll, { passive: true })
    return () => window.removeEventListener("scroll", handleScroll)
  }, [])

  const handleAuthClick = (mode: "login" | "signup") => {
    setModalMode(mode)
    setIsModalOpen(true)
  }

  return (
    <>
      <header
        className={`w-full fixed top-3 left-1/2 z-50 max-w-4xl bg-white/90 backdrop-blur-xl rounded-full border border-gray-200/50 shadow-xl shadow-black/5 transition-transform duration-500 ease-out will-change-transform`}
        style={{
          transform: `translateX(-50%) scale(${isScrolled ? 0.85 : 1})`
        }}
      >
        <div className="mx-auto px-6 py-3">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <div className="flex items-center gap-2">
              <Image 
                src="/images/logo.png" 
                alt="VannaKodu Logo" 
                width={40} 
                height={40} 
                className="w-10 h-10" 
              />
              <span className="text-xl text-gray-800">
                <span className="font-sans font-medium">Aruvi</span>
              </span>
            </div>

            {/* Navigation */}
            <nav className="hidden md:flex items-center gap-6">
              <Link href="/kolam-gpt" className="font-medium text-gray-600 hover:text-gray-900">
                KolamGPT
              </Link>
              <Link href="/kolam-generator" className="font-medium text-gray-600 hover:text-gray-900">
                Kolam Generator
              </Link>
              <a href="/kolam-extract" className="font-medium text-gray-600 hover:text-gray-900">
                KolamExtract
              </a>
            </nav>

            <div className="flex items-center">
              <div className="flex bg-white rounded-full border border-gray-200 relative overflow-hidden p-1">
                {/* Background slider */}
                <div
                  className={`absolute bg-[#1B596F] rounded-full transition-all duration-300 ease-out top-1 bottom-1 ${
                    activeTab === "login" ? "left-1 right-[50%]" : "left-[50%] right-1"
                  }`}
                />

                <Button
                  variant="ghost"
                  onClick={() => {
                    setActiveTab("login")
                    handleAuthClick("login")
                  }}
                  className={`font-serif relative z-10 rounded-full border-0 px-6 py-2 transition-colors duration-300 ${
                    activeTab === "login" ? "text-white" : "text-[#1B596F] hover:text-[#164d5f]"
                  }`}
                >
                  Login
                </Button>
                <Button
                  variant="ghost"
                  onClick={() => {
                    setActiveTab("signup")
                    handleAuthClick("signup")
                  }}
                  className={`font-serif relative z-10 rounded-full border-0 px-6 py-2 transition-colors duration-300 ${
                    activeTab === "signup" ? "text-white" : "text-[#1B596F] hover:text-[#164d5f]"
                  }`}
                >
                  Sign Up
                </Button>
              </div>
            </div>
          </div>
        </div>
      </header>

      <AuthModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} mode={modalMode} />
    </>
  )
}