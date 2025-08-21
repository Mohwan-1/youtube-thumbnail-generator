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
      title: "1️⃣ Google AI Studio 접속하기",
      description: "먼저 Google AI Studio에 들어가세요",
      content: (
        <div className="space-y-4">
          <p className="text-gray-300">
            📱 구글 계정으로 로그인해야 해요.<br/>
            <strong>지메일 계정 있으면 바로 가능!</strong>
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
              💡 <strong>팁:</strong> 새 탭에서 열리니까 이 가이드를 보면서 따라하세요!
            </p>
          </div>
        </div>
      )
    },
    {
      title: "2️⃣ API 키 발급 메뉴 찾기",
      description: "로그인 후, \"Get API key\" 버튼을 찾아요",
      content: (
        <div className="space-y-4">
          <div className="bg-yellow-900/30 p-3 rounded-lg">
            <p className="text-yellow-300 text-sm">
              🎯 <strong>찾는 곳:</strong> 왼쪽 메뉴나 상단에 있어요
            </p>
          </div>
          <p className="text-gray-300">
            <strong>&quot;Get API key&quot;</strong> 또는 <strong>&quot;API 키 만들기&quot;</strong> 버튼을 누르세요.<br/>
            보통 왼쪽 메뉴나 상단에 있어요.
          </p>
          <div className="bg-blue-900/30 p-3 rounded-lg">
            <p className="text-blue-300 text-sm">
              💡 메뉴가 안 보이면 햄버거 버튼(≡)을 눌러보세요!
            </p>
          </div>
        </div>
      )
    },
    {
      title: "3️⃣ 약관 동의하기",
      description: "API를 사용하려면 규칙(약관)에 동의해야 해요",
      content: (
        <div className="space-y-4">
          <p className="text-gray-300">
            체크박스를 선택하고 <strong>Continue(계속)</strong> 버튼을 누르면 돼요.
          </p>
          <div className="bg-green-900/30 p-3 rounded-lg">
            <p className="text-green-300 text-sm">
              ✅ <strong>간단해요:</strong> 체크 → Continue 버튼만 누르면 끝!
            </p>
          </div>
        </div>
      )
    },
    {
      title: "4️⃣ 새 프로젝트에 API 키 생성",
      description: "구글이 자동으로 새로운 API 키를 만들어줘요",
      content: (
        <div className="space-y-4">
          <p className="text-gray-300">
            <strong>&quot;Create API key&quot;</strong> 또는<br/>
            <strong>&quot;Create API key in new project&quot;</strong> 버튼을 클릭하세요.
          </p>
          <div className="bg-green-900/30 p-3 rounded-lg">
            <p className="text-green-300 text-sm">
              ✅ <strong>무료 사용량:</strong> 매월 1,500번까지 무료로 사용 가능!
            </p>
          </div>
        </div>
      )
    },
    {
      title: "5️⃣ 키 복사 & 안전 보관",
      description: "화면에 나오는 긴 문자열이 바로 API 키예요",
      content: (
        <div className="space-y-4">
          <div className="bg-green-900/30 p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <CheckCircle className="text-green-400" size={20} />
              <strong className="text-green-300">마지막 단계!</strong>
            </div>
            <ol className="list-decimal list-inside space-y-2 text-green-200">
              <li>화면에 나오는 긴 문자열(영문+숫자 조합)이 API 키예요</li>
              <li><strong>Copy(복사)</strong> 버튼을 눌러서 복사하세요</li>
              <li>이 페이지로 돌아와서 API 키를 입력하고 저장하세요</li>
            </ol>
          </div>
          <div className="bg-red-900/30 p-3 rounded-lg">
            <div className="flex items-center gap-2 mb-1">
              <AlertCircle className="text-red-400" size={16} />
              <strong className="text-red-300 text-sm">중요!</strong>
            </div>
            <p className="text-red-200 text-sm">
              <strong>중요한 비밀번호랑 비슷하니까 절대 남에게 알려주면 안 돼요!</strong><br/>
              SNS나 카페 등에 올리면 절대 안됩니다.
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