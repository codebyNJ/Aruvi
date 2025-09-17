"use client"

import Image from "next/image"
import { Button } from "@/components/ui/button"
import { useEffect, useState } from "react"
import { AuthModal } from "./auth-modal"

export function Header() {
  const [isScrolled, setIsScrolled] = useState(false)
  const [activeTab, setActiveTab] = useState<"login" | "signup">("signup")
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [modalMode, setModalMode] = useState<"login" | "signup">("login")

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50)
    }

    window.addEventListener("scroll", handleScroll)
    return () => window.removeEventListener("scroll", handleScroll)
  }, [])

  const handleAuthClick = (mode: "login" | "signup") => {
    setModalMode(mode)
    setIsModalOpen(true)
  }

  return (
    <>
      <header
        className={`w-full transition-all duration-300 ease-out ${
          isScrolled
            ? "fixed top-2 left-1/2 transform -translate-x-1/2 z-50 max-w-5xl bg-white/95 backdrop-blur-md rounded-full border border-gray-200 shadow-lg"
            : "absolute top-0 left-0 z-40 bg-transparent mt-6 max-w-full"
        }`}
      >
        <div className={`mx-auto px-6 transition-all duration-300 ${isScrolled ? "py-2" : "py-4"}`}>
          <div className="flex items-center justify-between">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <Image 
                src="/images/logo.png" 
                alt="VannaKodu Logo" 
                width={isScrolled ? 32 : 40} 
                height={isScrolled ? 32 : 40} 
                className={`transition-all duration-300 ${isScrolled ? "w-8 h-8" : "w-10 h-10"}`} 
              />
              <span className={`transition-all duration-300 ${isScrolled ? "text-xl" : "text-2xl"} ${isScrolled ? "text-gray-800" : "text-[#1B596F]"}`}>
                <span className="font-sans font-medium">Vanna</span>
                <span className="font-serif font-normal italic">Kodu</span>
              </span>
            </div>

            {/* Navigation */}
            <nav className="hidden md:flex items-center gap-6">
              <a
                href="#"
                className={`font-medium transition-all duration-300 ${isScrolled ? "text-sm" : "text-base"} ${
                  isScrolled ? "text-gray-600 hover:text-gray-900" : "text-[#1B596F] hover:text-[#164d5f]"
                }`}
              >
                KolamGPT
              </a>
              <a
                href="#"
                className={`font-medium transition-all duration-300 ${isScrolled ? "text-sm" : "text-base"} ${
                  isScrolled ? "text-gray-600 hover:text-gray-900" : "text-[#1B596F] hover:text-[#164d5f]"
                }`}
              >
                KolamGenerator
              </a>
              <a
                href="#"
                className={`font-medium transition-all duration-300 ${isScrolled ? "text-sm" : "text-base"} ${
                  isScrolled ? "text-gray-600 hover:text-gray-900" : "text-[#1B596F] hover:text-[#164d5f]"
                }`}
              >
                KolamExtract
              </a>
            </nav>

            <div className="flex items-center">
              <div className={`flex bg-white rounded-full border border-gray-200 relative overflow-hidden transition-all duration-300 ${isScrolled ? "p-0.5 scale-90" : "p-1"}`}>
                {/* Background slider for smooth transition */}
                <div
                  className={`absolute bg-[#1B596F] rounded-full transition-all duration-300 ease-out ${isScrolled ? "top-0.5 bottom-0.5" : "top-1 bottom-1"} ${
                    activeTab === "login" ? "left-0.5 right-[50%]" : "left-[50%] right-0.5"
                  }`}
                />

                <Button
                  variant="ghost"
                  onClick={() => {
                    setActiveTab("login")
                    handleAuthClick("login")
                  }}
                  className={`font-serif relative z-10 rounded-full border-0 transition-all duration-300 ease-out ${isScrolled ? "px-4 py-1.5 text-sm" : "px-6 py-2"} ${
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
                  className={`font-serif relative z-10 rounded-full border-0 transition-all duration-300 ease-out ${isScrolled ? "px-4 py-1.5 text-sm" : "px-6 py-2"} ${
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
