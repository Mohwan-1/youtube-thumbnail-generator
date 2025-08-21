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

      if (!response.ok) {
        throw new Error('썸네일 생성에 실패했습니다.')
      }

      const data = await response.json()
      setThumbnails(data.thumbnails)
    } catch (error) {
      console.error('Error:', error)
      alert('썸네일 생성 중 오류가 발생했습니다.')
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
                className="relative aspect-video rounded-lg overflow-hidden mb-4 cursor-pointer"
                style={{ backgroundColor: thumbnail.background }}
                onClick={() => setSelectedThumbnail(thumbnail.id)}
              >
                <div className="absolute inset-0 flex flex-col justify-center items-center p-6 text-center">
                  <h3
                    className="text-2xl md:text-3xl font-bold mb-2"
                    style={{ color: thumbnail.textColor }}
                  >
                    {thumbnail.title}
                  </h3>
                  {thumbnail.subtitle && (
                    <p
                      className="text-lg"
                      style={{ color: thumbnail.accentColor }}
                    >
                      {thumbnail.subtitle}
                    </p>
                  )}
                </div>
                {selectedThumbnail === thumbnail.id && (
                  <div className="absolute inset-0 bg-primary/20 border-2 border-primary rounded-lg" />
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