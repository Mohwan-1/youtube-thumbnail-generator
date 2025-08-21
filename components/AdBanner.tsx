import { useEffect } from 'react'

interface AdBannerProps {
  slot: string
  format?: string
  layout?: string
  style?: React.CSSProperties
  className?: string
}

export default function AdBanner({ 
  slot, 
  format = "auto", 
  layout,
  style,
  className = "" 
}: AdBannerProps) {
  useEffect(() => {
    try {
      // @ts-ignore
      (window.adsbygoogle = window.adsbygoogle || []).push({})
    } catch (err) {
      console.error('AdSense error:', err)
    }
  }, [])

  return (
    <div className={`ad-container ${className}`} style={style}>
      <ins
        className="adsbygoogle"
        style={{ display: 'block', textAlign: 'center' }}
        data-ad-client="ca-pub-8057197445850296"
        data-ad-slot={slot}
        data-ad-format={format}
        {...(layout && { 'data-ad-layout': layout })}
      />
    </div>
  )
}