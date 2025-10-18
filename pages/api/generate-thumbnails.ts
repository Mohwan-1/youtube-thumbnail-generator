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
    // Use gemini-2.5-flash for text generation
    const model = genAI.getGenerativeModel({ model: "gemini-2.5-flash" })

    const prompt = `
당신은 유튜브 썸네일 전문 디자이너입니다. "${title}"과 "${keywords}"를 분석하여 클릭률을 높일 수 있는 썸네일 디자인을 5개 생성해주세요.

영상 제목: "${title}"
키워드: "${keywords}"

각 썸네일에 대해 다음 요소들을 포함하여 설계해주세요:

1. 강력한 제목 문구 (6-12글자)
2. 화려한 CSS 배경 그라데이션 (복잡하고 멋진 효과)
3. 감정적 반응을 유도하는 부제목
4. 클릭 유도 요소 (화살표, 강조 등)

반드시 다음 JSON 형식으로만 응답하세요:
{
  "thumbnails": [
    {
      "title": "강력한 제목",
      "subtitle": "부제목",
      "background": "복잡한 CSS 그라데이션 (예: radial-gradient, conic-gradient, 여러 색상 조합)",
      "textColor": "#색상코드",
      "accentColor": "#색상코드",
      "visualElements": "배경 디자인 설명",
      "emotion": "유도하려는 감정 (호기심, 충격, 흥미 등)",
      "clickBait": "클릭 유도 요소 설명"
    }
  ]
}

중요 요구사항:
- 제목은 "${title}"의 핵심을 담되 더 자극적으로
- "${keywords}"를 활용하여 타겟 관심사 반영
- background는 반드시 화려하고 복잡한 CSS 그라데이션 (linear, radial, conic 등 조합)
- 각 썸네일은 서로 다른 감정과 스타일의 배경
- 유튜브 알고리즘에 최적화된 디자인
- 모바일에서도 잘 보이는 큰 텍스트와 명확한 대비
- 배경은 최소 3가지 색상을 포함하는 그라데이션

background 예시:
- "radial-gradient(circle at 30% 50%, #ff6b6b, #ee5a6f, #c44569)"
- "linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)"
- "conic-gradient(from 180deg at 50% 50%, #ff0080, #ff8c00, #40e0d0, #ff0080)"

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
      
      // 백업 썸네일 데이터 제공 (새로운 형식)
      const shortTitle = title.length > 8 ? title.substring(0, 8) + '..' : title
      const firstKeyword = keywords.split(',')[0]?.trim() || "트렌드"
      
      thumbnailData = {
        thumbnails: [
          {
            title: `충격! ${shortTitle}`,
            subtitle: "99% 몰랐던 비밀",
            background: "radial-gradient(circle at 20% 80%, #ff0000, #cc0000, #8b0000)",
            textColor: "#ffffff",
            accentColor: "#ffff00",
            visualElements: "강렬한 빨간 방사형 그라데이션 배경",
            emotion: "충격과 호기심",
            clickBait: "숫자와 비율로 신뢰성 어필"
          },
          {
            title: "대박 실화냐",
            subtitle: `${firstKeyword} 진실`,
            background: "linear-gradient(135deg, #667eea 0%, #764ba2 50%, #a26ea8 100%)",
            textColor: "#ffffff",
            accentColor: "#00ff88",
            visualElements: "보라-파랑 대각선 그라데이션",
            emotion: "놀라움과 의심",
            clickBait: "실화 여부 확인 욕구 자극"
          },
          {
            title: "지금 핫한",
            subtitle: `${firstKeyword} 정보`,
            background: "conic-gradient(from 45deg at 50% 50%, #ffd700, #ff8c00, #ff4500, #ffd700)",
            textColor: "#000000",
            accentColor: "#dc3545",
            visualElements: "원형 회전 그라데이션, 뜨거운 색상",
            emotion: "FOMO (놓칠까봐 하는 불안)",
            clickBait: "시급함과 트렌드 강조"
          },
          {
            title: "완벽 정리",
            subtitle: "한번에 끝내기",
            background: "linear-gradient(to bottom, #e0e0e0, #b0b0b0, #808080)",
            textColor: "#212529",
            accentColor: "#007bff",
            visualElements: "깔끔한 회색 세로 그라데이션",
            emotion: "완성도와 효율성",
            clickBait: "한번에 해결 가능함 어필"
          },
          {
            title: "프로 비밀",
            subtitle: `${firstKeyword} 노하우`,
            background: "radial-gradient(ellipse at 50% 30%, #2c2c2c, #1a1a1a, #000000)",
            textColor: "#ffffff",
            accentColor: "#ffd700",
            visualElements: "어두운 타원형 그라데이션, 프리미엄 느낌",
            emotion: "전문성과 특별함",
            clickBait: "전문가만 아는 비밀 정보"
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