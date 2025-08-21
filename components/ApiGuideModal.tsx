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
      title: "1단계: 구글 클라우드 콘솔 접속하기",
      description: "구글 계정으로 로그인해주세요",
      content: (
        <div className="space-y-4">
          <p className="text-gray-300">
            📱 <strong>구글 계정이 필요해요!</strong><br/>
            Gmail이나 YouTube 계정이 있으면 됩니다.
          </p>
          <button
            onClick={() => window.open('https://console.cloud.google.com/', '_blank')}
            className="btn-primary w-full flex items-center justify-center gap-2"
          >
            <ExternalLink size={20} />
            구글 클라우드 콘솔 열기
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
      title: "2단계: 새 프로젝트 만들기",
      description: "썸네일 생성기용 프로젝트를 만들어요",
      content: (
        <div className="space-y-4">
          <div className="bg-yellow-900/30 p-3 rounded-lg">
            <p className="text-yellow-300 text-sm">
              🎯 <strong>찾아보세요:</strong> 화면 위쪽에 프로젝트 선택 버튼이 있어요
            </p>
          </div>
          <ol className="list-decimal list-inside space-y-2 text-gray-300">
            <li>프로젝트 선택 클릭</li>
            <li>새 프로젝트 버튼 클릭</li>
            <li>프로젝트 이름: <code className="bg-gray-700 px-2 py-1 rounded">썸네일생성기</code></li>
            <li>만들기 버튼 클릭</li>
          </ol>
          <div className="bg-green-900/30 p-3 rounded-lg">
            <p className="text-green-300 text-sm">
              ✅ 프로젝트가 만들어질 때까지 1-2분 기다려주세요!
            </p>
          </div>
        </div>
      )
    },
    {
      title: "3단계: Gemini API 활성화하기",
      description: "AI 기능을 사용할 수 있게 켜주세요",
      content: (
        <div className="space-y-4">
          <button
            onClick={() => window.open('https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com', '_blank')}
            className="btn-secondary w-full flex items-center justify-center gap-2"
          >
            <ExternalLink size={20} />
            Gemini API 페이지 바로가기
          </button>
          <ol className="list-decimal list-inside space-y-2 text-gray-300">
            <li>위 버튼을 눌러서 Gemini API 페이지로 이동</li>
            <li><strong>사용 설정</strong> 파란 버튼 클릭</li>
            <li>몇 초 기다리면 활성화 완료!</li>
          </ol>
          <div className="bg-blue-900/30 p-3 rounded-lg">
            <p className="text-blue-300 text-sm">
              💡 <strong>참고:</strong> 무료로 매달 많은 요청을 할 수 있어요!
            </p>
          </div>
        </div>
      )
    },
    {
      title: "4단계: API 키 만들기",
      description: "썸네일 생성기에서 사용할 열쇠를 만들어요",
      content: (
        <div className="space-y-4">
          <button
            onClick={() => window.open('https://console.cloud.google.com/apis/credentials', '_blank')}
            className="btn-secondary w-full flex items-center justify-center gap-2"
          >
            <ExternalLink size={20} />
            API 키 만들기 페이지 바로가기
          </button>
          <ol className="list-decimal list-inside space-y-2 text-gray-300">
            <li>+ 사용자 인증 정보 만들기 클릭</li>
            <li>API 키 선택</li>
            <li>API 키가 만들어져요! (복사해두세요)</li>
            <li>키 제한 버튼 클릭 (보안을 위해)</li>
            <li>API 제한사항에서 Generative Language API 선택</li>
            <li>저장 클릭</li>
          </ol>
        </div>
      )
    },
    {
      title: "5단계: API 키 복사하고 사용하기",
      description: "만든 API 키를 썸네일 생성기에 붙여넣어요",
      content: (
        <div className="space-y-4">
          <div className="bg-green-900/30 p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <CheckCircle className="text-green-400" size={20} />
              <strong className="text-green-300">거의 다 끝났어요!</strong>
            </div>
            <ol className="list-decimal list-inside space-y-2 text-green-200">
              <li>만들어진 API 키를 복사하세요</li>
              <li>이 페이지로 돌아와서</li>
              <li>API 키 수정하기 버튼을 눌러서</li>
              <li>복사한 키를 붙여넣으세요</li>
            </ol>
          </div>
          <div className="bg-red-900/30 p-3 rounded-lg">
            <div className="flex items-center gap-2 mb-1">
              <AlertCircle className="text-red-400" size={16} />
              <strong className="text-red-300 text-sm">중요!</strong>
            </div>
            <p className="text-red-200 text-sm">
              API 키는 비밀번호 같은 거예요. 다른 사람에게 알려주면 안 돼요!
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
              🔑 구글 AI API 키 발급 가이드
            </h2>
            <p className="text-sm text-gray-400 mt-1">
              ESC 키 또는 배경 클릭으로 닫을 수 있어요
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
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            <button
              onClick={() => window.open('https://console.cloud.google.com/', '_blank')}
              className="text-left p-2 bg-gray-700 hover:bg-gray-600 rounded text-sm text-gray-300 transition-colors"
            >
              📊 구글 클라우드 콘솔
            </button>
            <button
              onClick={() => window.open('https://console.cloud.google.com/apis/credentials', '_blank')}
              className="text-left p-2 bg-gray-700 hover:bg-gray-600 rounded text-sm text-gray-300 transition-colors"
            >
              🔑 API 키 관리
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}