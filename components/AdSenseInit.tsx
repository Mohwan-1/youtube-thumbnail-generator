import { useEffect } from 'react'

declare global {
  interface Window {
    adsbygoogle: any[]
  }
}

export default function AdSenseInit() {
  useEffect(() => {
    // AdSense 자동 광고 초기화
    if (typeof window !== 'undefined') {
      const initAds = () => {
        try {
          (window.adsbygoogle = window.adsbygoogle || []).push({
            google_ad_client: "ca-pub-8057197445850296",
            enable_page_level_ads: true
          })
        } catch (err) {
          console.error('AdSense auto ads error:', err)
        }
      }

      // 페이지 로드 후 광고 초기화
      if (document.readyState === 'complete') {
        initAds()
      } else {
        window.addEventListener('load', initAds)
        return () => window.removeEventListener('load', initAds)
      }
    }
  }, [])

  return null
}