"use client"

import { useEffect, useRef, useState } from "react"
import { ChevronDownIcon } from "@heroicons/react/24/outline"

interface FAQItem {
  question: string
  answer: string
}

const faqData: FAQItem[] = [
  {
    question: "What is VannaKodu and how does it work?",
    answer:
      "VannaKodu is an AI-powered platform that helps you create, learn about, and share traditional kolam patterns. Our advanced algorithms understand the sacred geometry and cultural significance behind these ancient art forms, enabling both beginners and experts to explore infinite creative possibilities while maintaining cultural authenticity.",
  },
  {
    question: "Do I need artistic experience to use VannaKodu?",
    answer:
      "Not at all! VannaKodu is designed for everyone, from complete beginners to experienced artists. Our intuitive tools guide you through the process, teaching you about traditional patterns while helping you create beautiful kolams. The AI assistance makes it easy to understand the underlying principles and create authentic designs.",
  },
  {
    question: "How does the AI ensure cultural authenticity?",
    answer:
      "Our AI has been trained on thousands of traditional kolam patterns, understanding the mathematical principles, symbolic meanings, and cultural contexts. It respects traditional rules while offering creative variations, ensuring that generated patterns maintain their cultural integrity and spiritual significance.",
  },
  {
    question: "Can I share my creations with others?",
    answer:
      "VannaKodu includes a vibrant community platform where you can share your creations, learn from others, and connect with fellow kolam enthusiasts worldwide. You can also export your designs for printing or digital use, making it easy to bring your digital creations into the physical world.",
  },
  {
    question: "Is VannaKodu suitable for educational purposes?",
    answer:
      "Yes! VannaKodu is an excellent educational tool for schools, cultural centers, and anyone interested in learning about South Indian traditions. It provides historical context, explains symbolic meanings, and offers interactive lessons that make learning about kolam art engaging and accessible.",
  },
  {
    question: "What tools are included in the platform?",
    answer:
      "VannaKodu offers three main tools: KolamGPT for AI-powered pattern generation and cultural insights, KolamGenerator for creating custom designs with guided assistance, and KolamExtract for analyzing and understanding existing patterns. Each tool is designed to enhance your creative journey while preserving cultural authenticity.",
  },
]

export function FAQSection() {
  const [isVisible, setIsVisible] = useState(false)
  const [openItems, setOpenItems] = useState<number[]>([])
  const sectionRef = useRef<HTMLElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsVisible(true)
          }
        })
      },
      { threshold: 0.2 },
    )

    if (sectionRef.current) {
      observer.observe(sectionRef.current)
    }

    return () => observer.disconnect()
  }, [])

  const toggleItem = (index: number) => {
    setOpenItems((prev) => (prev.includes(index) ? prev.filter((i) => i !== index) : [...prev, index]))
  }

  return (
    <section
      ref={sectionRef}
      className={`min-h-screen flex items-center justify-center px-4 sm:px-6 py-12 sm:py-20 bg-white transition-all duration-1000 ${
        isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-20"
      }`}
    >
      <div className="max-w-4xl w-full">
        <div
          className={`text-center mb-12 sm:mb-16 transition-all duration-1200 delay-300 ${
            isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"
          }`}
        >
          <h2 className="text-4xl sm:text-6xl lg:text-7xl font-serif text-[#1B596F] mb-6 sm:mb-8 transition-all duration-300 hover:scale-105 hover:text-[#0f3d4a] cursor-default">
            Frequently Asked
            <span className="block mt-1 sm:mt-2">Questions</span>
          </h2>
          <div className="w-20 sm:w-32 h-1 bg-[#1B596F] mx-auto mb-6 sm:mb-8 transition-all duration-300 hover:bg-[#0f3d4a] hover:h-2" />
          <p className="text-lg sm:text-xl text-gray-700 leading-relaxed hover:text-gray-900 transition-colors duration-300">
            Everything you need to know about VannaKodu and traditional kolam art
          </p>
        </div>

        <div className="space-y-0">
          {faqData.map((item, index) => (
            <div
              key={index}
              className={`border-b border-gray-200 last:border-b-0 transition-all duration-1000 ${
                isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"
              }`}
              style={{ transitionDelay: `${500 + index * 100}ms` }}
            >
              <button
                onClick={() => toggleItem(index)}
                className="w-full px-0 py-6 sm:py-8 text-left flex items-center justify-between hover:bg-gray-50/50 transition-all duration-300 group"
              >
                <h3 className="text-lg sm:text-xl font-medium text-[#1B596F] pr-4 group-hover:text-[#0f3d4a] transition-colors duration-300 font-serif">
                  {item.question}
                </h3>
                <ChevronDownIcon
                  className={`w-5 h-5 sm:w-6 sm:h-6 text-[#1B596F] transition-all duration-300 group-hover:text-[#0f3d4a] flex-shrink-0 ${
                    openItems.includes(index) ? "rotate-180" : ""
                  }`}
                />
              </button>
              <div
                className={`overflow-hidden transition-all duration-500 ease-in-out ${
                  openItems.includes(index) ? "max-h-96 opacity-100 pb-6 sm:pb-8" : "max-h-0 opacity-0"
                }`}
              >
                <div className="pr-8">
                  <p className="text-gray-700 leading-relaxed text-sm sm:text-base border-l-2 border-[#1B596F]/20 pl-4">
                    {item.answer}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
