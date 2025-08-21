import { useState } from 'react'
import Head from 'next/head'
import Image from 'next/image'
import { Key, ExternalLink, Youtube, Sparkles } from 'lucide-react'
import ThumbnailGenerator from '@/components/ThumbnailGenerator'
import AdBanner from '@/components/AdBanner'

export default function Home() {
  const [apiKey, setApiKey] = useState('AIzaSyDBe0JCBmlce0jVlhyXpp08pXiLbW9G7bw')
  const [showApiInput, setShowApiInput] = useState(false)

  const openApiGuide = () => {
    window.open('https://console.cloud.google.com/apis/credentials', '_blank')
  }

  return (
    <>
      <Head>
        <title>썸네일 자동 생성기 - AI로 만드는 유튜브 썸네일</title>
        <meta name="description" content="유튜브 영상 제목과 키워드만 입력하면 AI가 자동으로 3-5개의 썸네일을 생성해드립니다. 무료로 PNG 다운로드 가능!" />
        <meta name="keywords" content="유튜브, 썸네일, 자동생성, AI, 썸네일메이커, 유튜브썸네일" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        
        {/* Open Graph */}
        <meta property="og:title" content="썸네일 자동 생성기 - AI로 만드는 유튜브 썸네일" />
        <meta property="og:description" content="유튜브 영상 제목과 키워드만 입력하면 AI가 자동으로 3-5개의 썸네일을 생성해드립니다." />
        <meta property="og:type" content="website" />
        <meta property="og:image" content="/logo.png" />
        
        {/* Twitter Card */}
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="썸네일 자동 생성기" />
        <meta name="twitter:description" content="AI로 만드는 유튜브 썸네일" />
        <meta name="twitter:image" content="/logo.png" />
      </Head>

      <div className="min-h-screen bg-dark">
        {/* Left Sidebar Ad */}
        <div className="fixed left-0 top-0 h-full w-32 hidden xl:block">
          <div className="sticky top-20">
            <AdBanner
              slot="auto"
              className="h-96"
              style={{ width: '120px' }}
            />
          </div>
        </div>

        {/* Right Sidebar Ad */}
        <div className="fixed right-0 top-0 h-full w-32 hidden xl:block">
          <div className="sticky top-20">
            <AdBanner
              slot="auto"
              className="h-96"
              style={{ width: '120px' }}
            />
          </div>
        </div>

        {/* Main Content */}
        <div className="xl:mx-32">
          {/* Header */}
          <header className="border-b border-gray-700">
            <div className="container mx-auto px-4 py-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-6">
                  <Image
                    src="/logo.png"
                    alt="Logo"
                    width={80}
                    height={80}
                    className="rounded-lg"
                  />
                  <div>
                    <h1 className="text-3xl md:text-4xl font-bold text-white">썸네일 자동 생성기</h1>
                    <p className="text-gray-400 text-base md:text-lg">AI로 만드는 유튜브 썸네일</p>
                  </div>
                </div>
                
                <button
                  onClick={openApiGuide}
                  className="btn-secondary flex items-center gap-2"
                >
                  <Key size={20} />
                  API 키 발급 가이드
                  <ExternalLink size={16} />
                </button>
              </div>
            </div>

          </header>

          {/* Hero Section */}
          <section className="container mx-auto px-4 py-12 text-center">
            <div className="max-w-3xl mx-auto">
              <div className="flex items-center justify-center gap-2 mb-4">
                <Youtube className="text-red-500" size={48} />
                <Sparkles className="text-yellow-400" size={32} />
              </div>
              
              <h2 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                AI가 만드는 완벽한 썸네일
              </h2>
              
              <p className="text-xl text-gray-300 mb-8">
                영상 제목과 키워드만 입력하면 <br />
                <span className="text-primary font-semibold">3-5개의 썸네일</span>을 자동으로 생성해드립니다
              </p>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="card text-center">
                  <div className="text-primary mb-3">📝</div>
                  <h3 className="font-semibold mb-2">간단한 입력</h3>
                  <p className="text-gray-400 text-sm">제목과 키워드만 입력하세요</p>
                </div>
                
                <div className="card text-center">
                  <div className="text-secondary mb-3">🤖</div>
                  <h3 className="font-semibold mb-2">AI 자동 생성</h3>
                  <p className="text-gray-400 text-sm">Google Gemini가 최적화된 썸네일 생성</p>
                </div>
                
                <div className="card text-center">
                  <div className="text-yellow-400 mb-3">⬇️</div>
                  <h3 className="font-semibold mb-2">무료 다운로드</h3>
                  <p className="text-gray-400 text-sm">PNG 파일로 즉시 다운로드</p>
                </div>
              </div>
            </div>
          </section>

          {/* API Key Section */}
          <section className="container mx-auto px-4 mb-8">
            <div className="max-w-2xl mx-auto">
              <div className="card">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold">Google Gemini API 키</h3>
                  <button
                    onClick={() => setShowApiInput(!showApiInput)}
                    className="text-primary hover:text-primary/80 text-sm"
                  >
                    {showApiInput ? '숨기기' : '수정하기'}
                  </button>
                </div>
                
                {showApiInput ? (
                  <div className="space-y-4">
                    <input
                      type="password"
                      value={apiKey}
                      onChange={(e) => setApiKey(e.target.value)}
                      placeholder="Google Gemini API 키를 입력하세요"
                      className="input-field w-full"
                    />
                    <p className="text-sm text-gray-400">
                      API 키가 없으신가요? 
                      <button
                        onClick={openApiGuide}
                        className="text-primary hover:text-primary/80 ml-1"
                      >
                        발급 가이드 보기
                      </button>
                    </p>
                  </div>
                ) : (
                  <p className="text-gray-400">API 키가 설정되었습니다 ✓</p>
                )}
              </div>
            </div>
          </section>


          {/* Thumbnail Generator */}
          <section className="container mx-auto px-4 mb-12">
            <ThumbnailGenerator apiKey={apiKey} />
          </section>


          {/* Footer */}
          <footer className="border-t border-gray-700">
            <div className="container mx-auto px-4 py-8 text-center">
              <div className="flex items-center justify-center gap-2 mb-4">
                <Image
                  src="/logo.png"
                  alt="Logo"
                  width={32}
                  height={32}
                  className="rounded"
                />
                <span className="font-semibold">썸네일 자동 생성기</span>
              </div>
              
              <p className="text-gray-400 text-sm mb-4">
                AI 기술로 만드는 완벽한 유튜브 썸네일
              </p>
              
              <div className="text-xs text-gray-500">
                <p>© 2024 썸네일 자동 생성기. All rights reserved.</p>
                <p className="mt-1">Powered by Google Gemini AI</p>
              </div>
            </div>
          </footer>
        </div>
      </div>
    </>
  )
}