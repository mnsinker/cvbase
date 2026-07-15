'use client'

import { useEffect, useId, useRef, useState } from 'react'
import Image from 'next/image'

import { Button } from '@/components/Button'
import wechatQrCode from '@/images/wechat_qrcode.jpg'

const wechatQrOpenEvent = 'wechat-qr-open'

export function WeChatQrButton({ children }: { children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(false)
  const containerRef = useRef<HTMLDivElement>(null)
  const popoverId = `wechat-qr-${useId().replace(/:/g, '')}`

  useEffect(() => {
    if (!isOpen) return

    function closeOnOutsidePointerDown(event: PointerEvent) {
      if (!containerRef.current?.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    function closeOnEscape(event: KeyboardEvent) {
      if (event.key === 'Escape') {
        setIsOpen(false)
        containerRef.current?.querySelector('button')?.focus()
      }
    }

    function closeForAnotherPopover(event: Event) {
      if ((event as CustomEvent<string>).detail !== popoverId) {
        setIsOpen(false)
      }
    }

    function closeOnScroll() {
      setIsOpen(false)
    }

    document.addEventListener('pointerdown', closeOnOutsidePointerDown)
    document.addEventListener('keydown', closeOnEscape)
    document.addEventListener(wechatQrOpenEvent, closeForAnotherPopover)
    window.addEventListener('scroll', closeOnScroll, true)

    return () => {
      document.removeEventListener('pointerdown', closeOnOutsidePointerDown)
      document.removeEventListener('keydown', closeOnEscape)
      document.removeEventListener(wechatQrOpenEvent, closeForAnotherPopover)
      window.removeEventListener('scroll', closeOnScroll, true)
    }
  }, [isOpen, popoverId])

  function togglePopover() {
    if (isOpen) {
      setIsOpen(false)
      return
    }

    document.dispatchEvent(
      new CustomEvent(wechatQrOpenEvent, { detail: popoverId }),
    )
    setIsOpen(true)
  }

  return (
    <div ref={containerRef} className="relative mt-6">
      <Button
        type="button"
        variant="secondary"
        className="w-full"
        aria-expanded={isOpen}
        aria-controls={popoverId}
        onClick={togglePopover}
      >
        {children}
      </Button>
      {isOpen && (
        <div
          id={popoverId}
          className="absolute right-0 bottom-full z-20 mb-3 rounded-2xl border border-zinc-200 bg-white p-3 shadow-xl dark:border-zinc-700 dark:bg-zinc-800"
        >
          <Image
            src={wechatQrCode}
            alt=""
            width={180}
            height={180}
            className="h-44 w-44 rounded-lg object-cover"
          />
        </div>
      )}
    </div>
  )
}
