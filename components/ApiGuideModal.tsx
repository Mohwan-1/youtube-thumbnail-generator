import { useState, useEffect } from 'react'
import { X, ExternalLink, CheckCircle, AlertCircle } from 'lucide-react'

interface ApiGuideModalProps {
  isOpen: boolean
  onClose: () => void
}

export default function ApiGuideModal({ isOpen, onClose }: ApiGuideModalProps) {
  const [currentStep, setCurrentStep] = useState(0)

  // ESC 키로 팝업 닫기
  useEffect(() => {
    const handleEscapeKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        onClose()
      }
    }

    if (isOpen) {
      document.addEventListener('keydown', handleEscapeKey)
      // 스크롤 방지
      document.body.style.overflow = 'hidden'
    }

    return () => {
      document.removeEventListener('keydown', handleEscapeKey)
      document.body.style.overflow = 'unset'
    }
  }, [isOpen, onClose])

  if (!isOpen) return null

  const steps = [
    {
      title: "1단계: Google AI Studio 접속하기",
      description: "구글 계정으로 로그인해주세요",
      content: (
        <div className="space-y-4">
          <p className="text-gray-300">
            📱 <strong>구글 계정이 필요해요!</strong><br/>
            Gmail이나 YouTube 계정이 있으면 됩니다.
          </p>
          <button
            onClick={() => window.open('https://aistudio.google.com/', '_blank')}
            className="btn-primary w-full flex items-center justify-center gap-2"
          >
            <ExternalLink size={20} />
            Google AI Studio 열기
          </button>
          <div className="bg-blue-900/30 p-3 rounded-lg">
            <p className="text-blue-300 text-sm">
              💡 <strong>팁:</strong> 새 탭에서 열리니까 이 가이드를 계속 보면서 따라하세요!
            </p>
          </div>
        </div>
      )
    },
    {
      title: "2단계: 약관 동의하기",
      description: "Google AI 서비스 이용 약관에 동의해요",
      content: (
        <div className="space-y-4">
          <div className="bg-yellow-900/30 p-3 rounded-lg">
            <p className="text-yellow-300 text-sm">
              🎯 <strong>처음 방문하신다면:</strong> 약관 동의 화면이 나타날 거예요
            </p>
          </div>
          <ol className="list-decimal list-inside space-y-2 text-gray-300">
            <li>Google AI Studio에 처음 접속</li>
            <li>서비스 약관 및 개인정보처리방침 확인</li>
            <li>동의 체크박스 클릭</li>
            <li>계속하기 또는 Continue 버튼 클릭</li>
          </ol>
          <div className="bg-green-900/30 p-3 rounded-lg">
            <p className="text-green-300 text-sm">
              ✅ 동의하면 AI Studio 메인 화면으로 이동합니다!
            </p>
          </div>
        </div>
      )
    },
    {
      title: "3단계: API 키 생성 메뉴 찾기",
      description: "왼쪽 메뉴에서 API key를 찾아요",
      content: (
        <div className="space-y-4">
          <div className="bg-blue-900/30 p-3 rounded-lg">
            <p className="text-blue-300 text-sm">
              🔍 <strong>찾는 방법:</strong> 화면 왼쪽에 메뉴가 있어요
            </p>
          </div>
          <ol className="list-decimal list-inside space-y-2 text-gray-300">
            <li>Google AI Studio 메인 화면 확인</li>
            <li>왼쪽 사이드바 메뉴에서 <strong>🔑 Get API key</strong> 클릭</li>
            <li>또는 <strong>API keys</strong> 메뉴 클릭</li>
          </ol>
          <div className="bg-yellow-900/30 p-3 rounded-lg">
            <p className="text-yellow-300 text-sm">
              💡 <strong>참고:</strong> 메뉴가 접혀있다면 햄버거 버튼(≡)을 클릭해서 열어주세요!
            </p>
          </div>
        </div>
      )
    },
    {
      title: "4단계: API 키 생성하기",
      description: "새로운 API 키를 만들어요",
      content: (
        <div className="space-y-4">
          <ol className="list-decimal list-inside space-y-2 text-gray-300">
            <li><strong>Create API key</strong> 또는 <strong>API 키 만들기</strong> 버튼 클릭</li>
            <li>Google Cloud 프로젝트 선택 (기본 프로젝트 선택 가능)</li>
            <li>만약 프로젝트가 없다면 <strong>Create API key in new project</strong> 선택</li>
            <li>API 키가 생성됩니다!</li>
          </ol>
          <div className="bg-green-900/30 p-3 rounded-lg">
            <p className="text-green-300 text-sm">
              ✅ <strong>무료 사용량:</strong> 매월 무료로 많은 요청을 할 수 있어요!<br/>
              (월 1,500 요청까지 무료)
            </p>
          </div>
        </div>
      )
    },
    {
      title: "5단계: API 키 복사하고 사용하기",
      description: "생성된 API 키를 썸네일 생성기에 입력해요",
      content: (
        <div className="space-y-4">
          <div className="bg-green-900/30 p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <CheckCircle className="text-green-400" size={20} />
              <strong className="text-green-300">완료!</strong>
            </div>
            <ol className="list-decimal list-inside space-y-2 text-green-200">
              <li>생성된 API 키 옆의 <strong>복사</strong> 버튼 클릭</li>
              <li>이 썸네일 생성기 페이지로 돌아와서</li>
              <li><strong>API 키 저장</strong> 버튼을 눌러서</li>
              <li>복사한 키를 붙여넣고 저장하세요</li>
            </ol>
          </div>
          <div className="bg-red-900/30 p-3 rounded-lg">
            <div className="flex items-center gap-2 mb-1">
              <AlertCircle className="text-red-400" size={16} />
              <strong className="text-red-300 text-sm">보안 주의!</strong>
            </div>
            <p className="text-red-200 text-sm">
              API 키는 절대 다른 사람과 공유하지 마세요!<br/>
              GitHub, SNS 등에 올리면 안됩니다.
            </p>
          </div>
        </div>
      )
    }
  ]

  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose()
    }
  }

  return (
    <div 
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      onClick={handleBackdropClick}
    >
      <div className="bg-dark-light rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-600">
          <div>
            <h2 className="text-2xl font-bold text-white">
              🔑 Google Gemini API 키 발급 가이드
            </h2>
            <p className="text-sm text-gray-400 mt-1">
              Google AI Studio에서 무료로 발급받을 수 있어요 · ESC 키 또는 배경 클릭으로 닫기
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
            title="닫기 (ESC)"
          >
            <X size={24} />
          </button>
        </div>

        {/* Progress */}
        <div className="p-6 border-b border-gray-600">
          <div className="flex justify-between items-center mb-4">
            {steps.map((_, index) => (
              <div
                key={index}
                className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                  index <= currentStep
                    ? 'bg-primary text-white'
                    : 'bg-gray-600 text-gray-400'
                }`}
              >
                {index + 1}
              </div>
            ))}
          </div>
          <div className="w-full bg-gray-600 rounded-full h-2">
            <div
              className="bg-primary h-2 rounded-full transition-all duration-300"
              style={{ width: `${((currentStep + 1) / steps.length) * 100}%` }}
            />
          </div>
        </div>

        {/* Content */}
        <div className="p-6">
          <div className="mb-6">
            <h3 className="text-xl font-bold text-white mb-2">
              {steps[currentStep].title}
            </h3>
            <p className="text-gray-300 mb-4">
              {steps[currentStep].description}
            </p>
            {steps[currentStep].content}
          </div>

          {/* Navigation */}
          <div className="flex justify-between">
            <button
              onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
              disabled={currentStep === 0}
              className="px-4 py-2 bg-gray-600 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              이전
            </button>
            
            {currentStep < steps.length - 1 ? (
              <button
                onClick={() => setCurrentStep(Math.min(steps.length - 1, currentStep + 1))}
                className="btn-primary"
              >
                다음
              </button>
            ) : (
              <button
                onClick={onClose}
                className="btn-primary"
              >
                완료! 👍
              </button>
            )}
          </div>
        </div>

        {/* Quick Links */}
        <div className="p-6 bg-gray-800 rounded-b-lg">
          <h4 className="text-white font-semibold mb-3">🔗 빠른 링크</h4>
          <div className="grid grid-cols-1 gap-2">
            <button
              onClick={() => window.open('https://aistudio.google.com/', '_blank')}
              className="text-left p-3 bg-gray-700 hover:bg-gray-600 rounded text-sm text-gray-300 transition-colors"
            >
              🤖 Google AI Studio - API 키 발급받기
            </button>
            <button
              onClick={() => window.open('https://ai.google.dev/gemini-api/docs/quickstart', '_blank')}
              className="text-left p-3 bg-gray-700 hover:bg-gray-600 rounded text-sm text-gray-300 transition-colors"
            >
              📚 Gemini API 공식 문서
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}