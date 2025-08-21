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
    const model = genAI.getGenerativeModel({ model: "gemini-2.0-flash-exp" })

    const prompt = `
유튜브 썸네일을 위한 텍스트 디자인을 5개 생성해주세요.

영상 제목: "${title}"
키워드: "${keywords}"

각 썸네일에 대해 다음 JSON 형식으로 응답해주세요:
{
  "thumbnails": [
    {
      "id": "1",
      "title": "짧고 임팩트 있는 제목",
      "subtitle": "부제목 (선택사항)",
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
`

    const result = await model.generateContent(prompt)
    const response = await result.response
    const text = response.text()

    // JSON 추출
    const jsonMatch = text.match(/\{[\s\S]*\}/)
    if (!jsonMatch) {
      throw new Error('Invalid response format')
    }

    const thumbnailData = JSON.parse(jsonMatch[0])
    
    // ID 추가 및 검증
    thumbnailData.thumbnails = thumbnailData.thumbnails.map((thumbnail: any, index: number) => ({
      ...thumbnail,
      id: `thumbnail-${index + 1}`
    }))

    res.status(200).json(thumbnailData)
  } catch (error) {
    console.error('Error generating thumbnails:', error)
    res.status(500).json({ error: 'Failed to generate thumbnails' })
  }
}