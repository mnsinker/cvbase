import { AlertTriangle, ArrowDown, CheckCircle2, Lightbulb } from 'lucide-react'

import { TOC, type TocItem } from '@/components/TOC'

type Problem = {
  frames: {
    title: string
    content: string[]
  }[]
  project_response?: string
}

type ArchitectureLayer = {
  title: string
  responsibilities?: string[]
  core_components?: string[]
}

type Story = {
  title: string
  description?: string[]
  problem?: string
  analysis?: string
  discovery?: string
  outcome?: string
}

type Capability = {
  title: string
  description?: string
  supports?: string[]
  includes?: string[]
  current_domains?: string[]
  future_domains?: string[]
}

type Project = {
  project: string
  problem_space: {
    current_problems: Problem[]
    future_problems: Problem[]
  }
  capabilities: {
    current_capabilities: Capability[]
    future_capabilities: Capability[]
  }
  architecture: {
    architectural_goal: {
      from?: string
      toward?: string
      purpose?: string
    }
    dynamic_flow?: string[]
    static_structure: ArchitectureLayer[]
  }
  stories: {
    story_groups: {
      title: string
      core_discovery_title?: string
      core_discovery_content?: string
      stories: Story[]
    }[]
  }
}

function Section({
  id,
  title,
  children,
}: {
  id: string
  title: string
  children: React.ReactNode
}) {
  return (
    <section
      id={id}
      className="scroll-mt-24 border-t border-zinc-100 pt-8 dark:border-zinc-700/40"
    >
      <h2 className="text-xl font-semibold tracking-tight text-teal-500 dark:text-teal-400">
        {title}
      </h2>
      <div className="mt-5">{children}</div>
    </section>
  )
}

function GroupTitle({ children }: { children: React.ReactNode }) {
  return (
    <h3 className="text-base font-semibold tracking-tight text-zinc-800 dark:text-zinc-100">
      {children}
    </h3>
  )
}

function TextList({ items }: { items?: string[] }) {
  if (!items?.length) {
    return null
  }

  return (
    <ul className="mt-3 space-y-1.5 text-sm text-zinc-600 dark:text-zinc-400">
      {items.map((item) => (
        <li key={item} className="flex gap-2">
          <span className="mt-2 h-1 w-1 flex-none rounded-full bg-teal-500" />
          <span>{item}</span>
        </li>
      ))}
    </ul>
  )
}

function LabelList({ label, items }: { label: string; items?: string[] }) {
  if (!items?.length) {
    return null
  }

  return (
    <div className="mt-4">
      <p className="text-xs font-medium tracking-wide text-zinc-400 uppercase dark:text-zinc-500">
        {label}
      </p>
      <TextList items={items} />
    </div>
  )
}

/**
 * Detects Statement/Symptoms/Consequence labels in frame content
 * and renders them as subsection labels with indented body text
 * instead of flat bullets.
 *
 * A content array like:
 *   ["Statement", "Project files exist.", "Symptoms", "…", "Consequence", "…"]
 *
 * is grouped into labeled subsections:
 *   Statement
 *     Project files exist.
 *   Symptoms
 *     …
 */
function ProblemFrameContent({ content }: { content: string[] }) {
  const LABELS = new Set(['Statement', 'Symptoms', 'Consequence'])

  // Segment the flat array into { label, body[] } groups
  const groups: { label: string; body: string[] }[] = []
  let current: { label: string; body: string[] } | null = null

  for (const item of content) {
    if (LABELS.has(item)) {
      current = { label: item, body: [] }
      groups.push(current)
    } else if (current) {
      current.body.push(item)
    } else {
      // Before any label — render as plain text
      groups.push({ label: '', body: [item] })
    }
  }

  if (!groups.length) return null

  // Check if this is actually a structured label pattern vs plain content
  const hasLabels = groups.some((g) => g.label)

  if (!hasLabels) {
    // Plain content — fall back to bullet list
    return <TextList items={content} />
  }

  return (
    <div className="mt-3 space-y-4">
      {groups.map((group) =>
        group.label ? (
          <div key={group.label}>
            <p className="text-xs font-semibold tracking-wide text-zinc-500 uppercase dark:text-zinc-400">
              {group.label}
            </p>
            <ul className="mt-1 space-y-1.5">
              {group.body.map((line) => (
                <li key={line} className="flex gap-2">
                  <span className="mt-2 h-1 w-1 flex-none rounded-full bg-teal-500" />
                  <span className="text-sm text-zinc-600 dark:text-zinc-400">{line}</span>
                </li>
              ))}
            </ul>
          </div>
        ) : (
          <p
            key={group.body[0]}
            className="text-sm text-zinc-600 dark:text-zinc-400"
          >
            {group.body[0]}
          </p>
        ),
      )}
    </div>
  )
}

/**
 * Detects "Question: … Answer: …" patterns in a capability description
 * and renders them as two separate labeled blocks, rather than one flat
 * paragraph.
 */
function CapabilityDescription({ text }: { text: string }) {
  const qaMatch = text.match(/^Question:\s*([\s\S]+?)\s*Answer:\s*([\s\S]+)$/i)

  if (!qaMatch) {
    return <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-400">{text}</p>
  }

  return (
    <div className="mt-2 space-y-2">
      <div>
        <p className="text-xs font-semibold tracking-wide text-teal-500 uppercase dark:text-teal-400">
          Question
        </p>
        <p className="mt-0.5 text-sm text-zinc-600 dark:text-zinc-400">
          {qaMatch[1].trim()}
        </p>
      </div>
      <div>
        <p className="text-xs font-semibold tracking-wide text-teal-500 uppercase dark:text-teal-400">
          Answer
        </p>
        <p className="mt-0.5 text-sm text-zinc-600 dark:text-zinc-400">
          {qaMatch[2].trim()}
        </p>
      </div>
    </div>
  )
}

function CoreDiscoveryContent({ content }: { content: string }) {
  const [intro, remainder] = content.split(/:(.+)/)
  const bullets = remainder
    ? remainder
        .split(';')
        .map((item) => item.trim())
        .filter(Boolean)
    : []

  return (
    <div className="mt-4 max-w-3xl text-base leading-8 text-zinc-600 dark:text-zinc-400">
      <p>{intro?.trim() ?? content}</p>
      {bullets.length ? (
        <ul className="mt-3 space-y-1.5 text-sm text-zinc-600 dark:text-zinc-400">
          {bullets.map((item) => (
            <li key={item} className="flex gap-2">
              <span className="mt-2 h-1 w-1 flex-none rounded-full bg-teal-500" />
              <span>{item}</span>
            </li>
          ))}
        </ul>
      ) : null}
    </div>
  )
}

function Card({
  children,
  className = '',
}: {
  children: React.ReactNode
  className?: string
}) {
  return (
    <div
      className={`rounded-lg border border-zinc-100 bg-white p-5 shadow-sm shadow-zinc-800/5 dark:border-zinc-700/40 dark:bg-zinc-800/20 ${className}`}
    >
      {children}
    </div>
  )
}

/**
 * A single stage card in the dynamic flow pipeline.
 * Renders the stage name as a box in a vertical chain.
 */
function StageCard({ name, isLast }: { name: string; isLast: boolean }) {
  return (
    <div className="space-y-2">
      <div className="rounded-md border border-zinc-200 bg-white px-4 py-2.5 text-sm text-zinc-600 dark:border-zinc-700 dark:bg-zinc-900/40 dark:text-zinc-300">
        {name}
      </div>
      {!isLast && (
        <ArrowDown className="ml-4 h-4 w-4 text-zinc-400 dark:text-zinc-500" />
      )}
    </div>
  )
}

/**
 * Dynamic Flow renderer driven entirely by project.architecture.dynamic_flow[].
 * No hardcoded stages — every stage comes from the data.
 */
function DynamicFlowStages({ stages }: { stages: string[] }) {
  if (!stages?.length) return null

  return (
    <div className="mt-4">
      {stages.map((stage, index) => (
        <StageCard key={stage} name={stage} isLast={index === stages.length - 1} />
      ))}
    </div>
  )
}

const tocItems: TocItem[] = [
  { id: 'problem-space', title: 'Problem Space' },
  { id: 'capabilities', title: 'Capabilities' },
  { id: 'architecture', title: 'Architecture' },
  { id: 'stories', title: 'Stories' },
]

export function ProjectRenderer({ project }: { project: Project }) {
  return (
    <div className="mx-auto max-w-5xl">
      <header>
        <p className="text-sm font-medium text-teal-500">Portfolio Project</p>
        <h1 className="mt-3 text-4xl font-bold tracking-tight text-zinc-800 sm:text-5xl dark:text-zinc-100">
          {project.project}
        </h1>
      </header>

      <div className="mt-8 lg:grid lg:grid-cols-[11rem_minmax(0,1fr)] lg:gap-10">
        <TOC items={tocItems} />

        <div className="space-y-8">
          <Section id="problem-space" title="Problem Space">
            <div className="space-y-6">
              <div>
                <GroupTitle>Current Problems</GroupTitle>
                <div className="mt-4 grid gap-4">
                  {project.problem_space.current_problems.map(
                    (problem, index) => (
                      <Card key={`current-${index}`}>
                        {problem.frames.map((frame) => (
                          <div key={frame.title} className="mt-4 first:mt-0">
                            <h4 className="text-sm font-semibold text-zinc-800 dark:text-zinc-100">
                              {frame.title}
                            </h4>
                            <ProblemFrameContent content={frame.content} />
                          </div>
                        ))}
                        {problem.project_response ? (
                          <p className="mt-4 text-sm text-zinc-600 dark:text-zinc-400">
                            {problem.project_response}
                          </p>
                        ) : null}
                      </Card>
                    ),
                  )}
                </div>
              </div>

              <div>
                <GroupTitle>Future Problems</GroupTitle>
                <div className="mt-4 grid gap-4">
                  {project.problem_space.future_problems.map(
                    (problem, index) => (
                      <Card key={`future-${index}`}>
                        {problem.frames.map((frame) => (
                          <div key={frame.title} className="mt-4 first:mt-0">
                            <h4 className="text-sm font-semibold text-zinc-800 dark:text-zinc-100">
                              {frame.title}
                            </h4>
                            <ProblemFrameContent content={frame.content} />
                          </div>
                        ))}
                        {problem.project_response ? (
                          <p className="mt-4 text-sm text-zinc-600 dark:text-zinc-400">
                            {problem.project_response}
                          </p>
                        ) : null}
                      </Card>
                    ),
                  )}
                </div>
              </div>
            </div>
          </Section>

          <Section id="capabilities" title="Capabilities">
            <div className="space-y-6">
              <div>
                <GroupTitle>Current Capabilities</GroupTitle>
                <div className="mt-4 grid gap-4 md:grid-cols-3">
                  {project.capabilities.current_capabilities.map(
                    (capability) => (
                      <Card key={capability.title}>
                        <h4 className="text-sm font-semibold text-zinc-800 dark:text-zinc-100">
                          {capability.title}
                        </h4>
                        {capability.description ? (
                          <CapabilityDescription
                            text={capability.description}
                          />
                        ) : null}
                        <LabelList
                          label="Supports"
                          items={capability.supports}
                        />
                        <LabelList
                          label="Includes"
                          items={capability.includes}
                        />
                        <LabelList
                          label="Current domains"
                          items={capability.current_domains}
                        />
                        <LabelList
                          label="Future domains"
                          items={capability.future_domains}
                        />
                      </Card>
                    ),
                  )}
                </div>
              </div>

              <div>
                <GroupTitle>Future Capabilities</GroupTitle>
                <div className="mt-4 grid gap-4 md:grid-cols-3">
                  {project.capabilities.future_capabilities.map(
                    (capability) => (
                      <Card key={capability.title}>
                        <h4 className="text-sm font-semibold text-zinc-800 dark:text-zinc-100">
                          {capability.title}
                        </h4>
                        {capability.description ? (
                          <CapabilityDescription
                            text={capability.description}
                          />
                        ) : null}
                        <LabelList
                          label="Supports"
                          items={capability.supports}
                        />
                      </Card>
                    ),
                  )}
                </div>
              </div>
            </div>
          </Section>

          <Section id="architecture" title="Architecture">
            <div className="space-y-5">
              {project.architecture.architectural_goal.from ||
              project.architecture.architectural_goal.toward ||
              project.architecture.architectural_goal.purpose ? (
                <Card>
                  <GroupTitle>Architectural Goal</GroupTitle>
                  <div className="mt-4 space-y-4 text-sm text-zinc-600 dark:text-zinc-400">
                    {project.architecture.architectural_goal.from ? (
                      <div>
                        <p className="text-xs font-medium tracking-wide text-zinc-400 uppercase dark:text-zinc-500">
                          From
                        </p>
                        <p className="mt-1">
                          {project.architecture.architectural_goal.from}
                        </p>
                      </div>
                    ) : null}
                    {project.architecture.architectural_goal.toward ? (
                      <div>
                        <p className="text-xs font-medium tracking-wide text-zinc-400 uppercase dark:text-zinc-500">
                          Toward
                        </p>
                        <p className="mt-1">
                          {project.architecture.architectural_goal.toward}
                        </p>
                      </div>
                    ) : null}
                    {project.architecture.architectural_goal.purpose ? (
                      <div>
                        <p className="text-xs font-medium tracking-wide text-zinc-400 uppercase dark:text-zinc-500">
                          Purpose
                        </p>
                        <p className="mt-1">
                          {project.architecture.architectural_goal.purpose}
                        </p>
                      </div>
                    ) : null}
                  </div>
                </Card>
              ) : null}

              {project.architecture.dynamic_flow?.length ? (
                <Card>
                  <GroupTitle>Dynamic Flow</GroupTitle>
                  <DynamicFlowStages
                    stages={project.architecture.dynamic_flow}
                  />
                </Card>
              ) : null}

              <Card>
                <GroupTitle>Static Structure</GroupTitle>

                <div className="mt-4 space-y-4">
                  {project.architecture.static_structure.map((layer) => (
                    <div
                      key={layer.title}
                      className="rounded-lg border-l-4 border-teal-500 bg-zinc-50 p-5 dark:bg-zinc-800/30"
                    >
                      <h3 className="text-sm font-semibold text-zinc-800 dark:text-zinc-100">
                        {layer.title}
                      </h3>
                      <div className="grid gap-4 md:grid-cols-2">
                        <LabelList
                          label="Responsibilities"
                          items={layer.responsibilities}
                        />
                        <LabelList
                          label="Core components"
                          items={layer.core_components}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </Card>
            </div>
          </Section>

          <Section id="stories" title="Stories">
            <div className="space-y-6">
              {project.stories.story_groups.map((group) => (
                <div key={group.title}>
                  {(group.core_discovery_title ||
                    group.core_discovery_content) && (
                    <div className="mt-6 border-t border-b border-zinc-200 py-7 dark:border-zinc-700">
                      <GroupTitle>{group.title}</GroupTitle>
                      {group.core_discovery_title && (
                        <h3 className="text-3xl font-semibold text-zinc-900 dark:text-zinc-100">
                          {group.core_discovery_title}
                        </h3>
                      )}
                      {group.core_discovery_content && (
                        <CoreDiscoveryContent
                          content={group.core_discovery_content}
                        />
                      )}
                    </div>
                  )}
                  <div className="mt-8 space-y-6">
                    {group.stories.map((story) => {
                      const [storyArea, storyTitle] = story.title.split(' — ')

                      return (
                        <Card key={story.title}>
                          <p className="text-xs font-medium tracking-wide text-zinc-400 uppercase dark:text-zinc-500">
                            Story
                          </p>
                          {storyTitle ? (
                            <div>
                              <div className="text-sm font-medium tracking-wide text-zinc-500 uppercase">
                                {storyArea}
                              </div>
                              <h3 className="mt-1 text-xl font-semibold text-zinc-900 dark:text-zinc-100">
                                {storyTitle}
                              </h3>
                            </div>
                          ) : (
                            <h4 className="text-sm font-semibold text-zinc-800 dark:text-zinc-100">
                              {story.title}
                            </h4>
                          )}
                          <TextList items={story.description} />
                          {story.problem ? (
                            <div className="mt-4">
                              <p className="flex items-center gap-2 text-xs font-medium tracking-wide text-zinc-400 uppercase dark:text-zinc-500">
                                <AlertTriangle className="h-3.5 w-3.5 text-teal-500 dark:text-teal-400" />
                                Problem
                              </p>
                              <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
                                {story.problem}
                              </p>
                            </div>
                          ) : null}
                          {story.analysis ? (
                            <div className="mt-4">
                              <p className="text-xs font-medium tracking-wide text-zinc-400 uppercase dark:text-zinc-500">
                                Analysis
                              </p>
                              <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
                                {story.analysis}
                              </p>
                            </div>
                          ) : null}
                          {story.discovery ? (
                            <div className="mt-4">
                              <p className="flex items-center gap-2 text-xs font-medium tracking-wide text-zinc-400 uppercase dark:text-zinc-500">
                                <Lightbulb className="h-3.5 w-3.5 text-teal-500 dark:text-teal-400" />
                                Discovery
                              </p>
                              <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
                                {story.discovery}
                              </p>
                            </div>
                          ) : null}
                          {story.outcome ? (
                            <div className="mt-4">
                              <p className="flex items-center gap-2 text-xs font-medium tracking-wide text-zinc-400 uppercase dark:text-zinc-500">
                                <CheckCircle2 className="h-3.5 w-3.5 text-teal-500 dark:text-teal-400" />
                                Outcome
                              </p>
                              <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
                                {story.outcome}
                              </p>
                            </div>
                          ) : null}
                        </Card>
                      )
                    })}
                  </div>
                </div>
              ))}
            </div>
          </Section>
        </div>
      </div>
    </div>
  )
}
