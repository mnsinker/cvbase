'use client'

import { useEffect, useState } from 'react'

export type TocItem = {
  id: string
  title: string
}

type TOCProps = {
  items: TocItem[]
}

export function TOC({ items }: TOCProps) {
  const [activeId, setActiveId] = useState(items[0]?.id)

  useEffect(() => {
    if (!items.length) {
      return
    }

    const visibleSections = new Map<string, number>()
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            visibleSections.set(entry.target.id, entry.intersectionRatio)
          } else {
            visibleSections.delete(entry.target.id)
          }
        })

        const mostVisible = [...visibleSections.entries()].sort(
          (a, b) => b[1] - a[1],
        )[0]

        if (mostVisible) {
          setActiveId(mostVisible[0])
        }
      },
      {
        rootMargin: '-20% 0px -55% 0px',
        threshold: [0, 0.25, 0.5, 0.75, 1],
      },
    )

    items.forEach((item) => {
      const section = document.getElementById(item.id)

      if (section) {
        observer.observe(section)
      }
    })

    return () => observer.disconnect()
  }, [items])

  return (
    <nav
      aria-label="Project sections"
      className="sticky top-24 hidden w-44 shrink-0 self-start lg:block"
    >
      <p className="text-xs font-medium tracking-wide text-zinc-400 uppercase dark:text-zinc-500">
        Contents
      </p>
      <ol className="mt-4 space-y-2 border-l border-zinc-100 dark:border-zinc-700/40">
        {items.map((item) => {
          const isActive = item.id === activeId

          return (
            <li key={item.id}>
              <a
                href={`#${item.id}`}
                className={`block border-l-2 py-1.5 pl-4 text-sm transition ${
                  isActive
                    ? '-ml-px border-teal-500 font-medium text-teal-500 dark:border-teal-400 dark:text-teal-400'
                    : '-ml-px border-transparent text-zinc-500 hover:border-zinc-200 hover:text-zinc-700 dark:text-zinc-400 dark:hover:border-zinc-600 dark:hover:text-zinc-200'
                }`}
              >
                {item.title}
              </a>
            </li>
          )
        })}
      </ol>
    </nav>
  )
}
