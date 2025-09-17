"use client"

import Image from "next/image"
import { useEffect, useState } from "react"

export function HeroSection() {
  const [scrollY, setScrollY] = useState(0)

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY)
    window.addEventListener("scroll", handleScroll)
    return () => window.removeEventListener("scroll", handleScroll)
  }, [])

  return (
    <section className="flex items-center justify-center min-h-screen px-6 py-12 mt-20">
      <div className="relative w-full max-w-5xl h-[600px] rounded-3xl overflow-hidden shadow-2xl">
        {/* Background Image */}
        <div className="absolute inset-0 z-0">
          <Image
            src="/images/hero-background.png"
            alt="Traditional Indian temple scene with palm trees and kolam art"
            fill
            className="object-cover transition-transform duration-75 ease-out"
            style={{
              transform: `translateY(${scrollY * 0.3}px) scale(${1 + scrollY * 0.0003})`,
            }}
            priority
          />
          <div
            className="absolute inset-0 bg-black transition-opacity duration-75 ease-out"
            style={{
              opacity: Math.min(0.15 + scrollY * 0.0008, 0.4),
            }}
          />
        </div>

        {/* Hero Content */}
        <div className="relative z-10 text-center px-6 h-full flex flex-col items-center justify-center">
          <div
            className="mb-8 transition-transform duration-75 ease-out"
            style={{
              transform: `translateY(${scrollY * -0.2}px)`,
            }}
          >
            
            <p className="text-sm md:text-base text-white/70 font-light text-balance">
              கோலம் • Kolam 
            </p>
          </div>

          <h1
            className="text-5xl md:text-6xl lg:text-7xl font-serif text-white mb-6 leading-tight transition-transform duration-75 ease-out"
            style={{
              transform: `translateY(${scrollY * -0.15}px)`,
            }}
          >
            <span className="block text-balance">Preserve Indian</span>
            <span className="block text-balance italic font-normal">Art</span>
            <span className="block text-balance">Tradition</span>
          </h1>

          <div
            className="mb-8 transition-transform duration-75 ease-out"
            style={{
              transform: `translateY(${scrollY * -0.1}px)`,
            }}
          >
            
          </div>

          {/* Decorative underline */}
          <div
            className="w-32 h-1 bg-white mx-auto mt-8 transition-all duration-75 ease-out"
            style={{
              width: `${Math.min(128 + scrollY * 0.08, 180)}px`,
              transform: `translateY(${scrollY * -0.12}px)`,
            }}
          />
        </div>
      </div>
    </section>
  )
}
