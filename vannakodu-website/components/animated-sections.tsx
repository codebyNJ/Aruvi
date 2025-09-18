"use client"

import { useEffect, useRef, useState } from "react"

export function AnimatedSections() {
  const [isVisible, setIsVisible] = useState({
    section1: false,
    section2: false,
    section3: false,
  })

  const section1Ref = useRef<HTMLElement>(null)
  const section2Ref = useRef<HTMLElement>(null)
  const section3Ref = useRef<HTMLElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const sectionId = entry.target.getAttribute("data-section")
            if (sectionId) {
              setIsVisible((prev) => ({ ...prev, [sectionId]: true }))
            }
          }
        })
      },
      { threshold: 0.3 },
    )

    const sections = [section1Ref.current, section2Ref.current, section3Ref.current]
    sections.forEach((section) => {
      if (section) observer.observe(section)
    })

    return () => observer.disconnect()
  }, [])

  return (
    <>
      {/* Section 1 - Heritage & Culture */}
      <section
        ref={section1Ref}
        data-section="section1"
        className={`min-h-screen flex items-center justify-center px-4 sm:px-6 py-12 sm:py-20 transition-all duration-1000 ${
          isVisible.section1 ? "opacity-100 translate-y-0" : "opacity-0 translate-y-20"
        }`}
      >
        <div className="max-w-4xl text-center">
          <h2
            className={`text-4xl sm:text-6xl lg:text-8xl font-serif text-[#1B596F] mb-6 sm:mb-8 transition-all duration-1200 delay-300 hover:scale-105 hover:text-[#0f3d4a] cursor-default ${
              isVisible.section1 ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"
            }`}
          >
            Heritage
          </h2>
          <div
            className={`w-20 sm:w-32 h-1 bg-[#1B596F] mx-auto mb-8 sm:mb-12 transition-all duration-800 delay-500 hover:bg-[#0f3d4a] hover:h-2 ${
              isVisible.section1 ? "scale-x-100" : "scale-x-0"
            }`}
          />
          <p
            className={`text-lg sm:text-xl lg:text-2xl text-gray-700 leading-relaxed mb-6 sm:mb-8 transition-all duration-1000 delay-700 hover:text-gray-900 px-2 ${
              isVisible.section1 ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"
            }`}
          >
            Every kolam tells a story of generations past, where sacred geometry meets artistic expression. These
            intricate patterns, drawn at dawn, connect us to our ancestors and preserve the wisdom of ancient
            traditions.
          </p>
          <p
            className={`text-base sm:text-lg text-gray-600 leading-relaxed transition-all duration-1000 delay-900 hover:text-gray-800 px-2 ${
              isVisible.section1 ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"
            }`}
          >
            Through Aruvi, we ensure these timeless art forms continue to flourish in the digital age.
          </p>
        </div>
      </section>

      {/* Section 2 - Innovation & Technology */}
      <section
        ref={section2Ref}
        data-section="section2"
        className={`min-h-screen flex items-center justify-center px-4 sm:px-6 py-12 sm:py-20 bg-gradient-to-br from-slate-50 to-blue-50 transition-all duration-1000 ${
          isVisible.section2 ? "opacity-100 translate-y-0" : "opacity-0 translate-y-20"
        }`}
      >
        <div className="max-w-5xl w-full">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-16 items-center">
            <div
              className={`transition-all duration-1200 delay-300 text-center lg:text-left ${
                isVisible.section2 ? "opacity-100 translate-x-0" : "opacity-0 -translate-x-20"
              }`}
            >
              <h2 className="text-3xl sm:text-5xl lg:text-7xl font-serif text-[#1B596F] mb-4 sm:mb-6 transition-all duration-300 hover:scale-105 hover:text-[#0f3d4a] cursor-default">
                Innovation
              </h2>
              <div className="w-16 sm:w-24 h-1 bg-[#1B596F] mb-6 sm:mb-8 mx-auto lg:mx-0 transition-all duration-300 hover:bg-[#0f3d4a] hover:h-2" />
              <p className="text-base sm:text-xl text-gray-700 leading-relaxed hover:text-gray-900 transition-colors duration-300">
                Where ancient wisdom meets cutting-edge technology. Our AI-powered tools understand the sacred
                mathematics behind traditional patterns, enabling creators to explore infinite possibilities while
                honoring cultural authenticity.
              </p>
            </div>
            <div
              className={`text-center lg:text-right transition-all duration-1200 delay-600 ${
                isVisible.section2 ? "opacity-100 translate-x-0" : "opacity-0 translate-x-20"
              }`}
            >
              <p className="text-4xl sm:text-6xl lg:text-8xl font-serif text-[#1B596F]/20 mb-2 sm:mb-4 transition-all duration-300 hover:text-[#1B596F]/40 hover:scale-110 cursor-default">
                Mathematics
              </p>
              <p className="text-sm sm:text-lg text-gray-600 leading-relaxed hover:text-gray-800 transition-colors duration-300 px-2 lg:px-0">
                Empowering artists, preserving culture, and inspiring the next generation of traditional art enthusiasts
                through intelligent design tools.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Section 3 - Community & Future */}
      <section
        ref={section3Ref}
        data-section="section3"
        className={`min-h-screen flex items-center justify-center px-4 sm:px-6 py-12 sm:py-20 transition-all duration-1000 ${
          isVisible.section3 ? "opacity-100 translate-y-0" : "opacity-0 translate-y-20"
        }`}
      >
        <div className="max-w-6xl text-center w-full">
          <div
            className={`transition-all duration-1200 delay-300 ${
              isVisible.section3 ? "opacity-100 scale-100" : "opacity-0 scale-95"
            }`}
          >
            <h2 className="text-2xl sm:text-4xl lg:text-6xl font-serif text-[#1B596F] mb-8 sm:mb-12 transition-all duration-300 hover:scale-105 hover:text-[#0f3d4a] cursor-default">
              Building Tomorrow's
              <span className="block text-3xl sm:text-5xl lg:text-7xl mt-1 sm:mt-2 hover:scale-105 transition-transform duration-300">
                Cultural Bridge
              </span>
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 sm:gap-12 mt-12 sm:mt-16">
            <div
              className={`transition-all duration-1000 delay-500 hover:transform hover:scale-105 hover:bg-white hover:shadow-lg hover:rounded-lg p-4 sm:p-6 cursor-pointer group ${
                isVisible.section3 ? "opacity-100 translate-y-0" : "opacity-0 translate-y-20"
              }`}
            >
              <h3 className="text-xl sm:text-2xl font-serif text-[#1B596F] mb-3 sm:mb-4 group-hover:text-[#0f3d4a] transition-colors duration-300">
                Create
              </h3>
              <p className="text-sm sm:text-base text-gray-700 leading-relaxed group-hover:text-gray-900 transition-colors duration-300">
                Generate authentic kolam patterns with AI assistance, exploring traditional motifs and contemporary
                interpretations.
              </p>
            </div>

            <div
              className={`transition-all duration-1000 delay-700 hover:transform hover:scale-105 hover:bg-white hover:shadow-lg hover:rounded-lg p-4 sm:p-6 cursor-pointer group ${
                isVisible.section3 ? "opacity-100 translate-y-0" : "opacity-0 translate-y-20"
              }`}
            >
              <h3 className="text-xl sm:text-2xl font-serif text-[#1B596F] mb-3 sm:mb-4 group-hover:text-[#0f3d4a] transition-colors duration-300">
                Learn
              </h3>
              <p className="text-sm sm:text-base text-gray-700 leading-relaxed group-hover:text-gray-900 transition-colors duration-300">
                Discover the rich history and symbolic meanings behind each pattern, connecting with centuries of
                cultural wisdom.
              </p>
            </div>

            <div
              className={`transition-all duration-1000 delay-900 hover:transform hover:scale-105 hover:bg-white hover:shadow-lg hover:rounded-lg p-4 sm:p-6 cursor-pointer group ${
                isVisible.section3 ? "opacity-100 translate-y-0" : "opacity-0 translate-y-20"
              }`}
            >
              <h3 className="text-xl sm:text-2xl font-serif text-[#1B596F] mb-3 sm:mb-4 group-hover:text-[#0f3d4a] transition-colors duration-300">
                Share
              </h3>
              <p className="text-sm sm:text-base text-gray-700 leading-relaxed group-hover:text-gray-900 transition-colors duration-300">
                Join a global community of artists and culture enthusiasts, sharing creations and preserving traditions
                for future generations.
              </p>
            </div>
          </div>

          <div
            className={`mt-12 sm:mt-16 transition-all duration-1200 delay-1100 ${
              isVisible.section3 ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"
            }`}
          >
            <p className="text-base sm:text-xl text-gray-600 leading-relaxed max-w-3xl mx-auto hover:text-gray-800 transition-colors duration-300 px-2">
              Every pattern created, every tradition shared, every connection made contributes to a living tapestry of
              cultural preservation and innovation.
            </p>
          </div>
        </div>
      </section>
    </>
  )
}
