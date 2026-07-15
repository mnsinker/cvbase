'use client'

import { useEffect, useRef, useState } from 'react'

export type TocItem = {
  id: string
  title: string
  level: number
}

type TocGroup = {
  heading: TocItem
  children: TocItem[]
}

type TOCProps = {
  items: TocItem[]
  title?: string
}

function buildGroups(items: TocItem[]): TocGroup[] {
  const groups: TocGroup[] = []

  for (const item of items) {
    if (item.level === 1) {
      groups.push({
        heading: item,
        children: [],
      })
      continue
    }

    const currentGroup = groups[groups.length - 1]

    if (currentGroup) {
      currentGroup.children.push(item)
    }
  }

  return groups
}

export function TOC({ items, title = 'Contents' }: TOCProps) {
  const [activeId, setActiveId] = useState(items[0]?.id)
  const clickedId = useRef<string | null>(null)

  const groups = buildGroups(items)

  useEffect(() => {
    if (!items.length) {
      return
    }

    const visibleSections = new Map<string, number>()

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            visibleSections.set(
              entry.target.id,
              entry.intersectionRatio,
            )
          } else {
            visibleSections.delete(entry.target.id)
          }
        })

        const mostVisible = [...visibleSections.entries()].sort(
          (a, b) => b[1] - a[1],
        )[0]

        if (mostVisible && !clickedId.current) {
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

  function renderItem(
    item: TocItem,
    isChild = false,
  ) {
    const isActive = item.id === activeId

    return (
      <a
        key={item.id}
        href={`#${item.id}`}
        onClick={() => {
          clickedId.current = item.id
          setActiveId(item.id)
          window.setTimeout(() => {
            clickedId.current = null
          }, 1000)
        }}
        className={`
          relative block
          text-sm
          py-1
          no-underline
          transition
          ${
            isChild
              ? 'ml-6'
              : ''
          }
          ${
            isActive
              ? 'font-medium text-teal-500 dark:text-teal-400'
              : 'text-zinc-600 hover:text-zinc-700 dark:text-zinc-500 dark:hover:text-zinc-300'
          }
        `}
      >
        {isActive && (
          <span
            className="
              absolute
              -left-3
              top-1/2
              h-5
              w-0.5
              -translate-y-1/2
              bg-teal-500
              dark:bg-teal-400
            "
          />
        )}

        {item.title}
      </a>
    )
  }

  return (
    <nav
      aria-label="Project sections"
      className="
        sticky
        top-24
        hidden
        w-64
        shrink-0
        self-start
        lg:block
      "
    >
      <p
        className="
          text-xs
          font-medium
          uppercase
          tracking-wider
          text-zinc-400
          dark:text-zinc-500
        "
      >
        {title}
      </p>

      <div className="mt-4 space-y-5">
        {groups.map((group) => (
          <div key={group.heading.id}>
            {renderItem(group.heading)}

            {group.children.length > 0 && (
              <div className="mt-1 space-y-1">
                {group.children.map((child) =>
                  renderItem(child, true),
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </nav>
  )
}
