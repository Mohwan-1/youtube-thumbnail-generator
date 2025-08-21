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
유튜브 썸네일을 위한 텍스트 디자인을 5개 생성해주세요.

영상 제목: "${title}"
키워드: "${keywords}"

반드시 다음 JSON 형식으로만 응답해주세요 (다른 텍스트 없이):
{
  "thumbnails": [
    {
      "title": "짧고 임팩트 있는 제목",
      "subtitle": "부제목",
      "background": "#색상코드",
      "textColor": "#색상코드",
      "accentColor": "#색상코드"
    },
    {
      "title": "다른 제목",
      "subtitle": "다른 부제목",
      "background": "#색상코드",
      "textColor": "#색상코드",
      "accentColor": "#색상코드"
    },
    {
      "title": "세번째 제목",
      "subtitle": "세번째 부제목",
      "background": "#색상코드",
      "textColor": "#색상코드",
      "accentColor": "#색상코드"
    },
    {
      "title": "네번째 제목",
      "subtitle": "네번째 부제목",
      "background": "#색상코드",
      "textColor": "#색상코드",
      "accentColor": "#색상코드"
    },
    {
      "title": "다섯번째 제목",
      "subtitle": "다섯번째 부제목",
      "background": "#색상코드",
      "textColor": "#색상코드",
      "accentColor": "#색상코드"
    }
  ]
}

요구사항:
- 제목은 10글자 이내로 짧고 임팩트 있게
- 배경색은 어둡거나 밝은 톤으로 다양하게
- 텍스트 색상은 배경과 대비되어 잘 보이게
- 유튜브 썸네일 특성상 자극적이고 클릭하고 싶게 만들어주세요
- 각 썸네일은 서로 다른 스타일과 색상을 가져야 합니다
- JSON 형식만 응답하고 다른 설명은 포함하지 마세요
`

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
      
      // 백업 썸네일 데이터 제공
      thumbnailData = {
        thumbnails: [
          {
            title: title.substring(0, 10),
            subtitle: keywords,
            background: "#1a1a1a",
            textColor: "#ffffff",
            accentColor: "#ff6b6b"
          },
          {
            title: "클릭 유도",
            subtitle: "지금 시청",
            background: "#2d2d2d",
            textColor: "#ffffff",
            accentColor: "#4ecdc4"
          },
          {
            title: "놓치면 후회",
            subtitle: "필수 시청",
            background: "#ff6b6b",
            textColor: "#ffffff",
            accentColor: "#ffffff"
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