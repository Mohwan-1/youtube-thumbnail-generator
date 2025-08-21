import { NextApiRequest, NextApiResponse } from 'next'
import { GoogleGenerativeAI } from '@google/generative-ai'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  const { title, keywords, apiKey } = req.body

  if (!title || !keywords || !apiKey) {
    return res.status(400).json({ error: 'Missing required fields' })
  }

  try {
    const genAI = new GoogleGenerativeAI(apiKey)
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" })

    const prompt = `
당신은 유튜브 썸네일 전문 디자이너입니다. 주어진 영상 제목과 키워드를 바탕으로 고품질의 썸네일 텍스트 디자인을 생성해주세요.

영상 제목: "${title}"
키워드: "${keywords}"

유튜브 썸네일 업계 트렌드를 반영하여 다음과 같이 5개의 다양한 스타일로 생성해주세요:

1. 충격적/자극적 스타일 (빨간색 계열, 굵은 텍스트)
2. 트렌디/모던 스타일 (그라데이션, 네온 컬러)
3. 미니멀/깔끔 스타일 (단순한 색상, 여백 활용)
4. 화려/눈에 띄는 스타일 (밝은 색상, 대비 강함)
5. 프리미엄/고급 스타일 (어두운 배경, 골드/실버 악센트)

반드시 다음 JSON 형식으로만 응답해주세요:
{
  "thumbnails": [
    {
      "title": "충격! 이것만 알면",
      "subtitle": "99% 몰랐던 비밀",
      "background": "#ff1744",
      "textColor": "#ffffff",
      "accentColor": "#ffff00"
    },
    {
      "title": "지금 핫한",
      "subtitle": "놓치면 후회할",
      "background": "linear-gradient(45deg, #667eea 0%, #764ba2 100%)",
      "textColor": "#ffffff",
      "accentColor": "#00ff88"
    },
    {
      "title": "완벽 정리",
      "subtitle": "한번에 끝내기",
      "background": "#f8f9fa",
      "textColor": "#212529",
      "accentColor": "#007bff"
    },
    {
      "title": "대박! 실화냐",
      "subtitle": "믿을 수 없는",
      "background": "#ffc107",
      "textColor": "#000000",
      "accentColor": "#dc3545"
    },
    {
      "title": "프로가 알려주는",
      "subtitle": "고급 노하우",
      "background": "#1a1a1a",
      "textColor": "#ffffff",
      "accentColor": "#ffd700"
    }
  ]
}

핵심 요구사항:
- 제목: 6-12글자, 클릭을 유도하는 강력한 문구
- 부제목: 호기심을 자극하는 보조 문구
- 색상: 유튜브에서 시선을 끄는 고대비 조합
- 각 썸네일은 완전히 다른 분위기와 타겟
- 실제 유튜브 크리에이터들이 사용하는 검증된 패턴 활용

JSON만 응답하세요:`

    const result = await model.generateContent(prompt)
    const response = await result.response
    const text = response.text().trim()

    console.log('API Response:', text)

    let thumbnailData
    try {
      // JSON 추출 시도
      const jsonMatch = text.match(/\{[\s\S]*\}/)
      if (jsonMatch) {
        thumbnailData = JSON.parse(jsonMatch[0])
      } else {
        thumbnailData = JSON.parse(text)
      }
    } catch (parseError) {
      console.error('JSON Parse Error:', parseError)
      console.error('Response text:', text)
      
      // 백업 썸네일 데이터 제공 (더 매력적인 버전)
      const shortTitle = title.length > 8 ? title.substring(0, 8) + '..' : title
      thumbnailData = {
        thumbnails: [
          {
            title: `충격! ${shortTitle}`,
            subtitle: "99% 몰랐던 사실",
            background: "#ff1744",
            textColor: "#ffffff",
            accentColor: "#ffff00"
          },
          {
            title: "대박 실화냐",
            subtitle: "믿을 수 없는",
            background: "linear-gradient(45deg, #667eea 0%, #764ba2 100%)",
            textColor: "#ffffff",
            accentColor: "#00ff88"
          },
          {
            title: "지금 핫한",
            subtitle: keywords.split(',')[0] || "트렌드",
            background: "#ffc107",
            textColor: "#000000",
            accentColor: "#dc3545"
          },
          {
            title: "완벽 정리",
            subtitle: "한번에 끝내기",
            background: "#f8f9fa",
            textColor: "#212529",
            accentColor: "#007bff"
          },
          {
            title: "프로 비밀",
            subtitle: "고급 노하우",
            background: "#1a1a1a",
            textColor: "#ffffff",
            accentColor: "#ffd700"
          }
        ]
      }
    }
    
    // ID 추가 및 검증
    if (thumbnailData.thumbnails && Array.isArray(thumbnailData.thumbnails)) {
      thumbnailData.thumbnails = thumbnailData.thumbnails.map((thumbnail: any, index: number) => ({
        ...thumbnail,
        id: `thumbnail-${index + 1}`
      }))
    } else {
      throw new Error('Invalid thumbnail data structure')
    }

    res.status(200).json(thumbnailData)
  } catch (error) {
    console.error('Error generating thumbnails:', error)
    
    // 상세한 에러 정보 제공
    const errorMessage = error instanceof Error ? error.message : 'Unknown error'
    res.status(500).json({ 
      error: 'Failed to generate thumbnails',
      details: errorMessage,
      apiKeyValid: !!apiKey && apiKey.length > 20
    })
  }
}