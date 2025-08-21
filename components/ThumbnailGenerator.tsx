import { useState, useRef } from 'react'
import { Download, Wand2, Key, ExternalLink } from 'lucide-react'
import html2canvas from 'html2canvas'

interface ThumbnailData {
  id: string
  title: string
  subtitle?: string
  background: string
  textColor: string
  accentColor: string
  visualElements?: string
  emotion?: string
  clickBait?: string
}

interface ThumbnailGeneratorProps {
  apiKey: string
}

export default function ThumbnailGenerator({ apiKey }: ThumbnailGeneratorProps) {
  const [title, setTitle] = useState('')
  const [keywords, setKeywords] = useState('')
  const [thumbnails, setThumbnails] = useState<ThumbnailData[]>([])
  const [loading, setLoading] = useState(false)
  const [selectedThumbnail, setSelectedThumbnail] = useState<string | null>(null)
  const thumbnailRefs = useRef<{ [key: string]: HTMLDivElement | null }>({})

  const generateThumbnails = async () => {
    if (!title.trim() || !keywords.trim() || !apiKey.trim()) {
      alert('제목, 키워드, API 키를 모두 입력해주세요.')
      return
    }

    setLoading(true)
    try {
      const response = await fetch('/api/generate-thumbnails', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title,
          keywords,
          apiKey,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        console.error('API Error:', data)
        throw new Error(data.details || data.error || '썸네일 생성에 실패했습니다.')
      }

      if (!data.thumbnails || !Array.isArray(data.thumbnails)) {
        throw new Error('잘못된 응답 형식입니다.')
      }

      setThumbnails(data.thumbnails)
    } catch (error) {
      console.error('Error:', error)
      const errorMessage = error instanceof Error ? error.message : '알 수 없는 오류가 발생했습니다.'
      
      if (errorMessage.includes('API') || errorMessage.includes('key')) {
        alert('API 키를 확인해주세요. Google Gemini API 키가 올바르지 않거나 만료되었을 수 있습니다.')
      } else {
        alert(`썸네일 생성 중 오류가 발생했습니다: ${errorMessage}`)
      }
    } finally {
      setLoading(false)
    }
  }

  const downloadThumbnail = async (thumbnailId: string) => {
    const element = thumbnailRefs.current[thumbnailId]
    if (!element) return

    try {
      const canvas = await html2canvas(element, {
        backgroundColor: null,
        scale: 2,
        width: 1280,
        height: 720,
      })

      const link = document.createElement('a')
      link.download = `thumbnail-${thumbnailId}.png`
      link.href = canvas.toDataURL()
      link.click()
    } catch (error) {
      console.error('Download error:', error)
      alert('다운로드 중 오류가 발생했습니다.')
    }
  }

  return (
    <div className="w-full max-w-4xl mx-auto">
      <div className="card mb-8">
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium mb-2">영상 제목</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="예: 유튜브 조회수 늘리는 방법"
              className="input-field w-full"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">키워드</label>
            <input
              type="text"
              value={keywords}
              onChange={(e) => setKeywords(e.target.value)}
              placeholder="예: 유튜브, 조회수, 마케팅"
              className="input-field w-full"
            />
          </div>

          <button
            onClick={generateThumbnails}
            disabled={loading}
            className="btn-primary w-full flex items-center justify-center gap-2"
          >
            <Wand2 size={20} />
            {loading ? '생성 중...' : '썸네일 생성하기'}
          </button>
        </div>
      </div>

      {thumbnails.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {thumbnails.map((thumbnail) => (
            <div key={thumbnail.id} className="card">
              <div
                ref={(el) => {
                  thumbnailRefs.current[thumbnail.id] = el
                }}
                className="relative aspect-video rounded-lg overflow-hidden mb-4 cursor-pointer transition-transform hover:scale-105"
                style={{ 
                  background: thumbnail.background.includes('gradient') 
                    ? thumbnail.background 
                    : thumbnail.background,
                  boxShadow: selectedThumbnail === thumbnail.id 
                    ? '0 0 20px rgba(255, 107, 107, 0.5)' 
                    : '0 4px 12px rgba(0, 0, 0, 0.3)'
                }}
                onClick={() => setSelectedThumbnail(thumbnail.id)}
              >
                <div className="absolute inset-0 flex flex-col justify-center items-center p-4 text-center">
                  <h3
                    className="text-2xl md:text-4xl font-black mb-2 leading-tight"
                    style={{ 
                      color: thumbnail.textColor,
                      textShadow: '2px 2px 4px rgba(0,0,0,0.8)',
                      fontFamily: 'system-ui, -apple-system, sans-serif'
                    }}
                  >
                    {thumbnail.title}
                  </h3>
                  {thumbnail.subtitle && (
                    <p
                      className="text-sm md:text-xl font-bold px-3 py-1 rounded-full"
                      style={{ 
                        color: thumbnail.accentColor,
                        backgroundColor: thumbnail.textColor + '20',
                        textShadow: '1px 1px 2px rgba(0,0,0,0.6)'
                      }}
                    >
                      {thumbnail.subtitle}
                    </p>
                  )}
                </div>
                
                {/* 유튜브 스타일 재생 버튼 */}
                <div className="absolute bottom-4 right-4 w-12 h-8 bg-red-600 rounded flex items-center justify-center">
                  <div className="w-0 h-0 border-l-[8px] border-l-white border-t-[4px] border-t-transparent border-b-[4px] border-b-transparent ml-1"></div>
                </div>
                
                {/* 조회수 표시 */}
                <div className="absolute bottom-4 left-4 bg-black bg-opacity-70 text-white text-xs px-2 py-1 rounded">
                  조회수 1.2만회
                </div>
                
                {selectedThumbnail === thumbnail.id && (
                  <div className="absolute inset-0 bg-primary/20 border-4 border-primary rounded-lg flex items-center justify-center">
                    <div className="bg-primary text-white px-4 py-2 rounded-full font-bold">
                      선택됨 ✓
                    </div>
                  </div>
                )}
              </div>

              {/* 썸네일 정보 표시 */}
              <div className="space-y-3 mb-4">
                {thumbnail.emotion && (
                  <div className="flex items-center gap-2 text-sm">
                    <span className="text-blue-400">😊 감정:</span>
                    <span className="text-gray-300">{thumbnail.emotion}</span>
                  </div>
                )}
                {thumbnail.visualElements && (
                  <div className="flex items-center gap-2 text-sm">
                    <span className="text-green-400">🎨 디자인:</span>
                    <span className="text-gray-300">{thumbnail.visualElements}</span>
                  </div>
                )}
                {thumbnail.clickBait && (
                  <div className="flex items-center gap-2 text-sm">
                    <span className="text-yellow-400">🎯 전략:</span>
                    <span className="text-gray-300">{thumbnail.clickBait}</span>
                  </div>
                )}
              </div>

              <button
                onClick={() => downloadThumbnail(thumbnail.id)}
                className="btn-secondary w-full flex items-center justify-center gap-2"
              >
                <Download size={20} />
                PNG 다운로드
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}