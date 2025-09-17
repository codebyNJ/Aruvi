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
    <section className="flex items-center justify-center min-h-screen px-6 pt-32 pb-12">
      <div className="relative w-full max-w-6xl h-[700px] rounded-3xl overflow-hidden shadow-2xl">
        {/* Background Image */}
        <div className="absolute inset-0 z-0">
          <Image
            src="/images/hero-background.png"
            alt="Traditional Indian temple scene with palm trees and kolam art"
            fill
            className="object-cover object-center transition-transform duration-75 ease-out"
            style={{
              transform: `translateY(calc(${scrollY * 0.2}px - 10%)) scale(${1 + scrollY * 0.0002})`,
            }}
            priority
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 100vw, 100vw"
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
            <p className="text-base md:text-lg text-white/70 font-light text-balance">
              கோலம் • Kolam 
            </p>
          </div>

          <h1
            className="text-6xl md:text-7xl lg:text-8xl text-white mb-6 leading-tight transition-transform duration-75 ease-out px-4"
            style={{
              transform: `translateY(${scrollY * -0.15}px)`,
            }}
          >
            <div className="font-['ThatThatNewPixel']">
              Preserve Indian<span className="italic">Art</span>
            </div>
            <div className="font-sans text-right text-5xl md:text-6xl lg:text-7xl mt-4">Tradition</div>
          </h1>

          <div
            className="mb-8 transition-transform duration-75 ease-out"
            style={{
              transform: `translateY(${scrollY * -0.1}px)`,
            }}
          >
            
          </div>

          
        </div>
      </div>
    </section>
  )
}
