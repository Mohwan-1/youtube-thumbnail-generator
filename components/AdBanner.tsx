import { useEffect } from 'react'

interface AdBannerProps {
  slot?: string
  format?: string
  layout?: string
  style?: React.CSSProperties
  className?: string
  type?: 'auto' | 'manual'
}

export default function AdBanner({ 
  slot = "5964488484", 
  format = "fluid", 
  layout = "in-article",
  style,
  className = "",
  type = "manual"
}: AdBannerProps) {
  useEffect(() => {
    try {
      // AdSense 스크립트가 로드되었는지 확인
      if (typeof window !== 'undefined' && window.adsbygoogle) {
        // @ts-ignore
        (window.adsbygoogle = window.adsbygoogle || []).push({})
      }
    } catch (err) {
      console.error('AdSense error:', err)
    }
  }, [])

  if (type === 'auto') {
    // 자동 광고는 스크립트만 필요 (사이드바용)
    return <div className={`ad-container ${className}`} style={style}></div>
  }

  return (
    <div className={`ad-container ${className}`} style={style}>
      <ins
        className="adsbygoogle"
        style={{ display: 'block', textAlign: 'center' }}
        data-ad-layout={layout}
        data-ad-format={format}
        data-ad-client="ca-pub-8057197445850296"
        data-ad-slot={slot}
      />
    </div>
  )
}