"use client"

import { useEffect, useRef, useState } from "react"

export function Footer() {
  const [isVisible, setIsVisible] = useState(false)
  const footerRef = useRef<HTMLElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsVisible(true)
          }
        })
      },
      { threshold: 0.3 },
    )

    if (footerRef.current) {
      observer.observe(footerRef.current)
    }

    return () => observer.disconnect()
  }, [])

  return (
    <footer
      ref={footerRef}
      className={`bg-[#1B596F] text-white py-12 sm:py-16 px-4 sm:px-6 transition-all duration-1000 ${
        isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-20"
      }`}
    >
      <div className="max-w-6xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 sm:gap-12">
          {/* Brand Section */}
          <div
            className={`lg:col-span-2 transition-all duration-1200 delay-300 ${
              isVisible ? "opacity-100 translate-x-0" : "opacity-0 -translate-x-20"
            }`}
          >
            <div className="flex items-center mb-4 sm:mb-6">
              <div className="w-8 h-8 sm:w-10 sm:h-10 bg-white rounded-lg flex items-center justify-center mr-3 sm:mr-4">
                <div className="w-4 h-4 sm:w-5 sm:h-5 bg-[#1B596F] rounded-sm"></div>
              </div>
              <h3 className="text-2xl sm:text-3xl font-bold font-sans">
                <span className="font-inter">Vanna</span>Kodu
              </h3>
            </div>
            <p className="text-gray-300 leading-relaxed mb-6 sm:mb-8 text-sm sm:text-base max-w-md">
              Preserving the sacred art of kolam through innovative AI technology. Connecting generations, cultures, and
              communities through the timeless beauty of traditional patterns.
            </p>
            <div className="flex space-x-4 sm:space-x-6">
              <a
                href="#"
                className="text-gray-300 hover:text-white transition-colors duration-300 hover:scale-110 transform"
                aria-label="Facebook"
              >
                <svg className="w-5 h-5 sm:w-6 sm:h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
                </svg>
              </a>
              <a
                href="#"
                className="text-gray-300 hover:text-white transition-colors duration-300 hover:scale-110 transform"
                aria-label="Twitter"
              >
                <svg className="w-5 h-5 sm:w-6 sm:h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z" />
                </svg>
              </a>
              <a
                href="#"
                className="text-gray-300 hover:text-white transition-colors duration-300 hover:scale-110 transform"
                aria-label="Instagram"
              >
                <svg className="w-5 h-5 sm:w-6 sm:h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12.017 0C5.396 0 .029 5.367.029 11.987c0 6.62 5.367 11.987 11.988 11.987 6.62 0 11.987-5.367 11.987-11.987C24.014 5.367 18.637.001 12.017.001zM8.449 16.988c-1.297 0-2.448-.49-3.323-1.297C4.198 14.895 3.708 13.744 3.708 12.447s.49-2.448 1.297-3.323C5.902 8.198 7.053 7.708 8.35 7.708s2.448.49 3.323 1.297c.897.875 1.387 2.026 1.387 3.323s-.49 2.448-1.297 3.323c-.875.897-2.026 1.387-3.323 1.387zm7.718 0c-1.297 0-2.448-.49-3.323-1.297-.897-.875-1.387-2.026-1.387-3.323s.49-2.448 1.297-3.323c.875-.897 2.026-1.387 3.323-1.387s2.448.49 3.323 1.297c.897.875 1.387 2.026 1.387 3.323s-.49 2.448-1.297 3.323c-.875.897-2.026 1.387-3.323 1.387z" />
                </svg>
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div
            className={`transition-all duration-1200 delay-500 ${
              isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-20"
            }`}
          >
            <h4 className="text-lg sm:text-xl font-semibold mb-4 sm:mb-6 text-white">Quick Links</h4>
            <ul className="space-y-2 sm:space-y-3">
              <li>
                <a
                  href="#"
                  className="text-gray-300 hover:text-white transition-colors duration-300 text-sm sm:text-base hover:translate-x-1 transform inline-block"
                >
                  KolamGPT
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-gray-300 hover:text-white transition-colors duration-300 text-sm sm:text-base hover:translate-x-1 transform inline-block"
                >
                  KolamGenerator
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-gray-300 hover:text-white transition-colors duration-300 text-sm sm:text-base hover:translate-x-1 transform inline-block"
                >
                  KolamExtract
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-gray-300 hover:text-white transition-colors duration-300 text-sm sm:text-base hover:translate-x-1 transform inline-block"
                >
                  Community
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-gray-300 hover:text-white transition-colors duration-300 text-sm sm:text-base hover:translate-x-1 transform inline-block"
                >
                  Gallery
                </a>
              </li>
            </ul>
          </div>

          {/* Support */}
          <div
            className={`transition-all duration-1200 delay-700 ${
              isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-20"
            }`}
          >
            <h4 className="text-lg sm:text-xl font-semibold mb-4 sm:mb-6 text-white">Support</h4>
            <ul className="space-y-2 sm:space-y-3">
              <li>
                <a
                  href="#"
                  className="text-gray-300 hover:text-white transition-colors duration-300 text-sm sm:text-base hover:translate-x-1 transform inline-block"
                >
                  Help Center
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-gray-300 hover:text-white transition-colors duration-300 text-sm sm:text-base hover:translate-x-1 transform inline-block"
                >
                  Tutorials
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-gray-300 hover:text-white transition-colors duration-300 text-sm sm:text-base hover:translate-x-1 transform inline-block"
                >
                  Contact Us
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-gray-300 hover:text-white transition-colors duration-300 text-sm sm:text-base hover:translate-x-1 transform inline-block"
                >
                  Privacy Policy
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-gray-300 hover:text-white transition-colors duration-300 text-sm sm:text-base hover:translate-x-1 transform inline-block"
                >
                  Terms of Service
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Section */}
        <div
          className={`border-t border-gray-600 mt-8 sm:mt-12 pt-6 sm:pt-8 flex flex-col sm:flex-row justify-between items-center transition-all duration-1200 delay-900 ${
            isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"
          }`}
        >
          <p className="text-gray-400 text-xs sm:text-sm mb-4 sm:mb-0 text-center sm:text-left">
            © 2024 VannaKodu. All rights reserved. Preserving culture through innovation.
          </p>
          <div className="flex items-center space-x-4 sm:space-x-6">
            <span className="text-gray-400 text-xs sm:text-sm">Made with</span>
            <div className="w-4 h-4 bg-red-500 rounded-full animate-pulse"></div>
            <span className="text-gray-400 text-xs sm:text-sm">for cultural preservation</span>
          </div>
        </div>
      </div>
    </footer>
  )
}
