import { Header } from "@/components/header"
import { HeroSection } from "@/components/hero-section"
import { AnimatedSections } from "@/components/animated-sections"
import { FAQSection } from "@/components/faq-section"
import { Footer } from "@/components/footer"

export default function HomePage() {
  return (
    <main className="min-h-screen">
      <Header />
      <HeroSection />
      <AnimatedSections />
      <FAQSection />
      <Footer />
    </main>
  )
}
